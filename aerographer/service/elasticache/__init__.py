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

"""elasticache service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_paginate
from aerographer.crawler import get_crawlers, deploy_crawlers
from aerographer.crawler.generic import GenericCustomPaginator


class ReplicationGroupTagPaginator(GenericCustomPaginator):
    """Paginator for replication group tag resource.

    Custom paginator used to retrieve resource information from AWS.


    Attributes:
        INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['elasticache.replication_group']

    async def paginate(self, **kwargs: Any) -> tuple[dict[str, Any], ...]:
        """Retrieves pages of resource data.

        Retrieves list of pages for resource data.

        Args:
            **kwargs: any arguements supported by function provided through paginate_func_name

        Returns:
            An iterable object.  Iterating over
            this object will yield a single page of a response
            at a time.
        """

        await deploy_crawlers(get_crawlers(services=self.INCLUDE))
        replication_groups: list[str] = [
            i.data.ARN
            for i in SURVEY['elasticache']['replication_group'].values()
            if i.context == self.context
        ]

        pages: list[dict[str, Any]] = []

        results = dict(
            zip(
                replication_groups,
                await async_paginate(
                    paginator=self.paginator,
                    id_key='ResourceName',
                    id_values=replication_groups,
                    **kwargs
                ),
            )
        )

        for group, result in results.items():
            for page in result:
                for tag in page['TagList']:
                    tag['ReplicationGroupId'] = group
                pages.append(page)

        return tuple(pages)
