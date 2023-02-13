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

from typing import Any

from aerographer.survey import Survey
from aerographer.crawler.generic import GenericCrawler

SURVEY: type

class Crawler:
    services: str | list[str]
    skip: str | list[str] | None
    profiles: list[str] | None
    roles: list[str] | None
    regions: list[str] | None
    evaluations: list[str] | None
    crawlers: GenericCrawler

    def __init__(
        self,
        services: str | list[str] = ...,
        skip: str | list[str] | None = ...,
        profiles: list[str | None] = ...,
        roles: list[str] | None = ...,
        regions: list[str | None] = ...,
        evaluations: list[str] | None = ...,
        parameters: list[dict[str,dict]] | None = ...,
    ) -> None: ...
    def _apply_external_evaluations(self) -> None: ...
    def scan(self) -> Survey: ...

def get_crawlers(
    services: set[str], skip: list[str] | None = ...
) -> list[GenericCrawler]: ...
def get_crawler_includes(crawlers: list[GenericCrawler]) -> list[GenericCrawler]: ...
async def deploy_crawlers(
    crawlers: list[GenericCrawler],
) -> None: ...
