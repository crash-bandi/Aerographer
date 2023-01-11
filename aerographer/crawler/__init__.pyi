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

"""Type stub file"""

from types import ModuleType
from typing import Any, Type

import aerographer.scan as scan
from aerographer.crawler.generic import GenericCrawler

class Crawler:
    services: str | list[str]
    skip: str | list[str] | None
    profiles: list[str] | None
    regions: list[str] | None
    role: str | None
    evaluations: list[str] | None
    crawlers: GenericCrawler
    _external_evalutations: dict[str, Any]

    def __init__(
        self,
        services: str | list[str] = ...,
        skip: str | list[str] | None = ...,
        profiles: str | list[str | None] = ...,
        regions: str | list[str | None] = ...,
        role: str | None = ...,
        evaluations: list[str] | None = ...,
    ) -> None: ...
    def _apply_external_evaluations(self) -> None: ...
    def scan(self) -> dict[str, Any]: ...

def _merge_dictionaries(
    dict1: dict[str, Any], dict2: dict[str, Any]
) -> dict[str, Any]: ...
def initialize_crawler(service: str, resource: str) -> GenericCrawler | None: ...
def initialize_crawler_metadata(
    service: str, resource: str
) -> tuple[type, ...] | None: ...
def _create_crawler_metadata_classes(
    class_name: str,
    data: dict[str, Any] | list[Any] | Any,
    collection: list[type] | None = ...,
) -> Any: ...
def _resource_crawler_class_factory(
    class_path: str, class_name: str, class_definition: dict[str, Any]
) -> GenericCrawler: ...
def _resource_crawler_metadata_class_factory(
    class_name: str, class_definition: list[list[Any]]
) -> type: ...
def _serialize_class_name(name: str) -> str: ...
def _import_external_evaluations(path: str) -> dict[str, Any]: ...
def _extract_external_evaluation_functions(
    module: ModuleType, data: dict[str, Any]
) -> dict[str, Any]: ...
def get_crawler(service: str, skip: list[str]) -> list[GenericCrawler]: ...
def _get_crawler_class(module: ModuleType) -> GenericCrawler: ...
def get_crawlers(
    services: str | list[str], skip: str | list[str] | None = ...
) -> list[GenericCrawler]: ...
async def deploy_crawlers(
    crawlers: list[GenericCrawler],
) -> None: ...
