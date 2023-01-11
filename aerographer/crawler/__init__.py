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

"""Contains components required for module initialization and use.

Contains the `Crawler` class, which is the component used to interact
with the aerographer module. Also contains initialization functions for
dynamic building and retrieval of web crawler classes.

    Typical usage example:

    from aerographer import Crawler
    crawler = Crawler(
        services=["ec2"],
        skip=["ec2.network_interface"],
        profiles=["default"],
        regions=["us-east-1"],
        evaluations=["evaluations"]
    )
    crawler.scan()
"""

from datetime import datetime
import gc
import sys
import asyncio
import pkgutil
import importlib
import importlib.util
import os.path
from inspect import getmembers, isclass, isfunction
from dataclasses import make_dataclass, field
from types import FunctionType, ModuleType
from typing import Any

from botocore.exceptions import ClientError  # type: ignore

import aerographer.scan as scan
from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_scan
from aerographer.crawler.generic import GenericCrawler
from aerographer.logger import logger, LogFormatter
from aerographer.exceptions import (
    FailedCrawlerScanExceptionError,
    CrawlerNotFoundExecptionError,
    EvaluationModuleNotFoundExecptionError,
    EvaluationModuleFailedToLoadExecptionError,
    InvalidServiceDefinitionsExceptionError,
)
from aerographer.config import SERVICE_DEFINITIONS, PROFILES, ROLES, REGIONS

_CRAWLERS: dict[str, GenericCrawler] = {}


