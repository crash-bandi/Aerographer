"""elbv2 service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_paginate
from aerographer.crawler import get_crawlers, deploy_crawlers
from aerographer.crawler.generic import GenericCustomPaginator


class TagPaginator(GenericCustomPaginator):
    """Paginator for tag resource.

    Custom paginator used to retrieve resource information from AWS.


    Attributes:
        INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['elbv2.load_balancer']

    async def paginate(self, **kwargs: Any) -> tuple[dict[str, Any], ...]:
        """Retrieves pages of resource data.

        Retrieves list of pages for resource data.

        Args:
            **kwargs: any arguements supported by function provided through paginate_func_name

        Returns:
            An iterable object. Iterating over this object will yield a single page of a
            response at a time.
        """

        await deploy_crawlers(get_crawlers(services=self.INCLUDE))
        load_balancers: list[str] = [
            i.data.LoadBalancerArn  # type: ignore
            for i in SURVEY['elbv2']['load_balancer'].values()
            if i.context == self.context
        ]

        chunks = [load_balancers[x : x + 20] for x in range(0, len(load_balancers), 20)]
        pages: list[dict[str, Any]] = []

        results = await async_paginate(
            paginator=self.paginator, id_key='ResourceArns', id_values=chunks, **kwargs
        )

        for result in results:
            for page in result:
                pages.append(page)

        return tuple(pages)
