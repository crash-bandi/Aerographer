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

from collections.abc import Generator
from typing import Any, Iterable, Callable

from aerographer.crawler.generic import GenericCrawler

class Freezable:
    _frozen: bool
    _id: str

    def _freeze(self) -> None: ...
    def __delattr__(self, __key: str) -> None: ...
    def __setattr__(self, __key: str, __val: Any) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...


class SurveySearch(Generator):
    _checks: dict[str, Callable[[Any, list[Any]], bool]]

    def __init__(self, iter: Iterable) -> None: ...
    def __iter__(self) -> Generator[GenericCrawler, None, None]: ...
    def get(self) -> list[GenericCrawler]: ...
    def send(self, *args, **kwargs) -> Any: ...
    def throw(self, *args, **kwargs) -> None: ...
    def where(self, attribute: str, condition: str, values: list[Any]) -> SurveySearch: ...
    def where_not(self, attribute: str, condition: str, values: list[Any]) -> SurveySearch: ...

class SurveyResourceType(Freezable):
    resource_type: str
    resources: set[str]

    def __init__(self, resource_type: str) -> None: ...
    def _add_resource(self, resource: GenericCrawler) -> None: ...
    def get_resource(self, resource: str) -> GenericCrawler: ...
    def get_resources(self) -> SurveySearch: ...
    def __contains__(self, __o: Any) -> bool: ...

class SurveyService(Freezable):
    service: str
    resource_types: set[str]

    def __init__(self, service: str) -> None: ...
    @property
    def resources(self) -> set[str]: ...
    def _add_resource_type(self, resource_type: str) -> None: ...
    def get_resource_type(self, resource_type: str) -> SurveyResourceType: ...
    def get_resource_types(self) -> Generator[SurveyResourceType, None, None]: ...
    def get_resources(self) -> SurveySearch: ...
    def get_resource(self, id: str) -> GenericCrawler: ...
    def __contains__(self, __o: Any) -> bool: ...
    def __getattr__(self, __attr) -> SurveyResourceType: ...

class Survey(Freezable):
    services: str

    def __init__(self) -> None: ...
    @property
    def resources(self) -> set[str]: ...
    @property
    def resources_types(self) -> set[str]: ...
    def _add_service(self, service: str) -> None: ...
    def get_service(self, service: str) -> SurveyService: ...
    def get_services(self) -> Generator[SurveyService, None, None]: ...
    def get_resource_types(self) -> Generator[SurveyResourceType, None, None]: ...
    def get_resource_type(self, resource_type: str) -> SurveyResourceType:...
    def get_resources(self) -> SurveySearch: ...
    def get_resource(self, id: str) -> GenericCrawler: ...
    def _publish(self) -> None: ...
    def __contains__(self, __o: Any) -> bool: ...
    def __getattr__(self, __attr) -> SurveyService: ...

def _flatten(l: list[list[Any]]) -> list[Any]: ...
def _serialize_resource__id(resource: GenericCrawler) -> str: ...
def _get_obj_attr(o, path: str) -> list[Any]: ...
def _eq(val: Any, matches: list[Any]) -> bool: ...
def _ne(val: Any, matches: list[Any]) -> bool: ...
def _gt(val: Any, matches: list[Any]) -> bool: ...
def _lt(val: Any, matches: list[Any]) -> bool: ...
def _contains(val: Any, matches: list[Any]) -> bool: ...
def _not_contains(val: Any, matches: list[Any]) -> bool: ...
def _contains_all(val: Any, matches: list[Any]) -> bool: ...
def _not_contains_all(val: Any, matches: list[Any]) -> bool: ...
def _startswith(val: Any, matches: list[Any]) -> bool: ...
def _endswith(val: Any, matches: list[Any]) -> bool: ...

SURVEY: Survey
chars: str