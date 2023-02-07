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

"""kms service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_paginate
from aerographer.crawler import get_crawlers, deploy_crawlers
from aerographer.crawler.generic import GenericCustomPaginator


SERVICE_DEFINITION = {'globalService': False}


class KeyPaginator(GenericCustomPaginator):
    """Paginator for KeyMetadata resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
        INCLUDE (set[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE = {'kms.key_id'}

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
        keys: list[str] = [
            i.id for i in SURVEY['kms']['key_id'].values() if i.context == self.context
        ]

        ## return a single page with multiple results
        pages: list[dict[str, Any]] = []
        page: dict[str, list[dict[str, str]]] = {'KeyMetadata': []}

        for results in await async_paginate(
            self.paginator, id_key='KeyId', id_values=keys, **kwargs
        ):
            for result in results:
                page['KeyMetadata'].append(result['KeyMetadata'])
        pages.append(page)

        return tuple(pages)


class KeyRotationPaginator(GenericCustomPaginator):
    """Paginator for KeyRotation resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
       INCLUDE (set[str]): (class attribute) List of resource information the paginator is dependant on.
       context (CONTEXT): Which context to use for retrieving data.
       paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
       paginate(**kwargs): Retrieve data.
    """

    INCLUDE = {'kms.key'}

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

        if not SURVEY['kms']['key'].values():
            return tuple(pages)

        keys: list[str] = [
            i.id
            for i in SURVEY['kms']['key'].values()
            if i.context == self.context
            and i.KeyManager == 'CUSTOMER'  # type:ignore
            and i.Origin == 'AWS_KMS'  # type:ignore
        ]

        ## return a single page with multiple results
        page: dict[str, list[dict[str, str]]] = {"KeyRotation": []}

        pager_results = dict(
            zip(
                keys,
                await async_paginate(
                    self.paginator, id_key='KeyId', id_values=keys, **kwargs
                ),
            )
        )

        for key, results in pager_results.items():
            for result in results:
                page["KeyRotation"].append(
                    {'KeyId': key, 'KeyRotationEnabled': result['KeyRotationEnabled']}
                )
        pages.append(page)

        return tuple(pages)
