"""Contains generic base web crawler classes required for module initialization.

Contains the generic base class `GenericCrawler` and `GenericCustomPaginator`
that all dynamically generated web crawlers. Not meant for external use.
"""

from types import FunctionType
from typing import Any, Callable, Generator, Iterable, Protocol
from dataclasses import asdict
import json

from botocore.exceptions import ParamValidationError, ClientError, OperationNotPageableError  # type: ignore

import aerographer.scan as scan
from aerographer.scan.context import CONTEXT
from aerographer.scan.parallel import asyncify, async_paginate
from aerographer.evaluations import Result
from aerographer.whiteboard import WHITEBOARD
from aerographer.logger import logger
from aerographer.exceptions import (
    ActiveCrawlerScanExceptionError,
    FailedCrawlerScanExceptionError,
    PaginatorNotFoundExecptionError,
    MetadataClassNotFoundExecptionError,
    EvaluationMethodNotFoundError,
)


class PaginateWrapper:
    """Wrapper class for boto3 client function without native paginator.

    Attributes:
        func: function to paginate.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    def __init__(self, func: FunctionType) -> None:
        self.func = func

    def paginate(self, **kwargs: Any) -> Generator[dict[str, Any], Any, Any]:
        """Iterate through pages of resource.

        Iterages through all pages of information provided by API call
        made by provided function and returns result.

        Returns:
            Generator for list of pages.
        """
        page: dict[str, Any] = self.func(**kwargs)
        yield page

        if 'NextToken' in page:
            while 'NextToken' in page:
                page = self.func(NextToken=page['NextToken'], **kwargs)
                yield page

        elif 'IsTruncated' in page:
            while page['IsTruncated']:
                page = self.func(Marker=page['Marker'], **kwargs)
                yield page


class GenericCustomPaginator:
    """Abstract class for custom paginators.

    Custom paginators need to be used when boto3 does not provided a builtin
    paginator for a specific resource. Custom paginators must return a list of
    pages following the same format that boto3 default paginators provide.
    The `INCLUDE` class attribute can be used to ensure required dependant data
    is available prior to retrieving resource page data.


    Attributes:
        INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE: list[str] = []

    def __init__(self, context: CONTEXT, paginator_func_name: str) -> None:

        self.context: CONTEXT = context
        self._paginate_func: Callable[..., Any] = getattr(
            context.client, paginator_func_name
        )

        try:
            self.paginator: Callable[..., Any] = self.context.client.get_paginator(  # type: ignore
                self._paginate_func.__name__
            )
        except OperationNotPageableError:
            self.paginator: PaginateWrapper = PaginateWrapper(  # type: ignore
                getattr(context.client, paginator_func_name)
            )

        setattr(self.paginator, 'service', context.service)
        setattr(self.paginator, 'function', paginator_func_name)

    async def paginate(self, **kwargs: Any) -> tuple[dict[str, Any], ...]:
        """Default method definition.

        Inheriting class must implement method that retrieves list of pages for resource data.

        Returns:
            List of pages.
        """
        pages = await async_paginate(paginator=self.paginator, **kwargs)
        return tuple(pages[0])


class GenericMetadata(Protocol):
    """Protocol for dataclass, used for type checking for Metadata class."""

    # checking for this attribute is currently the most reliable way
    # to ascertain that something is a dataclass
    __dataclass_fields__: dict[Any, Any]


