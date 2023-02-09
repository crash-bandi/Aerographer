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

from __future__ import annotations

"""Contains components for Survey class.

Contains the `Survey` class, which is the component used to interact
with scan results.

    Typical usage example:

    from aerographer.survey import SURVEY
    SURVEY.get_resources()
    SURVEY.get_service('ec2').get_resource('example')
    SURVEY.ec2.security_group.get_resources()
"""

import string
import re
import itertools
from typing import Any, Iterable, Callable, Generator
from collections.abc import Generator

from aerographer.crawler.generic import GenericCrawler
from aerographer.exceptions import (
    FrozenInstanceError,
    SurveyAttributeError,
    SurveySearchQueryError,
)

chars = re.escape(string.punctuation)


def _serialize_resource_id(resource_id: str) -> str:
    """Get serialized resource id.

    Returns a serialize resource id where all puncuation is convered to an underscore ( _ ).

    Args:
        resource_id (str): Id to serialize.

    Return:
        Serialized id string.
    """
    return re.sub('[' + chars + ']', '_', resource_id)


def _flatten(l: list[list[Any]]) -> list[Any]:
    """Flatten list.

    Flattens provided list of lists.

    Args:
        l (list[Any]): List to flatten.

    Return:
        Flattened list.
    """
    return list(itertools.chain.from_iterable(l))


def _get_obj_attr(o: type, path: str) -> list[Any]:
    """Get attribute values at provided path.

    Recursively traverses provided object and returns a list of all values at provided path.

    Args:
        o (type): Object to search.
        path (str): Path to attribute to retrieve.

    Return:
        List of found values.

    Raises:
        SurveySearchQueryError: Path traversing error encountered.
    """
    try:
        if '.' in path:
            key, rest = path.split('.', 1)
            if key.isdigit() and isinstance(o, (list, tuple)):
                return _get_obj_attr(o[int(key)], rest)
            elif key == "*" and isinstance(o, (list, tuple)):
                return _flatten([_get_obj_attr(i, rest) for i in o])
            else:
                return _get_obj_attr(getattr(o, key), rest)
        else:
            if path.isdigit() and isinstance(o, (list, tuple)):
                return [o[int(path)]]
            elif path == '*' and isinstance(o, (list, tuple)):
                return list(o)
            else:
                return [getattr(o, path)]
    except (KeyError, IndexError, TypeError, AttributeError):
        raise SurveySearchQueryError(f'Invalid search string: {path}') from None


def _eq(val: Any, matches: list[Any]) -> bool:
    """Check if value is equal to any in provided list.

    Returns `True` if value equals any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.
    """
    return val in matches


def _ne(val: Any, matches: list[Any]) -> bool:
    """Check if value is not equal to any in provided list.

    Returns `True` if value does not equal any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.
    """
    return val not in matches


def _gt(val: Any, matches: list[Any]) -> bool:
    """Check if value is greater than to any in provided list.

    Returns `True` if value is greather than any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.

    Raises:
        ValueError: value error encounted.
    """
    try:
        return any(val > match for match in matches)
    except ValueError:
        return False


def _lt(val: Any, matches: list[Any]) -> bool:
    """Check if value is less than to any in provided list.

    Returns `True` if value is less than any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.

    Raises:
        ValueError: value error encounted.
    """
    try:
        return any(val < match for match in matches)
    except ValueError:
        return False


def _contains(val: Any, matches: list[Any]) -> bool:
    """Check if value contains any in provided list.

    Returns `True` if value contains any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.
    """
    return any(match in val for match in matches)


def _not_contains(val: Any, matches: list[Any]) -> bool:
    """Check if value not contains to any in provided list.

    Returns `True` if value does not contain any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.
    """
    return any(match not in val for match in matches)


def _startswith(val: Any, matches: list[Any]) -> bool:
    """Check if value starts with to any in provided list.

    Returns `True` if value starts with any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.
    """
    return any(val.startswith(match) for match in matches)


def _endswith(val: Any, matches: list[Any]) -> bool:
    """Check if value ends with to any in provided list.

    Returns `True` if value ends with any items in provided list.

    Args:
        val (Any): Value to check.
        matches (list[Any]): Values to check against.

    Return:
        Bool of comparision results.
    """
    return any(val.endswith(match) for match in matches)


