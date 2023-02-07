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

"""ec2 service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan.parallel import async_paginate
from aerographer.crawler.generic import GenericCustomPaginator


SERVICE_DEFINITION = {'globalService': False}


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