class GenericCrawler:
    """Abstract class for web crawler classes.

    Web crawler classes are generated dynamically at scan runtime. A module under the aerographer.service
    with the target resource must exist, it can be an empty file or can contain evaluation functions. A
    corresponding service definition must be present in the service definitions json configuration file.
    If a custom paginator is required, it must be located in the target aerographer.service __init__.py
    file. Custom paginators and evaluation functions (both local and externally provided) are detected and
    attached to the web crawler class during class generation. Data assigned to class instances are dynamically
    build dataclasses that are immutable and designed for efficient data retrieval.


    Attributes:
        state (str): State of web crawler class: Can be `initialized` (no scan performed), `active` (actively scanning),
            or `complete` (scan complete).
        evaluations (tuple): List of evlaution method names.
        custom_paginator (Callable): Custom pagintaor class.
        INCLUDE (list[str]): List of resources that evaluations depend on.
        serviceType (str): Name of target service.
        resourceType (str): Resource data identifier in scan pages.
        resourceName (str): Name of target resource.
        paginator (str): Name of boto3 function to use for resource scan.
        scanParameters (dict): Additional parameters to pass to paginator.
        idAttribute (str): Resource id attribute in resource data.

    Methods:
        evaluate(): Run class evaluation methods.
        scan(): (class method) Scan resource and return a new class instance for each resource found.
    """

    state: str = 'initialized'
    evaluations: tuple[str, ...]
    custom_paginator: Callable[..., Any] | None = None
    INCLUDE: list[str] = []

    # attributes set from service definitions
    serviceType: str
    resourceType: str
    resourceName: str
    paginator: str
    scanParameters: dict[str, Any]
    idAttribute: str

    def __init__(self, context: CONTEXT, metadata: dict[str, Any]) -> None:

        self.data = self._build_metadata(metadata=metadata)
        self.context = context
        self.results: list[tuple[str, str, bool]] = []

        self._set_id()
        self._set_infrastructure_as_code_id()

    def _set_id(self) -> None:
        """Set unique Id of class instance.

        Retrieves resource unique id from scan data, based on service
        definition idAttribute value, and assigned as class id attribute.
        """

        self.id: str = getattr(
            self.data, self.idAttribute, ''
        )  # pylint: disable=invalid-name

    def _set_infrastructure_as_code_id(self) -> None:
        """Set infrastructure as code Id of class instance.

        Retrieves infrastructure as code id from scan tag data and
        assigned as class iac_id attribute. Empty string assigned if
        no value is found.
        """

        iac_id: str = ''
        try:
            iac_id = next(
                (
                    tag.Value  # type: ignore
                    for tag in self.data.Tags  # type: ignore
                    if tag.Key == 'aws:cloudformation:stack-id'  # type: ignore
                ),
                '',
            )
        except AttributeError:
            try:
                iac_id = next(
                    (
                        tag.Value  # type: ignore
                        for tag in self.data.TagSet  # type: ignore
                        if tag.Key == 'aws:cloudformation:stack-id'  # type: ignore
                    ),
                    '',
                )
            except AttributeError:
                pass
                # logger.debug('no iac id found for %s.%s', self.__class__.__name__, self.id) <--- should be logging level trace

        self.iac_id: str = iac_id

    @property
    def passed(self) -> bool:
        """Returns if all evaluations passed."""
        return all(result[2] for result in self.results)

    def evaluate(self, evaluation: str) -> bool:
        """Run class evaluation methods.

        Runs all methods listed in `evaluations` class attribute and
        writes result to whiteboard.

        Args:
            evaluation (str): name of evaluation to run.

        Returns:
            bool: status of evaluation
        """

        # try to get requested evaluation function
        try:
            eval_func: Callable[..., Any] = getattr(self, evaluation)
        except AttributeError as err:
            raise EvaluationMethodNotFoundError(
                f'{evaluation} is not a valid evaluation name for {self.__class__.__name__}'
            ) from err

        # return status if evaluation already run
        for result in self.results:
            if result[0] == evaluation:
                return result[2]

        # run evlaution and record result if returned Result object
        eval_result = eval_func()
        if isinstance(eval_result, Result):
            self.results.append(
                (eval_func.__name__, eval_result.message, eval_result.status)
            )
            WHITEBOARD.write(
                section='evaluations',
                title=f'{eval_func.__name__}:{self.id}',
                msg={'finding': eval_result.message, 'passed': eval_result.status},
            )

        # return evalutions status
        return eval_result.status

    def run_evaluations(self) -> None:
        """Run class evaluation methods.

        Runs all methods listed in `evaluations` class attribute and
        writes result to whiteboard.
        """
        for evaluation in self.evaluations:
            self.evaluate(evaluation=evaluation)

    def _build_metadata(
        self, metadata: dict[str, Any] | list[Any] | Any, path: str = ''
    ) -> GenericMetadata | tuple[Any] | Any:
        """Populates metadata class.

        Creates a new metadata class populated with provided metadata.

        Args:
            metadata (dict): metadata to populate metadata class instance with.
            path (str): (Optional) current path for data recursion tracking. Defaults to empty string.

        Return:
            Populated metadata class. Metadata class data is immuntable.
        """

        # standard recursive dict structure to allow retrieving and populating all
        # layers of metadata class
        if isinstance(metadata, list):
            return tuple(self._build_metadata(i, path) for i in metadata)
        elif isinstance(metadata, dict):
            for k, v in metadata.items():  # pylint: disable=invalid-name
                metadata[k] = self._build_metadata(v, path + k.capitalize())
            return self._get_metadata_class(path)(**metadata)  # type: ignore
        else:
            return metadata

    @classmethod
    def _get_metadata_class(cls, name: str = '') -> GenericMetadata:
        """Get requested metadata class.

        Retrieves metadata class with name provided.

        Args:
            name (str): Name of metadata class to get.

        Return:
            Requested metadata class.

        Raises:
            MetadataClassNotFoundExecptionError: Metadata class not found.
        """

        # metadata classes are created dynamically during initialization and
        # assigned as class attributes where they can be retrieved here.
        metadata_class = getattr(cls, f'{cls.__name__}{name}Metadata', None)
        if not metadata_class:
            raise MetadataClassNotFoundExecptionError(
                f'Failed to find "{cls.__name__}{name}Metadata".'
            )

        return metadata_class

    @classmethod
    def _get_paginator(cls, context: CONTEXT) -> GenericCustomPaginator:
        """Get class paginator.

        Return custom paginator if one if assigned, else returns an generic
        custom paginator wrapping the boto3 builtin paginator for target to
        allow asyncronous API calls.

        Args:
            context (CONTEXT): context to use to get builtin paginator.

        Return:
            Requested metadata class.

        Raises:
            PaginatorNotFoundExecptionError: Paginator not found.
        """

        try:
            if cls.custom_paginator is not None:
                return cls.custom_paginator(  # pylint: disable=not-callable
                    context=context,
                    paginator_func_name=cls.paginator,  # pylint: disable=not-callable
                )

            return GenericCustomPaginator(
                context=context, paginator_func_name=cls.paginator
            )
        except Exception:
            raise PaginatorNotFoundExecptionError(
                f'Failed to get paginator for {cls.__name__}'
            ) from None

    @classmethod
    async def scan(cls) -> None:
        """Run asyncronous scan.

        Runs the scan of target resource asyncrously if scan is not already active or
        complete. Once scan is complete, create a class instance for each resource found
        and add it to `RESOURCE COLLECTION`.

        Raises:
            FailedCrawlerScanExceptionError: Scan failed.
        """

        # make sure scan in not active or complete
        if cls.state == 'active':
            logger.debug('%s scan already in progress, skipping...', cls.__name__)
            raise ActiveCrawlerScanExceptionError
        elif cls.state == 'complete':
            return

        # make sure SURVEY has proper data structure present
        if cls.serviceType not in scan.SURVEY:
            scan.SURVEY[cls.serviceType] = {}

        if cls.resourceName not in scan.SURVEY[cls.serviceType]:
            scan.SURVEY[cls.serviceType][cls.resourceName] = {}

        # mark scan as active
        cls.state = 'active'
        logger.info('Scanning %s:%s...', cls.serviceType, cls.resourceName)
        for context in [
            context for context in scan.CONTEXTS if context.service == cls.serviceType
        ]:

            logger.debug('Scanning %s:%s...', context.name, cls.resourceName)

            # get pager
            paginator = cls._get_paginator(context)

            try:
                # run scan
                # logger.debug('%s is getting asyncify %s',cls.__name__ ,paginator.paginate.__name__) <-- should be trace level log
                pages: Iterable[dict[str, Any]] = await asyncify(
                    paginator.paginate, **cls.scanParameters
                )

                # create new class instance for each resource found and add to SURVEY
                for resource in (
                    resource for page in pages for resource in page[cls.resourceType]
                ):
                    resource_instance: GenericCrawler = cls(
                        context=context, metadata=resource
                    )
                    scan.SURVEY[cls.serviceType][cls.resourceName].update(
                        {resource_instance.id: resource_instance}
                    )

            except ParamValidationError as err:
                raise FailedCrawlerScanExceptionError(
                    (
                        f'Failed scan of {context.name}:{cls.resourceName} - invalid scan parameters.'
                    )
                ) from err
            except (ClientError, MetadataClassNotFoundExecptionError) as err:
                raise FailedCrawlerScanExceptionError(err) from err

        # mark scan as complete
        cls.state = 'complete'
        logger.info('Scan of %s:%s complete.', cls.serviceType, cls.resourceName)

    def asdict(self) -> dict:
        """Return crawler data as dictionary.

        Returns dictionary representation of crawler instance.

        Returns:
            Dictionary of attributes.
        """

        data = {
            'id': self.id,
            'iac_id': self.iac_id,
            'service': self.serviceType,
            'resource': self.resourceType,
            'passed': self.passed,
            'context': {
                'name': self.context.name,
                'account_id': self.context.account_id,
                'region': self.context.region,
                'session': self.context.service,
            },
            'data': asdict(self.data),
        }

        return data

    def asjson(self) -> str:
        """Return crawler data as json string.

        Returns json string representation of crawler instance.

        Returns:
            JSON string of attributes.
        """

        return json.dumps(self.asdict(), default=str)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, GenericCrawler):
            return __o.id == self.id
        return str(__o) == self.id
