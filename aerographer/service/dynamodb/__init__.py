"""dynamodb service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_paginate
from aerographer.crawler import get_crawlers, deploy_crawlers
from aerographer.crawler.generic import GenericCustomPaginator


class TableIdPaginator(GenericCustomPaginator):
    """Paginator for TableId resource.

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
                page_new: dict[str, list[dict[str, str]]] = {}
                page_new["TableNames"] = [{"TableId": r} for r in page["TableNames"]]
                pages.append(page_new)

        return tuple(pages)


class TablePaginator(GenericCustomPaginator):
    """Paginator for Table resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
        INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['dynamodb.table_id']

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
        tables: list[str] = [
            i.id
            for i in SURVEY['dynamodb']['table_id'].values()
            if i.context == self.context
        ]

        ## return a single page with multiple results
        pages: list[dict[str, Any]] = []
        new_page: dict[str, list[dict[str, str]]] = {'Table': []}

        results = await async_paginate(
            self.paginator, id_key='TableName', id_values=tables, **kwargs
        )

        for result in results:
            for page in result:
                new_page['Table'].append(page['Table'])

        pages.append(new_page)

        return tuple(pages)