class Freezable:
    """Provides ability to freeze child classes.

    Provides the ability to convert a child class into read-only.


    Attributes:
        _frozen (bool): Frozen state of class.
        _id (str): (optional) Friendly class name. Default: ''

    Methods:
        _freeze(self): Converts class to read-only.
    """

    _frozen: bool = False
    _id: str = ''

    def _freeze(self) -> None:
        """Freeze class."""
        self._frozen = True

    def __delattr__(self, __key: str) -> None:
        if self._frozen:
            raise FrozenInstanceError(f"cannot delete field '{__key}'")
        object.__delattr__(self, __key)

    def __setattr__(self, __key: str, __val: Any) -> None:
        if self._frozen:
            raise FrozenInstanceError(f"cannot assign to field '{__key}'")
        object.__setattr__(self, __key, __val)

    def __repr__(self) -> str:
        return f'{self.__class__}({self._id})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self._id})'


class SurveySearch(Generator):
    """Provides ability to freeze child classes.

    Provides the ability to convert a child class into read-only.

    Methods:
        where(self, attribute: str, condition: str, values: list[Any]): Return SurveySearch containing list where condition is true.
        where_not(self, attribute: str, condition: str, values: list[Any]): Return SurveySearch containing list where condition is false.
    """

    _checks: dict[str, Callable[[Any, list[Any]], bool]] = {
        'eq': _eq,
        'ne': _ne,
        'gt': _gt,
        'lt': _lt,
        'contains': _contains,
        'not_contains': _not_contains,
        'startswith': _startswith,
        'endswith': _endswith,
    }

    def __init__(self, iter: Iterable) -> None:
        self.__iter = iter

    def __iter__(self) -> Generator[GenericCrawler, None, None]:
        return super().__iter__()

    def send(self, *args, **kwargs) -> Any:
        """Default generator method. Not of external use."""
        return next(self.__iter)  # type: ignore[call-overload]

    def throw(self, *args, **kwargs) -> None:
        """Default generator method. Not of external use."""
        raise StopIteration

    def where(self, attribute: str, condition: str, values: list[Any]) -> SurveySearch:
        """Filter results where condition is true.

        Applies a filter to a `SurveySearch` where the confition provided is true.

        Provide a path to search the object for, a list of values, and a comparision methd.
        Path examples:
            'id'
            'components.1.description'
            'rules.*.enabled'

        Comparisions:
            eq: equal
            ne: not equal
            gt: greater than
            lt: less than
            contains: contains
            not_contains: does not contain
            startswith: starts with
            endswith: ends with

        Args:
            attribute (str): Value to check.
            condition: (str): Comparision to perform.
            values (list[Any]): Values to check against.

        Return:
            SurveySearch instance containing filtered results.
        """
        if condition not in self._checks:
            raise SurveySearchQueryError(f'Invalid search condition: {condition}')

        return SurveySearch(
            i
            for i in self.__iter
            if any(
                self._checks[condition](o, values) for o in _get_obj_attr(i, attribute)
            )
        )

    def where_not(
        self, attribute: str, condition: str, values: list[Any]
    ) -> SurveySearch:
        """Filter results where condition is false.

        Applies a filter to a `SurveySearch` where the confition provided is false.

        Provide a path to search the object for, a list of values, and a comparision methd.
        Path examples:
            'id'
            'components.1.description'
            'rules.*.enabled'

        Comparisions:
            eq: equal
            ne: not equal
            gt: greater than
            lt: less than
            contains: contains
            not_contains: does not contain
            startswith: starts with
            endswith: ends with

        Args:
            attribute (str): Value to check.
            condition: (str): Comparision to perform.
            values (list[Any]): Values to check against.

        Return:
            SurveySearch instance containing filtered results.
        """
        if condition not in self._checks:
            raise SurveySearchQueryError(f'Invalid search condition: {condition}')

        return SurveySearch(
            i
            for i in self.__iter
            if not any(
                self._checks[condition](o, values) for o in _get_obj_attr(i, attribute)
            )
        )


