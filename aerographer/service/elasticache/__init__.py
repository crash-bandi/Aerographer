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