def _merge_dictionaries(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """Merge two dictionaries.

    Recursively merge two dictionaries.

    Args:
        dict1 (dict): first dictionary
        dict2 (dict): second dictionary

    Return:
        Merged dictionary.
    """

    for key, val in dict1.items():
        if isinstance(val, dict):
            dict2_node = dict2.setdefault(key, {})
            v: dict[str, Any] = val  # pylint: disable=invalid-name
            _merge_dictionaries(v, dict2_node)
        else:
            if key not in dict2:
                dict2[key] = val

    return dict2


def initialize_crawler(service: str, resource: str) -> GenericCrawler:
    """Initialize web crawler class for target resource.

    Collect service definition for provided service and resource and trigger
    creation of web crawler class.

    Args:
        service (str): Service of crawler class to create.
        resource (str): Resource of crawler class to create.

    Return:
        New web crawler class

    Raises:
        InvalidServiceDefinitionsExceptionError: invalid service definition found.
    """

    required_definition_attributes = [
        "resourceType",
        "idAttribute",
        "paginator",
        "scanParameters",
        "responseSchema",
    ]

    module_name = __name__.split('.', maxsplit=1)[0]

    try:
        class_definition = SERVICE_DEFINITIONS[service][resource]
        # make sure required properties are present
        if any(
            attribute not in class_definition
            for attribute in required_definition_attributes
        ):
            raise InvalidServiceDefinitionsExceptionError(
                f'Bad service definition found for {service}.{resource}'
            )

        class_definition = {
            k: v for k, v in class_definition.items() if k != 'responseSchema'
        }
        # build module path for later import
        class_path = f'{module_name}.service.{service}.{resource}'

        return _resource_crawler_class_factory(
            class_path=class_path,
            class_name=f'{service}_{resource}',
            class_definition={
                **{'serviceType': service, 'resourceName': resource},
                **class_definition,
            },
        )
    except KeyError:
        raise InvalidServiceDefinitionsExceptionError(
            f'No service definition found for {service}.{resource}'
        ) from None


def initialize_crawler_metadata(service: str, resource: str) -> tuple[type, ...]:
    """Initialize metadata classes for target resource.

    Collect service definition for provided service and resource and trigger
    creation of web crawler class.

    Args:
        service (str): Service of crawler class to create.
        resource (str): Resource of crawler class to create.

    Return:
        Tuple of new metadata classes

    Raises:
        InvalidServiceDefinitionsExceptionError: invalid service definition found.
    """

    try:
        class_definition = SERVICE_DEFINITIONS[service][resource]['responseSchema']
        # length of 0 means schema definition is empty
        if len(class_definition) == 0:
            raise InvalidServiceDefinitionsExceptionError(
                f'Bad metadata definition found for {service}.{resource}'
            )
        return tuple(
            _create_crawler_metadata_classes(
                class_name=f'{service}_{resource}', class_definition=class_definition
            )
        )
    except KeyError:
        raise InvalidServiceDefinitionsExceptionError(
            f'No metadata definition found for {service}.{resource}'
        ) from None


def _create_crawler_metadata_classes(
    class_name: str,
    class_definition: dict[str, Any] | list[Any] | Any,
    collection: list[type] | None = None,
) -> Any:
    """Create metadata classes.

    Dynamically create metadata class, and associated subclasses for provided service and resource
    parameters.

    Args:
        class_name (str): Name for new metadata class.
        class_definition (dict): data structure containing class attribute key/values.
        data (dict): Resource of crawler class to create.
        collection (list): Used for recursive creation of all metadata classes.

    Return:
        Tuple of new metadata classes
    """

    if collection is None:
        collection = []

    # standard recursive dict structure to allow creation all layers of metadata class
    if isinstance(class_definition, list):
        return [
            _create_crawler_metadata_classes(class_name, i, collection)
            for i in class_definition
        ]
    elif isinstance(class_definition, dict):
        for k, v in class_definition.items():  # pylint: disable=invalid-name
            class_definition[k] = _create_crawler_metadata_classes(
                f'{class_name}_{k}', v, collection
            )
        collection.append(
            _resource_crawler_metadata_class_factory(
                class_name=class_name,
                class_scheme=[(k, type(v)) for k, v in class_definition.items()],
            )
        )
        return collection
    else:
        return class_definition


def _resource_crawler_class_factory(
    class_path: str, class_name: str, class_definition: dict[str, Any]
) -> GenericCrawler:
    """Class factory for web crawler class.

    Collects class components from module at provided path and creates a new type
    of type `GenericCrawler` with name provides and definition provided, along with
    components gathered from module import.

    Args:
        class_path (str): path of module where methods are located
        class_name (str): Name for new metadata class.
        class_definition (dict): data structure containing class attribute key/values

    Return:
        New class.
    """

    module_name = __name__.split('.', maxsplit=1)[0]
    # import target module
    module = importlib.import_module(class_path)

    # collect class evaluation methods
    class_methods: dict[str, FunctionType] = {
        obj.__name__: obj
        for _, obj in getmembers(module)
        if isfunction(obj) and getattr(obj, '__evaluation__', False)
    }
    class_evaluation_func_names = {'evaluations': tuple(class_methods)}

    # if includes are present, format and add to class definition
    class_includes = getattr(module, 'INCLUDE', None)
    if class_includes:
        class_definition['INCLUDE'] = [
            f'{module_name}.service.{i}' for i in class_includes
        ]

    # get custom paginator from service module if it exists
    parent_module = importlib.import_module('.'.join(module.__name__.split('.')[:-1]))
    class_paginator: dict[str, type] = {
        'custom_paginator': obj
        for _, obj in getmembers(parent_module)
        if isclass(obj)
        and obj.__name__
        == (f'{_serialize_class_name(class_definition["resourceName"])}Paginator')
    }

    class_name = _serialize_class_name(class_name)

    return type(  # type: ignore
        class_name,
        (GenericCrawler,),
        {
            **class_definition,
            **class_paginator,
            **class_evaluation_func_names,
            **class_methods,
        },
    )


def _resource_crawler_metadata_class_factory(
    class_name: str, class_scheme: list[tuple[str, type]]
) -> type:
    """Class factory for metadata class.

    Creates a new dataclass with name and definition provided. Ensures all attributes
    are immutable.

    Args:
        class_name (str): Name for new metadata class.
        class_scheme (dict): data structure containing class attribute key/values

    Return:
        New class.
    """

    class_fields: list[tuple[str, type, Any]] = []

    # Transform class definition to dataclass definition
    for i in class_scheme:
        if i[1] is list:
            class_fields.append((*i, field(default_factory=tuple)))
        elif i[1] is dict:
            class_fields.append((*i, field(default_factory=dict)))
        elif i[1] in (int, float):
            class_fields.append((*i, field(default=0)))
        elif i[1] is str:
            class_fields.append((*i, field(default='')))
        elif i[1] is bool:
            class_fields.append((*i, field(default=False)))

    class_name = _serialize_class_name(f'{class_name}_metadata')

    return make_dataclass(
        cls_name=class_name, fields=class_fields, frozen=True, slots=True
    )


def _serialize_class_name(name: str) -> str:
    """Serialize class name.

    Removes all dashes and capatilizes all words.

    Args:
        name (str): Name to serialize.

    Return:
        Serialized name.
    """

    return ''.join([word.capitalize() for word in name.split('_')])


def _import_external_evaluations(path: str) -> dict[str, Any]:
    """Load external evaluations.

    Load provided external evalulation modules, and all submodules.

    Args:
        path (str): Path to external module

    Return:
        Dictionary containing evaluation data and methods.

    Raises:
        EvaluationModuleNotFoundExecptionError: Failed to retrieve evaluation data.
    """

    evaluations: dict[str, Any] = {}

    # try and import, either by path (if file), or as module (if directory)
    try:
        logger.debug('loading module from %s...', path)
        if os.path.isfile(path):
            spec = importlib.util.spec_from_file_location("external_evaluations", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            sys.path.append(path)
            module = importlib.import_module(path)
    except ModuleNotFoundError as err:
        raise EvaluationModuleFailedToLoadExecptionError(
            f'Failed to load {path} -- {err}'
        ) from err
    except ImportError as err:
        raise EvaluationModuleNotFoundExecptionError(
            f'Could not load module {path}'
        ) from err

    # search module for submodules
    if getattr(module, '__path__', None):
        for _, sub_module_name, is_pkg in pkgutil.walk_packages(
            module.__path__, module.__name__ + '.'
        ):
            if not is_pkg:
                # recurively load submodules
                evaluations = _merge_dictionaries(
                    evaluations, _import_external_evaluations(sub_module_name)
                )
    # no submodules, load functions from this module
    else:
        evaluations = _merge_dictionaries(
            evaluations, _extract_external_evaluation_functions(module)
        )

    return evaluations


def _extract_external_evaluation_functions(module: ModuleType) -> dict[str, Any]:
    """Extract evaluation data from module.

    Extracts evaluation methods and data module.

    Args:
        module (str): Path to external module.

    Return:
        Dictionary containing evaluation data and methods.
    """

    module_data: dict[str, Any] = {}

    # for each evaluation function in module
    for name, func in {
        obj.__name__: obj
        for _, obj in getmembers(module)
        if isfunction(obj) and getattr(obj, '__evaluation__', False)
    }.items():

        # make sure module_data is populated appropriately
        if func.__service__ not in module_data:  # type: ignore
            module_data[func.__service__] = {func.__resource__: {'include': set()}}  # type: ignore
        if func.__resource__ not in module_data[func.__service__]:  # type: ignore
            module_data[func.__service__][func.__resource__] = {'include': set()}  # type: ignore

        # update module_data with function data
        module_data[func.__service__][func.__resource__]['include'].update(  # type: ignore
            func.__includes__  # type: ignore
        )
        module_data[func.__service__][func.__resource__].update({name: func})  # type: ignore

    return module_data


def get_crawler(
    path: str, skip: list[str], quiet_skip: bool = False
) -> list[GenericCrawler]:
    """Get crawler class.

    Return all web crawler classes from the service path requested.

    Args:
        service (str): name of service to get web crawlers for.
        skip (list[str]): service paths to skip.
        quiet_skip (bool): (Optional) Supresses skip debug messages. Defaults to `False`.

    Return:
        List of web crawlers.

    Raises:
        CrawlerNotFoundExecptionError: failed to get GenericCrawler class.
    """

    crawlers: list[GenericCrawler] = []

    # skip any modules included in skip list, if service or service.resource match exactly
    if any(substring == path.rsplit('.', 1)[0] for substring in skip) or any(
        substring == path for substring in skip
    ):
        if not quiet_skip:
            logger.debug('Skipping submodule %s.', path)
        return []

    if path in _CRAWLERS:
        logger.debug('Pulling %s from cache', path)
        crawlers.append(_CRAWLERS[path])
    else:
        try:
            module = importlib.import_module(path)
            logger.debug('loading module %s...', path)
        except ModuleNotFoundError as err:
            raise CrawlerNotFoundExecptionError(
                f'Failed to load {path} -- {err}'
            ) from err
        except ImportError as err:
            raise CrawlerNotFoundExecptionError(f'Could not load {path}.') from err

        # search for any submodules
        if getattr(module, '__path__', None):
            for _, sub_module_name, is_pkg in pkgutil.walk_packages(
                module.__path__, module.__name__ + '.'
            ):
                if not is_pkg:
                    # recurively load submodules
                    crawlers.extend(
                        get_crawler(
                            path=sub_module_name, skip=skip, quiet_skip=quiet_skip
                        )
                    )

        # no submodules, gather classes from this module
        else:
            try:
                crawler = _get_crawler_class(module)
                _CRAWLERS[path] = crawler
                crawlers.append(crawler)
            except CrawlerNotFoundExecptionError as err:
                raise CrawlerNotFoundExecptionError(f'Failed to load {path}.') from err

    return crawlers


def _get_crawler_class(module: ModuleType) -> GenericCrawler:
    """Get web crawler class from module.

    Scans provided module and returns the `GenericCrawler` if found.

    Args:
        module (ModuleType): Module to scan.

    Return:
        GenericCrawler class or None.

    Raises:
        CrawlerNotFoundExecptionError: if class is not found.
    """
    try:
        return next(
            (
                obj  # type: ignore
                for _, obj in getmembers(module)
                if isclass(obj) and issubclass(obj, GenericCrawler)
            )
        )
    except StopIteration as err:
        raise CrawlerNotFoundExecptionError(
            f'Did not find a crawler class in {module}'
        ) from err


def get_crawlers(
    services: str | list[str],
    skip: str | list[str] | None = None,
    quiet_skip: bool = False,
) -> list[GenericCrawler]:
    """Get list of web crawlers.

    Returns a list of all web crawler classes ready to start scanning
    from a list of service paths. Skip sub paths by providing `skip`
    parameter.

    Args:
        services (str|list): Service path, or list of service paths.
        skip (str|list): Service path, or list of service paths, to skip.
        quiet_skip (bool): (Optional) Supresses skip debug messages. Defaults to `False`.

    Return:
        List of web crawler class.
    """

    # safe default to []
    if skip is None:
        skip = []

    module_name = __name__.split('.', maxsplit=1)[0]

    # set top level service scan if `*` used
    if services == '*':
        services = [f'{module_name}.service']
    else:
        # convert to list in necessary, format string properly to further use
        services = [services] if not isinstance(services, list) else services
        services = [
            f'{module_name}.service.{service}'
            if not service.startswith(f'{module_name}.service.')
            else service
            for service in services
        ]

    # convert to list in necessary, format string properly to further use
    skip = [skip] if not isinstance(skip, list) else skip
    skip = [
        f'{module_name}.service.{s}'
        if not s.startswith('{module_name}.service.')
        else s
        for s in skip
    ]

    # return crawlers from service paths
    try:
        return sum([get_crawler(service, skip, quiet_skip) for service in services], [])
    except CrawlerNotFoundExecptionError as err:
        logger.error(err)
        sys.exit(1)


def get_crawler_includes(crawlers: list[GenericCrawler]) -> list[GenericCrawler]:
    """Get include crawlers.

    Returns a list of all crawler dependencies for provides list of crawlers.

    Args:
        crawlers (list): List of web crawlers to get dependencies for.

    Return:
        List of web crawler classes.
    """
    provided = [f'{crawler.serviceType}.{crawler.resourceName}' for crawler in crawlers]
    includes = list(set(sum([crawler.INCLUDE for crawler in crawlers], [])))
    include_crawlers = [
        crawler
        for crawler in get_crawlers(services=includes, skip=provided, quiet_skip=True)
        if crawlers and crawler.state == 'initialized'
    ]

    if include_crawlers:
        include_crawlers.extend(
            get_crawler_includes(list(set(include_crawlers + crawlers)))
        )

    return include_crawlers


async def deploy_crawlers(
    crawlers: list[GenericCrawler],
) -> None:
    """Deploy web crawlers.

    Triggers list of web crawlers to scan their target resource.

    Args:
        crawlers (list): List of web crawlers to deploy.

    Raises:
        FailedCrawlerScanExceptionError: web crawler scan failed
    """
    logger.debug('Gathering included crawlers...')
    for name, includes in [
        (crawler.__name__, crawler.INCLUDE) for crawler in crawlers  # type:ignore
    ]:
        logger.trace('%s: %s', name, ','.join(includes))  # type: ignore

    include_crawlers = get_crawler_includes(crawlers=crawlers)

    try:
        await asyncio.gather(*(async_scan(s) for s in crawlers + include_crawlers))
    except ClientError as err:
        raise FailedCrawlerScanExceptionError(err) from err


class Crawler:
    """Runs web crawler scans and evaluations.

    Primary class to initialize module and run scans and evaluations.


    Attributes:
        services (str|list[str]): (optional) Target service(s). Default: all services.
        skip (str|list[str]): (optional) Service(s) to skip. Default: []
        profiles (list[str]): (optional) AWS profile(s) for accounts to scan. Default ['default'].
        regions (list[str]): (optional) AWS region(s) to scan. Default ['us-east-1'].
        role (str): (optional) AWS role name to assume in each account.
        evaluations (list[str]): (optional) Module containing evalution functions to run.
        crawlers (GenericCrawler): (class attribute) Collection of web crawlers to use.

    Methods:
        scan(self): Trigger scan of targets.
    """

    def __init__(
        self,
        services: str | list[str] = '*',
        skip: str | list[str] | None = None,  # safe default for list
        profiles: list[str] | None = None,  # safe default for list
        roles: list[str] | None = None,  # safe default for list
        regions: list[str] | None = None,  # safe default for list
        evaluations: list[str] | None = None,  # safe default for list
    ) -> None:
        """Class initializer."""

        if logger.getEffectiveLevel() <= 10:
            LogFormatter.debug = True

        if services != '*' and isinstance(services, str):
            services = [services]
        if skip is not None and isinstance(skip, str):
            skip = [skip]

        self.services = services
        self.profiles = profiles or PROFILES
        self.roles = roles or ROLES
        self.regions = regions or REGIONS
        self.skip = skip or []
        self.evaluations = evaluations or []
        self._external_evalutations: dict[str, Any] = {}

        # apply provided external evaluations to web crawlers
        for path in self.evaluations:
            try:
                self._external_evalutations = _merge_dictionaries(
                    self._external_evalutations, _import_external_evaluations(path)
                )
            except (
                EvaluationModuleNotFoundExecptionError,
                EvaluationModuleFailedToLoadExecptionError,
            ) as err:
                logger.warning(err)
        self._apply_external_evaluations()

        # initialize and get web crawlers
        try:
            logger.debug('Gathering crawlers for %s', ', '.join(self.services))
            self.crawlers = get_crawlers(self.services, self.skip)
            if self.crawlers is None:
                logger.error('No crawlers found for %s', self.services)
                sys.exit(1)
        except CrawlerNotFoundExecptionError as err:
            logger.error('Error getting crawlers for %s -- %s', self.services, err)
            sys.exit(1)

        # initialize contexts
        self.accounts = [
            {'profile': profile, 'regions': self.regions, 'role': role}
            for profile in self.profiles
            for role in self.roles
        ]
        scan.CONTEXTS = scan.init(
            self.accounts,
            services=set([crawler.serviceType for crawler in self.crawlers]),
        )

    def _apply_external_evaluations(self) -> None:
        """Apply external evaluations to crawlers.

        Takes provide external evalutions module, determines target service and
        resource, extracts evalution functions, and applies to target web crawlers.
        """
        for service in [
            f'{service}.{resource}'
            for service, resources in self._external_evalutations.items()
            for resource in resources
        ]:
            for crawler in get_crawlers(services=service):
                try:
                    external_evaluation_includes = list(
                        self._external_evalutations[crawler.serviceType][
                            crawler.resourceName
                        ].pop('include')
                    )
                    external_evaluation_functions = self._external_evalutations[
                        crawler.serviceType
                    ][crawler.resourceName]
                    # build new includes list
                    class_includes = list(
                        set(crawler.INCLUDE + external_evaluation_includes)
                    )

                    logger.debug(
                        'Applying external evaluation methods to %s.',
                        type(crawler).__name__,
                    )
                    # set new crawler includes
                    setattr(crawler, 'INCLUDE', class_includes)

                    for name, func in external_evaluation_functions.items():
                        # add function name to evaluations func name list
                        crawler.evaluations = tuple(
                            [i for i in crawler.evaluations] + [name]
                        )
                        # add functions to crawler
                        setattr(crawler, name, func)

                except KeyError:
                    logger.debug(
                        'No external evaluation functions found for %s.',
                        type(crawler).__name__,
                    )
                    continue

    def scan(self) -> dict[str, Any]:
        """Performs scan and evaluations of all web crawlers.

        Triggers each web crawler to scan target resource and perform any
        present evaluations. Forces garabage cleanup to after scan as scan
        can consume a lot of memory.

        Return:
            Dictionary containing all class instances created by scan.
        """
        try:
            # run scan and force GC
            start = datetime.now()
            asyncio.run(deploy_crawlers(crawlers=self.crawlers))
            gc.collect()
            logger.trace('Scan time: %s', datetime.now() - start)  # type:ignore
        except FailedCrawlerScanExceptionError as err:
            logger.error('Scan failed -- %s', err)
            sys.exit(1)

        # build new dictionary that only contains class instances included in targeted scans
        # this is so instances created to fulfill dependancy scan requirements are not returned
        RETURN_COLLECTION: dict[str, Any] = {}  # pylint: disable=invalid-name

        for crawler in self.crawlers:
            if crawler.serviceType not in RETURN_COLLECTION:
                RETURN_COLLECTION[crawler.serviceType] = {}

            RETURN_COLLECTION[crawler.serviceType][crawler.resourceName] = SURVEY[
                crawler.serviceType
            ][crawler.resourceName]

            for resource in RETURN_COLLECTION[crawler.serviceType][
                crawler.resourceName
            ].values():
                resource.run_evaluations()

        return RETURN_COLLECTION