class SurveyResourceType(Freezable):
    """Contains scan objects of specific resource type.

    Contains all objects collected during scan of its respective resource type.

    Attribute:
        resources (list[str]): List of available resource id's.

    Methods:
        get_resource(self, resource: str): Get resource with provided id.
        get_resources(self): Get all resources.
    """

    def __init__(self, resource_type: str) -> None:
        self.resources: set[str] = set()
        self._id: str = resource_type

    def _add_resource(self, resource: GenericCrawler) -> None:
        """Add resource.

        Adds the provided resource to self.

        Args:
            resource (GenericCrawler): Resource to add.
        """
        self.resources.add(resource.id)
        self.__setattr__(_serialize_resource_id(resource.id), resource)

    def get_resource(self, resource: str) -> GenericCrawler:
        """Get single resource.

        Get the resource with the provided id.

        Args:
            resource (str): Resource id to get.

        Returns:
            Single resource.

        Raises:
            SurveyAttributeError: Request of invalid object made.
        """
        try:
            return getattr(self, _serialize_resource_id(resource))
        except AttributeError:
            raise SurveyAttributeError(
                f'Survey does not contain "{resource}" resource.'
            )

    def get_resources(self) -> SurveySearch:
        """Get all resources.

        Get all resources of resource type.

        Return:
            `SurveySearch` containing resources.
        """
        return SurveySearch(self.get_resource(resource) for resource in self.resources)

    def __contains__(self, __o: Any) -> bool:
        return any(__o == resource for resource in self.get_resources())


class SurveyService(Freezable):
    """Contains scan objects of specific service.

    Contains all objects collected during scan of its respective service.

    Attribute:
        resource_types (list[str]): List of available resource types.
        resources (list[str]): List of resource id's in resource type.

    Methods:
        get_resource_type(self, resource_type): Get resource type with provided id.
        get resource_types(self): Get all resource types.
        get_resource(self, resource: str): Get resource with provided id.
        get_resources(self): Get all resources.
    """

    def __init__(self, service: str) -> None:
        self.resource_types: set[str] = set()
        self._id: str = service

    @property
    def resources(self) -> set[str]:
        """Get all resources id's.

        Get all resource id's in service.

        Return:
            List containing resource id's.
        """
        resources: set[str] = set()
        for resource_type in self.get_resource_types():
            resources.update(resource_type.resources)
        return resources

    def _add_resource_type(self, resource_type: str) -> None:
        """Add resource type.

        Adds the provided resource type to self.

        Args:
            resource_type (str): Resource type to add.
        """
        self.resource_types.add(resource_type)
        self.__setattr__(resource_type, SurveyResourceType(resource_type))

    def get_resource_type(self, resource_type: str) -> SurveyResourceType:
        """Get single resource type.

        Get the resource type with the provided id.

        Args:
            resource_type (str): Resource type to get.

        Returns:
            Single resource type.

        Raises:
            SurveyAttributeError: Request of invalid object made.
        """
        try:
            return getattr(self, resource_type)
        except AttributeError:
            raise SurveyAttributeError(
                f'Survey does not contain "{resource_type}" resource type.'
            )

    def get_resource_types(self) -> Generator[SurveyResourceType, None, None]:
        """Get all resource types.

        Get all resource types of service.

        Return:
            List of resource types.
        """
        return SurveySearch(
            self.get_resource_type(resource) for resource in self.resource_types
        )

    def get_resources(self) -> SurveySearch:
        """Get all resources.

        Get all resources of service.

        Return:
            `SurveySearch` containing resources.
        """
        return SurveySearch(
            resource
            for resource_type in self.get_resource_types()
            for resource in resource_type.get_resources()
        )

    def get_resource(self, id: str) -> GenericCrawler:
        """Get single resource.

        Get the resource with the provided id.

        Args:
            resource (str): Resource id to get.

        Returns:
            Single resource.

        Raises:
            SurveyAttributeError: Request of invalid object made.
        """
        sid = _serialize_resource_id(id)
        for resource_type in self.get_resource_types():
            if sid in resource_type.resources:
                return resource_type.get_resource(sid)
        else:
            raise SurveyAttributeError(f'Survey does not contain "{id}" resource')

    def __contains__(self, __o: Any) -> bool:
        return any(__o == resource for resource in self.get_resources())


