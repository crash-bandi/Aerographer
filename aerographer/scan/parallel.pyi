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

from typing import Any, Awaitable, Callable, Iterable

async def asyncify(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any: ...
async def async_scan(cls: Any) -> Awaitable[Any]: ...
async def async_paginate(
    paginator: Any,
    id_key: str | None = ...,
    id_values: Iterable[Any] | None = ...,
    **kwargs: Any
) -> tuple[list[dict[str, Any]], ...]: ...
def _resolve_pages(page_iterator: Iterable[Any]) -> list[dict[str, Any]]: ...
