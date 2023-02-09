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
from typing import Any

from aerographer.crawler.generic import GenericCrawler, GenericMetadata

_CRAWLER_CACHE: dict[str, GenericCrawler]

def import_crawlers(service: str, skip: list[str], quiet_skip: bool) -> list[GenericCrawler]: ...
def initialize_crawler(
    service: str,
    resource: str,
    class_definition: dict[str, Any]) -> GenericCrawler | None: ...
def initialize_crawler_metadata(
    service: str,
    resource: str,
    class_definition: dict[str, Any]
) -> tuple[GenericMetadata, ...] | None: ...
def apply_external_evaluations(evaluations: list[str]) -> None: ...
def _create_crawler_metadata_classes(
    class_name: str,
    data: dict[str, Any] | list[Any] | Any,
    collection: list[GenericMetadata] | None = ...,
    _depth: int = ...,
) -> list[GenericMetadata] | tuple[Any, list[GenericMetadata]]: ...
def _resource_crawler_class_factory(
    service_path: str, class_name: str, class_definition: dict[str, Any]
) -> GenericCrawler: ...
def _resource_crawler_metadata_class_factory(
    class_name: str, class_definition: list[list[Any]]
) -> GenericMetadata: ...
def _serialize_class_name(name: str) -> str: ...
def _import_external_evaluations(path: str) -> dict[str, Any]: ...
def _extract_external_evaluation_functions(
    module: ModuleType, data: dict[str, Any]
) -> dict[str, Any]: ...
def _get_crawler_class(module: ModuleType) -> GenericCrawler: ...
def _merge_dictionaries(
    dict1: dict[str, Any], dict2: dict[str, Any]
) -> dict[str, Any]: ...