class Survey(Freezable):
    """Contains all scan objects.

    Contains all objects collected during scan.

    Attribute:
        services (list[str]): List of all available services.
        resource_types (list[str]): List of available resource types.
        resources (list[str]): List of resource id's in resource type.

    Methods:
        get_service(self, service): Get service with provided id.
        get_services(self): get all services.
        get_resource_type(self, resource_type): Get resource type with provided id.
        get resource_types(self): Get all resource types.
        get_resource(self, resource: str): Get resource with provided id.
        get_resources(self): Get all resources.

    Raises:
        SurveyAttributeError: Request of invalid object made.
    """

    def __init__(self) -> None:
        self.services: set[str] = set()
        self._id: str = ''

    @property
    def resources(self) -> set[str]:
        """Get all resources id's.

        Get all resource id's in survey.

        Return:
            List containing resource id's.
        """
        resources: set[str] = set()
        for resource_type in self.get_resource_types():
            resources.update(resource_type.resources)
        return resources

    @property
    def resources_types(self) -> set[str]:
        """Get all resources types.

        Get all resource types in survey.

        Return:
            List containing resource id's.
        """
        resources_types: set[str] = set()
        for service in self.get_services():
            resources_types.update(service.resource_types)
        return resources_types

    def _add_service(self, service: str) -> None:
        """Add service.

        Adds the provided service to self.

        Args:
            service (str): service to add.
        """
        self.services.add(service)
        self.__setattr__(service, SurveyService(service))

    def get_service(self, service: str) -> SurveyService:
        """Get single service.

        Get the service with the provided id.

        Args:
            service (str): service to get.

        Returns:
            Single service.

        Raises:
            SurveyAttributeError: Request of invalid object made.
        """
        try:
            return getattr(self, service)
        except AttributeError:
            raise SurveyAttributeError(f'Survey does not contain "{service}" service.')

    def get_services(self) -> Generator[SurveyService, None, None]:
        """Get all services.

        Get all service in survey.

        Return:
            List of services.
        """
        return SurveySearch(self.get_service(service) for service in self.services)

    def get_resource_types(self) -> Generator[SurveyResourceType, None, None]:
        """Get all resource types.

        Get all resource in survey.

        Return:
            List of resource types.
        """
        return (
            resource_type
            for service in self.get_services()
            for resource_type in service.get_resource_types()
        )

    def get_resource_type(self, resource_type: str) -> SurveyResourceType:
        """Get single resource type.

        Get the resource type with the provided id.

        Args:
            resource_type (str): Resource type to get.

        Returns:
            Single resource type.

        Raises:
            SurveyAttributeError: Request of invalid object made.
        """
        for service in self.get_services():
            if resource_type in service.resource_types:
                return service.get_resource_type(resource_type)
        else:
            raise SurveyAttributeError(f'Survey does not contain "{id}" resource type.')

    def get_resources(self) -> SurveySearch:
        """Get all resources.

        Get all resources in survey.

        Return:
            `SurveySearch` containing resources.
        """
        return SurveySearch(
            resource
            for resource_type in self.get_resource_types()
            for resource in resource_type.get_resources()
        )

    def get_resource(self, id: str) -> GenericCrawler:
        """Get single resource.

        Get the resource with the provided id.

        Args:
            resource (str): Resource id to get.

        Returns:
            Single resource.

        Raises:
            SurveyAttributeError: Request of invalid object made.
        """
        sid = _serialize_resource_id(id)
        for resource_type in self.get_resource_types():
            if sid in resource_type.resources:
                return resource_type.get_resource(sid)
        else:
            raise SurveyAttributeError(f'Survey does not contain "{id}" resource')

    def _publish(self) -> None:
        for service in self.get_services():
            for resource in service.get_resource_types():
                resource._freeze()
            service._freeze()
        self._freeze()

    def __contains__(self, __o: Any) -> bool:
        return any(__o == resource for resource in self.get_resources())


SURVEY = Survey()
