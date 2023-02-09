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

"""Contains crawler initialization functions.

Contains functions for dynamic building and retrieval of web crawler
classes, webcrawler metadata classes, and retrieval and assignment of
external evaulation methods. Not meant for external use.
"""

import os
import sys
import importlib
import pkgutil
from dataclasses import make_dataclass, field, is_dataclass, asdict
from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers, isclass, isfunction
from types import ModuleType, FunctionType
from typing import Any, no_type_check

from aerographer.crawler.generic import GenericCrawler, GenericMetadata
from aerographer.logger import logger
from aerographer.config import MODULE_NAME
from aerographer.exceptions import (
    InvalidServiceDefinitionError,
    CrawlerNotFoundError,
    EvaluationModuleNotFoundError,
    EvaluationModuleFailedToLoadError,
    EvaluationMethodNameError,
)

_CRAWLER_CACHE: dict[str, GenericCrawler] = {}


def import_crawlers(
    path: str, skip: list[str] | None = None, quiet_skip: bool = False
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
        CrawlerNotFoundError: failed to get GenericCrawler class.
    """

    skip = skip or []
    crawlers: list[GenericCrawler] = []

    # skip any modules included in skip list, if service or service.resource match exactly
    if any(substring == path.rsplit('.', 1)[0] for substring in skip) or any(
        substring == path for substring in skip
    ):
        if not quiet_skip:
            logger.debug('Skipping submodule %s.', path)
        return []

    if path in _CRAWLER_CACHE:
        logger.debug('Loading %s from cache', path)
        crawlers.append(_CRAWLER_CACHE[path])
    else:
        try:
            module = importlib.import_module(path)
            logger.debug('loading module %s...', path)
        except ModuleNotFoundError as err:
            raise CrawlerNotFoundError(f'Failed to load {path} -- {err}') from err
        except ImportError as err:
            raise CrawlerNotFoundError(f'Could not load {path}.') from err

        # search for any submodules
        if getattr(module, '__path__', None):
            for _, sub_module_name, is_pkg in pkgutil.walk_packages(
                module.__path__, module.__name__ + '.'
            ):
                if not is_pkg:
                    # recurively load submodules
                    crawlers.extend(
                        import_crawlers(
                            path=sub_module_name, skip=skip, quiet_skip=quiet_skip
                        )
                    )

        # no submodules, gather classes from this module
        else:
            try:
                crawler = _get_crawler_class(module)
                _CRAWLER_CACHE[path] = crawler
                crawlers.append(crawler)
            except CrawlerNotFoundError as err:
                raise CrawlerNotFoundError(f'Failed to load {path}.') from err

    return crawlers


def initialize_crawler(
    service: str, resource: str, class_definition: dict[str, Any]
) -> GenericCrawler:
    """Initialize web crawler class for target resource.

    Collect service definition for provided service and resource and trigger
    creation of web crawler class.

    Args:
        service (str): Service of crawler class to create.
        resource (str): Resource of crawler class to create.

    Return:
        New web crawler class

    Raises:
        InvalidServiceDefinitionError: invalid service definition found.
    """

    required_definition_attributes = [
        "globalService",
        "resourceType",
        "idAttribute",
        "paginator",
        "page_marker",
        "scanParameters",
        "responseSchema",
    ]

    logger.trace('Collecting %s.%s crawler class attributes', service, resource)  # type: ignore

    # make sure required properties are present
    for attribute in required_definition_attributes:
        if attribute not in class_definition:
            raise InvalidServiceDefinitionError(
                f'Bad service definition found for {service}.{resource}. Missing "{attribute}" attribute.'
            )

    class_definition = {
        k: v for k, v in class_definition.items() if k != 'responseSchema'
    }
    # build module path for later import
    service_path = f'{MODULE_NAME}.service.{service}'

    return _resource_crawler_class_factory(
        service_path=service_path,
        class_name=f'{service}_{resource}',
        class_definition={
            **{'serviceType': service, 'resourceName': resource},
            **class_definition,
        },
    )


def initialize_crawler_metadata(
    service: str, resource: str, class_definition: dict[str, Any]
) -> tuple[GenericMetadata, ...]:
    """Initialize metadata classes for target resource.

    Collect service definition for provided service and resource and trigger
    creation of web crawler class.

    Args:
        service (str): Service of crawler class to create.
        resource (str): Resource of crawler class to create.

    Return:
        Tuple of new metadata classes

    Raises:
        InvalidServiceDefinitionError: invalid service definition found.
    """

    logger.trace('Collecting %s.%s metadata class attributes', service, resource)  # type: ignore

    # length of 0 means schema definition is empty
    if len(class_definition) == 0:
        raise InvalidServiceDefinitionError(
            f'Bad metadata definition found for {service}.{resource}'
        )

    metaclasses: tuple[GenericMetadata, ...] = tuple(
        _create_crawler_metadata_classes(  # type: ignore[arg-type]
            class_name=f'{service}_{resource}', class_definition=class_definition
        )
    )

    return metaclasses


def apply_external_evaluations(evaluations: list[str]) -> None:
    """Apply external evaluations to crawlers.

    Takes provide external evalutions module, determines target service and
    resource, extracts evalution functions, and applies to target web crawlers.
    """

    external_evalutations: dict[str, Any] = {}

    for path in evaluations:
        try:
            external_evalutations = _merge_dictionaries(
                external_evalutations, _import_external_evaluations(path)
            )
        except (
            EvaluationModuleNotFoundError,
            EvaluationModuleFailedToLoadError,
        ) as err:
            logger.warning(err)

    for service in [
        f'{MODULE_NAME}.service.{service}.{resource}'
        for service, resources in external_evalutations.items()
        for resource in resources
    ]:
        for crawler in import_crawlers(path=service):
            try:
                external_evaluation_includes: list[str] = list(
                    external_evalutations[crawler.serviceType][
                        crawler.resourceName
                    ].pop('include')
                )
                external_evaluation_functions: dict[
                    str, FunctionType
                ] = external_evalutations[crawler.serviceType][crawler.resourceName]
                # build new includes list

                logger.debug(
                    'Applying external evaluation methods to %s.',
                    type(crawler).__name__,
                )
                # set new crawler includes
                crawler.INCLUDE.update(external_evaluation_includes)

                for name, func in external_evaluation_functions.items():
                    # ensure evalution is not override original attributes
                    if getattr(GenericCrawler, name, False):
                        raise EvaluationMethodNameError(
                            f'Evaluation {name} invalid. {type(GenericCrawler)}.{name} cannot be overwritten.'
                        )
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


@no_type_check  # mypy doesn't handle complex recursion well.
def _create_crawler_metadata_classes(
    class_name: str,
    class_definition: dict[str, Any] | list[Any] | Any,
    collection: list[type] | None = None,
    _depth: int = 0,
) -> list[GenericMetadata] | tuple[Any, list[GenericMetadata]]:
    """Create metadata classes.

    Dynamically create metadata class, and associated subclasses for provided service and resource
    parameters.

    Args:
        class_name (str): Name for new metadata class.
        class_definition (dict): data structure containing class attribute key/values.
        data (dict): Resource of crawler class to create.
        collection (list): Used for recursive creation of all metadata classes.
        _depth (int): Used for recursion depth tracking.

    Return:
        Tuple of new metadata classes
    """

    collection: list[GenericMetadata] = collection or []

    # standard recursive dict structure to allow creation all layers of metadata class
    if isinstance(class_definition, list):
        for i in class_definition:
            _, collection = _create_crawler_metadata_classes(
                class_name, i, collection, _depth=_depth + 1
            )
        return (list, collection)
    elif isinstance(class_definition, dict):
        for k, v in class_definition.items():  # pylint: disable=invalid-name
            attr, collection = _create_crawler_metadata_classes(
                f'{class_name}_{k}', v, collection, _depth=_depth + 1
            )
            class_definition[k] = attr
        metadata_class = _resource_crawler_metadata_class_factory(
            class_name=class_name,
            class_scheme=class_definition,
        )
        collection.append(metadata_class)
        if not _depth:
            return collection
        return (metadata_class, collection)
    else:
        return (class_definition, collection)


def _resource_crawler_class_factory(
    service_path: str, class_name: str, class_definition: dict[str, Any]
) -> GenericCrawler:
    """Class factory for web crawler class.

    Collects class components from module at provided path and creates a new type
    of type `GenericCrawler` with name provides and definition provided, along with
    components gathered from module import.

    Args:
        service_path (str): path of module where methods are located
        class_name (str): Name for new metadata class.
        class_definition (dict): data structure containing class attribute key/values

    Return:
        New class.
    """

    # get custom paginator from service module if it exists
    parent_module = importlib.import_module(service_path)
    class_paginator: dict[str, type] = {
        'custom_paginator': obj
        for _, obj in getmembers(parent_module)
        if isclass(obj)
        and obj.__name__
        == (f'{_serialize_class_name(class_definition["resourceName"])}Paginator')
    }

    if class_paginator:
        logger.trace('Custom paginator %s found.', class_paginator['custom_paginator'])  # type: ignore

    class_name = _serialize_class_name(class_name)

    logger.trace('Generating crawler class "%s".', class_name)  # type: ignore
    return type(  # type: ignore
        class_name,
        (GenericCrawler,),
        {**class_definition, **class_paginator},
    )


def _resource_crawler_metadata_class_factory(
    class_name: str, class_scheme: dict[str, Any]
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

    class_name = _serialize_class_name(f'{class_name}_metadata')
    class_fields: list[tuple[str, type, Any]] = []

    # Transform class definition to dataclass definition
    for f_name, f_type in class_scheme.items():
        if f_type is list:
            class_fields.append((f_name, f_type, field(default_factory=tuple)))
        elif f_type in (int, float):
            class_fields.append((f_name, f_type, field(default=0)))
        elif f_type is str:
            class_fields.append((f_name, f_type, field(default='')))
        elif f_type is bool:
            class_fields.append((f_name, f_type, field(default=False)))
        elif is_dataclass(f_type):
            class_fields.append((f_name, type(f_type), field(default_factory=f_type)))

    logger.trace('Generating metadata class "%s".', class_name)  # type: ignore
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
        EvaluationModuleNotFoundError: Failed to retrieve evaluation data.
    """

    evaluations: dict[str, Any] = {}

    # try and import, either by path (if file), or as module (if directory)
    try:
        logger.debug('loading module from %s...', path)
        if os.path.isfile(path):
            spec = spec_from_file_location("external_evaluations", path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            sys.path.append(path)
            module = importlib.import_module(path)
    except ModuleNotFoundError as err:
        raise EvaluationModuleFailedToLoadError(
            f'Failed to load {path} -- {err}'
        ) from err
    except ImportError as err:
        raise EvaluationModuleNotFoundError(f'Could not load module {path}') from err

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
        logger.trace('External evaluation method %s found.', name)  # type: ignore
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


def _get_crawler_class(module: ModuleType) -> GenericCrawler:
    """Get web crawler class from module.

    Scans provided module and returns the `GenericCrawler` if found.

    Args:
        module (ModuleType): Module to scan.

    Return:
        GenericCrawler class or None.

    Raises:
        CrawlerNotFoundError: if class is not found.
    """
    try:
        return next(
            (
                obj  # type: ignore
                for _, obj in getmembers(module)
                if isclass(obj) and issubclass(obj, GenericCrawler)
            )
        )
    except StopIteration:
        raise CrawlerNotFoundError(
            f'Did not find a crawler class in {module}'
        ) from None


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
