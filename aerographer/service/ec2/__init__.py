"""ec2 service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan.parallel import async_paginate
from aerographer.crawler.generic import GenericCustomPaginator


class InstancePaginator(GenericCustomPaginator):
    """Paginator for instance resource.

    Custom paginator used to retrieve resource information from AWS.


    Attributes:
        INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    async def paginate(self, **kwargs: Any) -> tuple[dict[str, Any], ...]:
        """Retrieves pages of resource data.

        Retrieves list of pages for resource data.

        Args:
            **kwargs: any arguements supported by function provided through paginate_func_name

        Returns:
            An iterable object. Iterating over this object will yield a single page of a
            response at a time.
        """

        pages: list[Any] = []

        results = await async_paginate(paginator=self.paginator, **kwargs)

        for result in results:
            for page in result:
                for reservation in page['Reservations']:
                    pages.append(reservation)

        return tuple(pages)
