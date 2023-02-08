""" Copyright 2023 Jason Lines.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""Contains generic base web crawler classes required for module initialization.

Contains the generic base class `GenericCrawler` and `GenericCustomPaginator`
that all dynamically generated web crawlers. Not meant for external use.
"""

from types import FunctionType
from typing import Any, Callable, Generator, Iterable, Protocol
from dataclasses import asdict
import json
import asyncio

from botocore.exceptions import ParamValidationError, ClientError, OperationNotPageableError  # type: ignore

import aerographer.scan as scan
from aerographer.scan.context import CONTEXT
from aerographer.scan.parallel import asyncify, async_paginate
from aerographer.evaluations import Result
from aerographer.logger import logger
from aerographer.exceptions import (
    ActiveCrawlerScanExceptionError,
    FailedCrawlerScanExceptionError,
    PaginatorNotFoundExecptionError,
    MetadataClassNotFoundExecptionError,
    EvaluationMethodNotFoundError,
    EvaluationMethodResultOutputError,
    FrozenInstanceError,
)


class PaginateWrapper:
    """Wrapper class for boto3 client function without native paginator.

    Attributes:
        func (FunctionType): function to paginate.
        page_marker (str): attribute used to page with.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    def __init__(self, func: FunctionType, page_marker: str) -> None:
        self.func = func
        self.page_marker = page_marker

    def paginate(self, **kwargs: Any) -> Generator[dict[str, Any], Any, Any]:
        """Iterate through pages of resource.

        Iterages through all pages of information provided by API call
        made by provided function and returns result.

        Returns:
            Generator for list of pages.
        """
        page: dict[str, Any] = self.func(**kwargs)
        yield page

        if self.page_marker:
            if self.page_marker in page:
                while self.page_marker in page:
                    page = self.func(
                        **{self.page_marker: page[self.page_marker]} | kwargs
                    )
                    yield page

            elif 'IsTruncated' in page:
                while page['IsTruncated']:
                    page = self.func(
                        **{self.page_marker: page[self.page_marker]} | kwargs
                    )
                    yield page
        # TODO: Legacy method of using page marker. SERVICE_DEFINITIONS need to be updated with appropriate page_marker attributes.
        else:
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
        INCLUDE (set[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE: set[str] = set()

    def __init__(
        self, context: CONTEXT, paginator_func_name: str, page_marker: str
    ) -> None:
        self.context: CONTEXT = context
        self._paginate_func: Callable[..., Any] = getattr(
            context.client, paginator_func_name
        )
        self.page_marker = page_marker

        try:
            self.paginator: Callable[..., Any] = self.context.client.get_paginator(  # type: ignore
                self._paginate_func.__name__
            )
        except OperationNotPageableError:
            logger.trace(  # type: ignore
                'No native support for %s pagination, applying PaginateWrapper.',
                paginator_func_name,
            )
            self.paginator: PaginateWrapper = PaginateWrapper(  # type: ignore
                func=getattr(context.client, paginator_func_name),
                page_marker=self.page_marker,
            )

        setattr(self.paginator, 'context', context.name)
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
    __dataclass_fields__: dict[str, Any]


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
        INCLUDE (set[str]): List of resources that evaluations depend on.
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
    _frozen: bool = False
    evaluations: tuple[str, ...] = ()
    custom_paginator: GenericCustomPaginator | None = None
    INCLUDE: set[str] = set()

    # attributes set from service definitions
    globalService: bool
    serviceType: str
    resourceType: str
    resourceName: str
    paginator: str
    page_marker: str
    scanParameters: dict[str, Any]
    idAttribute: str

    def __init__(self, context: CONTEXT, metadata: dict[str, Any]) -> None:
        self.__metadata__ = self._build_metadata(metadata=metadata)
        self.context = context
        self.results: list[tuple[str, Result]] = []

        self._set_id()
        self._frozen = True

    def _set_id(self) -> None:
        """Set unique Id of class instance.

        Retrieves resource unique id from scan data, based on service
        definition idAttribute value, and assigned as class id attribute.
        """

        self.id: str = getattr(
            self.__metadata__, self.idAttribute, ''
        )  # pylint: disable=invalid-name

    @property
    def passed(self) -> bool:
        """Returns if all evaluations passed."""
        return all(result[1].status for result in self.results)

    def evaluate(self, evaluation: str) -> bool:
        """Run class evaluation methods.

        Runs all methods listed in `evaluations` class attribute and
        writes result to whiteboard.

        Args:
            evaluation (str): name of evaluation to run.

        Returns:
            bool: status of evaluation
        """

        # return status if evaluation already run
        for result in self.results:
            if result[0] == evaluation:
                return result[1].status

        # try to get requested evaluation function
        try:
            eval_func: Callable[..., Any] = getattr(self, evaluation)
        except AttributeError as err:
            raise EvaluationMethodNotFoundError(
                f'{evaluation} is not a valid evaluation name for {self.__class__.__name__}'
            ) from err

        # run evlaution and record result
        eval_result = eval_func()
        if not isinstance(eval_result, Result):
            raise EvaluationMethodResultOutputError(
                f'"{evaluation}" returned {type(eval_result)}. Must return {Result}.'
            )

        self.results.append((eval_func.__name__, eval_result))

        # return evalutions status
        return eval_result.status

    def run_evaluations(self) -> None:
        """Run class evaluation methods.

        Runs all methods listed in `evaluations` class attribute and
        writes result to whiteboard.
        """
        for evaluation in self.evaluations:
            logger.debug(
                'Running evalution %s on %s.%s',
                evaluation,
                self.__class__.__name__,
                self.id,
            )
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
            metadata_class = self._get_metadata_class(path)
            # Find any discrepencies between metadata cls and scan data. Report and remove missing attributes.
            for missing_attr in [
                attr
                for attr in metadata.keys()
                if attr not in metadata_class.__dataclass_fields__
            ]:
                logger.warn(
                    f'{metadata_class.__name__} received unexpected attribute: {missing_attr}'  # type: ignore
                )
                del metadata[missing_attr]
            return metadata_class(**metadata)  # type: ignore[operator]
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
                logger.trace(  # type: ignore
                    'Found custom paginator %s.', cls.custom_paginator.__name__  # type: ignore
                )
                return cls.custom_paginator(  # type: ignore[operator]
                    context=context,
                    paginator_func_name=cls.paginator,
                    page_marker=cls.page_marker,
                )

            logger.trace('Generating generic plaginator.')  # type: ignore[attr-defined]
            return GenericCustomPaginator(
                context=context,
                paginator_func_name=cls.paginator,
                page_marker=cls.page_marker,
            )
        except Exception:
            raise PaginatorNotFoundExecptionError(
                f'Failed to get paginator for {cls.__name__}'
            ) from None

    @classmethod
    async def _scan_context(cls, context: CONTEXT) -> None:
        """Run asyncronous scan on provided context.

        Runs the scan of target resource of provided conteext asyncrously.
        Once scan is complete, create a class instance for each resource found
        and add it to `RESOURCE COLLECTION`.

        Args:
            context (CONTEXT): context to use to run scan.

        Raises:
            FailedCrawlerScanExceptionError: Scan failed.
        """

        logger.debug('Scanning %s:%s...', context.name, cls.resourceName)

        # get pager
        paginator = cls._get_paginator(context)

        try:
            # run scan
            logger.trace(  # type: ignore
                '%s is getting asyncify %s:%s',
                cls.__name__,
                context.name,
                paginator.paginate.__name__,
            )  # type: ignore
            pages: Iterable[dict[str, Any]] = await asyncify(
                paginator.paginate, **cls.scanParameters
            )

            # create new class instance for each resource found and add to scan_results
            for resource in (
                resource for page in pages for resource in page[cls.resourceType]
            ):
                resource_instance: GenericCrawler = cls(
                    context=context, metadata=resource
                )
                scan.scan_results[cls.serviceType][cls.resourceName].update(
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

    @classmethod
    async def scan(cls) -> None:
        """Run asyncronous scan.

        Runs the scan of target resource asyncrously if scan is not already active or
        complete.

        Raises:
            FailedCrawlerScanExceptionError: Scan failed.
        """

        # make sure scan in not active or complete
        if cls.state == 'active':
            logger.debug('%s scan already in progress.', cls.__name__)
            raise ActiveCrawlerScanExceptionError
        elif cls.state == 'complete':
            logger.debug('%s scan already complete.', cls.__name__)
            return

        # mark scan as active
        cls.state = 'active'
        logger.info('Scanning %s:%s...', cls.serviceType, cls.resourceName)

        # make sure scan_results has proper data structure present
        if cls.serviceType not in scan.scan_results:
            scan.scan_results[cls.serviceType] = {}

        if cls.resourceName not in scan.scan_results[cls.serviceType]:
            scan.scan_results[cls.serviceType][cls.resourceName] = {}

        contexts = tuple([scan.CONTEXTS[0]]) if cls.globalService else scan.CONTEXTS

        await asyncio.gather(
            *(
                cls._scan_context(context)
                for context in contexts
                if context.service == cls.serviceType
            )
        )

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
            'service': self.serviceType,
            'resource': self.resourceType,
            'passed': self.passed,
            'context': {
                'name': self.context.name,
                'account_id': self.context.account_id,
                'region': self.context.region,
                'session': self.context.service,
            },
            'data': asdict(self.__metadata__),
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

    def __delattr__(self, __key: str):
        if self._frozen:
            raise FrozenInstanceError(f"cannot delete field '{__key}'")
        object.__delattr__(self, __key)

    def __setattr__(self, __key: str, __val: Any):
        if self._frozen:
            raise FrozenInstanceError(f"cannot assign to field '{__key}'")
        object.__setattr__(self, __key, __val)

    def __getattr__(self, __attr) -> GenericMetadata:
        try:
            return getattr(self.__metadata__, __attr)
        except AttributeError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{__attr}'"
            ) from None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.context.account_id}:{self.context.region}:{self.id})'

    def __str__(self):
        return self.id
