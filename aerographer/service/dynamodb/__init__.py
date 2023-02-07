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

"""dynamodb service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_paginate
from aerographer.crawler import get_crawlers, deploy_crawlers
from aerographer.crawler.generic import GenericCustomPaginator


SERVICE_DEFINITION = {'globalService': False}


class TableIdPaginator(GenericCustomPaginator):
    """Paginator for TableId resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
        INCLUDE (set[str]): (class attribute) List of resource information the paginator is dependant on.
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
        INCLUDE (set[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE = {'dynamodb.table_id'}

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
        pages: list[dict[str, Any]] = []

        if not SURVEY['dynamodb']['table_id'].values():
            return tuple(pages)

        tables: list[str] = [
            i.id
            for i in SURVEY['dynamodb']['table_id'].values()
            if i.context == self.context
        ]

        ## return a single page with multiple results
        new_page: dict[str, list[dict[str, str]]] = {'Table': []}

        results = await async_paginate(
            self.paginator, id_key='TableName', id_values=tables, **kwargs
        )

        for result in results:
            for page in result:
                new_page['Table'].append(page['Table'])

        pages.append(new_page)

        return tuple(pages)
