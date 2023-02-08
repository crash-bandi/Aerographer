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
from aerographer.scan.context import SESSION, CONTEXT
from aerographer.crawler.generic import GenericCrawler

scan_results: dict[str, dict[str, dict[str, GenericCrawler]]]
CONTEXTS: tuple[CONTEXT, ...]

def _init_session(profile:str, region:str, role:str) -> SESSION: ...
def _init_service_contexts(session:SESSION, services:set[str]) -> list[CONTEXT]: ...
async def _init_sessions(accounts: list[dict[str, Any]] = ...) -> tuple[SESSION, ...]: ...
async def _init_contexts(sessions: tuple[SESSION, ...], services: set[str]) -> tuple[CONTEXT, ...]: ...
def build_contexts(accounts: list[dict[str, Any]], services: set[str]) -> tuple[CONTEXT, ...]: ...
