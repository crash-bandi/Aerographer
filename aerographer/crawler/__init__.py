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
with the aerographer module.

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

import sys
import gc
import asyncio
from datetime import datetime
from typing import Any

from botocore.exceptions import ClientError  # type: ignore

from aerographer.scan import build_contexts, scan_results
from aerographer.survey import SURVEY, Survey
from aerographer.scan.parallel import async_scan
from aerographer.crawler.factories import apply_external_evaluations, import_crawlers
from aerographer.crawler.generic import GenericCrawler
from aerographer.logger import logger
from aerographer.config import PROFILES, ROLES, REGIONS, MODULE_NAME
from aerographer.exceptions import (
    CrawlerNotFoundError,
    FailedCrawlerScanError,
)


def get_crawlers(
    services: set[str],
    skip: list[str] | None = None,
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
    skip = skip or []

    # format services and skip names properly to further use
    services = set(
        f'{MODULE_NAME}.service.{service}'
        if not service.startswith(f'{MODULE_NAME}.service')
        else service
        for service in services
    )

    skip = [
        f'{MODULE_NAME}.service.{s}'
        if not s.startswith('{MODULE_NAME}.service.')
        else s
        for s in skip
    ]

    # return crawlers from service paths
    try:
        return sum(
            [import_crawlers(service, skip, quiet_skip) for service in services], []
        )
    except CrawlerNotFoundError as err:
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
    includes = set()
    for crawler in crawlers:
        includes.update(crawler.INCLUDE)
    include_crawlers = [
        crawler
        for crawler in get_crawlers(services=includes, skip=provided, quiet_skip=True)
        if crawlers and crawler.state == 'initialized'
    ]

    # recursively get include crawlers until empty list is returned, meaning all have been retrieved.
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
        FailedCrawlerScanError: web crawler scan failed
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
        raise FailedCrawlerScanError(err) from err


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
        parameters (list[dict]): (optional) List of paramter options to use for scan.
        crawlers (GenericCrawler): (class attribute) Collection of web crawlers to use.

    Methods:
        scan(self): Trigger scan of targets.
    """

    def __init__(
        self,
        services: str | list[str] | None = None,  # safe default for list
        skip: str | list[str] | None = None,  # safe default for list
        profiles: list[str] | None = None,  # safe default for list
        roles: list[str] | None = None,  # safe default for list
        regions: list[str] | None = None,  # safe default for list
        evaluations: list[str] | None = None,  # safe default for list
        parameters: list[dict[str, dict]] | None = None,
    ) -> None:
        """Class initializer."""

        if isinstance(services, str):
            self.services = [services]
        else:
            self.services = services or [f'{MODULE_NAME}.service']

        if isinstance(skip, str):
            self.skip = [skip]
        else:
            self.skip = skip or []

        self.profiles = profiles or PROFILES
        self.roles = roles or ROLES
        self.regions = regions or REGIONS
        self.parameters = parameters or []

        # apply provided external evaluations to web crawlers
        apply_external_evaluations(evaluations or [])

        # initialize and get web crawlers
        try:
            # import service module to initialize crawler classes
            import aerographer.service

            logger.debug('Gathering crawlers for %s', ', '.join(self.services))
            self.crawlers = get_crawlers(set(self.services), self.skip)
            if self.crawlers is None:
                logger.error('No crawlers found for %s', self.services)
                sys.exit(1)
        except CrawlerNotFoundError as err:
            logger.error('Error getting crawlers for %s -- %s', self.services, err)
            sys.exit(1)

        # TODO: add to README
        # set provided scan parameters
        for k, v in (
            (k, v) for parameter in self.parameters for k, v in parameter.items()
        ):
            service, resource = k.split('.')
            crawler = next(
                (
                    crawler
                    for crawler in self.crawlers
                    if crawler.serviceType.lower() == service
                    and crawler.resourceName == resource
                ),
                None,
            )
            if crawler:
                crawler.scanParameters = v

        # initialize contexts
        self.accounts = [
            {'profile': profile, 'regions': self.regions, 'role': role}
            for profile in self.profiles
            for role in self.roles
        ]

    def scan(self) -> Survey:
        """Performs scan and evaluations of all web crawlers.

        Triggers each web crawler to scan target resource and perform any
        present evaluations. Forces garabage cleanup to after scan as scan
        can consume a lot of memory.

        Return:
            Dictionary containing all class instances created by scan.
        """

        logger.info("Building scan sessions...")
        start = datetime.now()
        build_contexts(
            self.accounts,
            services=set([crawler.serviceType for crawler in self.crawlers]),
        )
        logger.trace(  # type: ignore
            'Session initialization time: %s', datetime.now() - start
        )

        try:
            # run scan and force GC
            start = datetime.now()
            asyncio.run(deploy_crawlers(crawlers=self.crawlers))
            logger.trace('Scan time: %s', datetime.now() - start)  # type:ignore
            gc.collect()
        except FailedCrawlerScanError as err:
            logger.error('Scan failed -- %s', err)
            sys.exit(1)

        # build new dictionary that only contains class instances included in targeted scans
        # this is so instances created to fulfill dependancy scan requirements are not returned
        RETURN_COLLECTION: dict[str, Any] = {}  # pylint: disable=invalid-name

        # TODO: this needs rework as it does not strip unrequested resources from return collection. use kms.key_rotation to observe.
        for crawler in self.crawlers:
            if crawler.serviceType not in RETURN_COLLECTION:
                RETURN_COLLECTION[crawler.serviceType] = {}

            RETURN_COLLECTION[crawler.serviceType][crawler.resourceName] = scan_results[
                crawler.serviceType
            ][crawler.resourceName]

            for resource in RETURN_COLLECTION[crawler.serviceType][
                crawler.resourceName
            ].values():
                resource.run_evaluations()

        for service, resources in RETURN_COLLECTION.items():
            SURVEY._add_service(service=service)
            for resource, assets in resources.items():
                s = SURVEY.get_service(service)
                s._add_resource_type(resource_type=resource)
                r = s.get_resource_type(resource_type=resource)
                for asset in assets.values():
                    r._add_resource(asset)

        SURVEY._publish()
        return SURVEY
