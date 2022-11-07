"""Contains components for web crawlers.

Contains custom paginators for web crawler classes.
Dynamically builds and attaches web crawler and
metadata classes on initialization. Not meant for
external use.
"""

import pkgutil
import importlib
import gc

from aerographer.crawler import initialize_crawler, initialize_crawler_metadata
from aerographer.logger import logger

for _, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + '.'):
    if not is_pkg:
        logger.trace('Initializing module %s...', module_name)  # type: ignore
        sub_module = importlib.import_module(module_name)

        _, _, service, resource = sub_module.__name__.split('.')  # type: ignore
        CrawlerClass = initialize_crawler(service=service, resource=resource)
        CrawlerMetadataClasses = initialize_crawler_metadata(
            service=service, resource=resource
        )
        if CrawlerClass and CrawlerMetadataClasses:
            for MetadataClass in CrawlerMetadataClasses:
                setattr(CrawlerClass, MetadataClass.__name__, MetadataClass)
            setattr(sub_module, CrawlerClass.__name__, CrawlerClass)  # type: ignore

gc.collect()
