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

"""route53 service.

Contains any customer paginators for service.
"""

from typing import Any
from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_paginate
from aerographer.crawler import get_crawlers, deploy_crawlers
from aerographer.crawler.generic import GenericCustomPaginator


SERVICE_DEFINITION = {'globalService': True}


class RecordSetPaginator(GenericCustomPaginator):
    """Paginator for Record Set resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
        INCLUDE (set[str]): (class attribute) List of resource information the paginator is dependant on.
        context (CONTEXT): Which context to use for retrieving data.
        paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
        paginate(**kwargs): Retrieve data.
    """

    INCLUDE = {'route53.hosted_zone'}

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
        zones: list[str] = [
            i.id
            for i in SURVEY['route53']['hosted_zone'].values()
            if i.context == self.context
        ]

        ## return a single page with multiple results
        pages: list[dict[str, Any]] = []
        page: dict[str, list[dict[str, str]]] = {'ResourceRecordSets': []}

        page_results: dict[str, list[dict[str, Any]]] = dict(
            zip(
                zones,
                await async_paginate(
                    self.paginator, id_key='HostedZoneId', id_values=zones, **kwargs
                ),
            )
        )

        for zone_id, results in page_results.items():
            for result in results:
                for record in result['ResourceRecordSets']:
                    record_id = f"{zone_id.split('/')[2]}:{record['Name'].rstrip('.')}:{record['Type']}"
                    if 'SetIdentifier' in record:
                        record_id += f':{record["SetIdentifier"]}'
                    page['ResourceRecordSets'].append(
                        record | {'HostedZoneId': zone_id, 'Id': record_id}
                    )
        pages.append(page)

        return tuple(pages)
