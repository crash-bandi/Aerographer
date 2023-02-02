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

"""iam service.

Contains any customer paginators for service.
"""

from typing import Any
import json
import asyncio

from aerographer.scan import SURVEY
from aerographer.scan.parallel import async_paginate
from aerographer.crawler import get_crawlers, deploy_crawlers
from aerographer.crawler.generic import GenericCustomPaginator


class RolePaginator(GenericCustomPaginator):
    """Paginator for Role resource.

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

        # list_roles is missing RoleLastUsed attribute, so get_role is required to get data
        pages: list[dict[str, Any]] = []
        new_page: dict[str, list[dict[str, str]]] = {'Roles': []}
        roles: list[str] = []

        # get list of role names
        for result in await async_paginate(paginator=self.paginator, **kwargs):
            for page in result:
                for role in page['Roles']:
                    roles.append(role['RoleName'])

        # get_role for each role name
        role_results = await async_paginate(
            paginator=GenericCustomPaginator(
                context=self.context, paginator_func_name='get_role', page_marker=None
            ).paginator,
            id_key='RoleName',
            id_values=roles,
            **kwargs,
        )

        # convert AssumeRolePolicyDocument attribute from dict to string
        for result in role_results:
            for role in result:
                role['Role']['AssumeRolePolicyDocument'] = json.dumps(
                    role['Role']['AssumeRolePolicyDocument']
                )
                new_page['Roles'].append(role['Role'])

        pages.append(new_page)

        return tuple(pages)


class RolePolicyIdPaginator(GenericCustomPaginator):
    """Paginator for Role Policy Id resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
       INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
       context (CONTEXT): Which context to use for retrieving data.
       paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
       paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['iam.role']

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
        roles: list[str] = [
            i.id for i in SURVEY['iam']['role'].values() if i.context == self.context
        ]

        pages: list[dict[str, Any]] = []

        results = dict(
            zip(
                roles,
                await async_paginate(
                    paginator=self.paginator,
                    id_key='RoleName',
                    id_values=roles,
                    **kwargs,
                ),
            )
        )

        for role_name, page_results in results.items():
            for result in page_results:
                page: dict[str, list[dict[str, str]]] = {'PolicyNames': []}
                for policy in result['PolicyNames']:
                    page['PolicyNames'].append(
                        {'RoleName': role_name, 'PolicyName': policy}
                    )
                pages.append(page)

        return tuple(pages)


class RolePolicyPaginator(GenericCustomPaginator):
    """Paginator for Role Policy resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
       INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
       context (CONTEXT): Which context to use for retrieving data.
       paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
       paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['iam.role_policy_id']

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
        role_and_policy_names: list[dict[str, str]] = [
            {
                policy.data.RoleName: policy.id  # type:ignore
            }
            for policy in SURVEY['iam']['role_policy_id'].values()
            if policy.context == self.context
        ]

        pages: list[dict[str, Any]] = []
        new_page: dict[str, list[dict[str, Any]]] = {'RolePolicies': []}

        results = await asyncio.gather(
            *[
                async_paginate(
                    paginator=self.paginator,
                    **{
                        'RoleName': role_name,
                        'PolicyName': policy_name,
                    },
                    **kwargs,
                )
                for pair in role_and_policy_names
                for role_name, policy_name in pair.items()
            ]
        )

        for result in results:
            for page in result:
                for policy in page:
                    policy['PolicyDocument'] = json.dumps(policy['PolicyDocument'])
                    del policy['ResponseMetadata']
                    new_page['RolePolicies'].append(policy)

        pages.append(new_page)
        return tuple(pages)


class RoleAttachedPolicyPaginator(GenericCustomPaginator):
    """Paginator for Role Attached Policy resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
       INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
       context (CONTEXT): Which context to use for retrieving data.
       paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
       paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['iam.role']

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
        roles: list[str] = [
            role.id
            for role in SURVEY['iam']['role'].values()
            if role.context == self.context
        ]

        pages: list[dict[str, Any]] = []

        results = dict(
            zip(
                roles,
                await async_paginate(
                    paginator=self.paginator,
                    id_key='RoleName',
                    id_values=roles,
                    **kwargs,
                ),
            )
        )

        for role_name, page_result in results.items():
            for page in page_result:
                for policy in page['AttachedPolicies']:
                    policy['RoleName'] = role_name
                pages.append(page)

        return tuple(pages)


class PolicyDocumentPaginator(GenericCustomPaginator):
    """Paginator for Policy Document resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
       INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
       context (CONTEXT): Which context to use for retrieving data.
       paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
       paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['iam.policy']

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
        policies: list[dict[str, str]] = [
            {
                'id': i.id,
                'version_id': i.data.DefaultVersionId,  # type:ignore
                'arn': i.data.Arn,  # type:ignore
            }
            for i in SURVEY['iam']['policy'].values()
            if i.context == self.context
        ]

        pages: list[dict[str, Any]] = []
        page: dict[str, list[dict[str, str]]] = {'PolicyDocuments': []}

        results: dict[str, list[list[dict[str, Any]]]] = dict(
            zip(
                [policy['id'] for policy in policies],
                (
                    await asyncio.gather(
                        *[
                            async_paginate(
                                paginator=self.paginator,
                                **{
                                    'PolicyArn': policy['arn'],
                                    'VersionId': policy['version_id'],  # type:ignore
                                },
                                **kwargs,
                            )
                            for policy in policies
                        ]
                    )
                ),
            )
        )

        for policy_id, page_results in results.items():
            for result in page_results:
                for document in result:
                    document['PolicyVersion']['Document'] = json.dumps(
                        document['PolicyVersion']['Document']
                    )
                    page['PolicyDocuments'].append(
                        {'PolicyName': policy_id, **document['PolicyVersion']}
                    )

        pages.append(page)

        return tuple(pages)


class ManagedPolicyDocumentPaginator(GenericCustomPaginator):
    """Paginator for AWS managed Policy Document resource.

    Custom paginator used to retrieve resource information from AWS.

    Attributes:
       INCLUDE (list[str]): (class attribute) List of resource information the paginator is dependant on.
       context (CONTEXT): Which context to use for retrieving data.
       paginate_func_name (str): Name of the boto3 function used to retrieve data.

    Methods:
       paginate(**kwargs): Retrieve data.
    """

    INCLUDE = ['iam.managed_policy']

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
        policies: list[dict[str, str]] = [
            {
                'id': i.id,
                'version_id': i.data.DefaultVersionId,  # type:ignore
                'arn': i.data.Arn,  # type:ignore
            }
            for i in SURVEY['iam']['managed_policy'].values()
            if i.context == self.context
        ]

        pages: list[dict[str, Any]] = []
        page: dict[str, list[dict[str, str]]] = {'PolicyDocuments': []}

        results: dict[str, list[list[dict[str, Any]]]] = dict(
            zip(
                [policy['id'] for policy in policies],
                (
                    await asyncio.gather(
                        *[
                            async_paginate(
                                paginator=self.paginator,
                                **{
                                    'PolicyArn': policy['arn'],
                                    'VersionId': policy['version_id'],  # type:ignore
                                },
                                **kwargs,
                            )
                            for policy in policies
                        ]
                    )
                ),
            )
        )

        for policy_id, page_results in results.items():
            for result in page_results:
                for document in result:
                    document['PolicyVersion']['Document'] = json.dumps(
                        document['PolicyVersion']['Document']
                    )
                    page['PolicyDocuments'].append(
                        {'PolicyName': policy_id, **document['PolicyVersion']}
                    )

        pages.append(page)

        return tuple(pages)
