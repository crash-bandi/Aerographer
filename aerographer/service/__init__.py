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

"""Contains components for web crawlers.

Contains custom paginators for web crawler classes.
Dynamically builds and attaches web crawler and
metadata classes on initialization. Not meant for
external use.
"""

from datetime import datetime
import pkgutil
import importlib
import gc

from aerographer.crawler.factories import (
    initialize_crawler,
    initialize_crawler_metadata,
)
from aerographer.logger import logger
from aerographer.exceptions import InvalidServiceDefinitionsExceptionError

start = datetime.now()
for _, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + '.'):
    if is_pkg:
        module = importlib.import_module(module_name)
        try:
            service_definition = getattr(module, 'SERVICE_DEFINITION')
        except AttributeError:
            raise InvalidServiceDefinitionsExceptionError(
                f'No service definition found for {module_name}'
            ) from None
    else:
        logger.debug('Initializing module %s...', module_name)  # type: ignore
        sub_module = importlib.import_module(module_name)
        try:
            resource_definition = getattr(sub_module, 'RESOURCE_DEFINITION')
        except AttributeError:
            raise InvalidServiceDefinitionsExceptionError(
                f'No resource definition found for {module_name}'
            ) from None

        try:
            metadata_definition = resource_definition['responseSchema']
        except KeyError:
            raise InvalidServiceDefinitionsExceptionError(
                f'No "responseSchema" definition found for {module_name}'
            ) from None

        _, _, service, resource = sub_module.__name__.split('.')  # type: ignore
        CrawlerClass = initialize_crawler(
            service=service,
            resource=resource,
            class_definition=service_definition | resource_definition,
        )
        CrawlerMetadataClasses = initialize_crawler_metadata(
            service=service, resource=resource, class_definition=metadata_definition
        )
        if CrawlerClass and CrawlerMetadataClasses:
            for MetadataClass in CrawlerMetadataClasses:
                setattr(CrawlerClass, MetadataClass.__name__, MetadataClass)  # type: ignore
            setattr(sub_module, CrawlerClass.__name__, CrawlerClass)  # type: ignore

logger.trace('Class initialization time: %s', datetime.now() - start)  # type:ignore
gc.collect()
