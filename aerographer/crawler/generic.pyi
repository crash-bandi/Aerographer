"""Type stub file"""

from abc import ABC
from types import FunctionType
from typing import Any, Callable, Generator, Protocol

import aerographer.scan as scan
from aerographer.scan.context import CONTEXT

class PaginateWrapper:
    func: FunctionType

    def __init__(self, func: FunctionType) -> None: ...
    def paginate(self, **kwargs: Any) -> Generator[dict[str, Any], Any, Any]: ...

class GenericCustomPaginator(ABC):
    INCLUDE: list[str]
    context: CONTEXT
    paginate_func_name: str
    _paginate_func: Callable[..., Any]
    paginator: Callable[..., Any]

    def __init__(self, context: CONTEXT, paginator_func_name: str) -> None: ...
    async def paginate(self, **kwargs: Any) -> tuple[dict[str, Any], ...]: ...

class GenericMetadata(Protocol):
    __dataclass_fields__: dict[Any, Any]

class GenericCrawler:
    state: str
    evaluations: tuple[str, ...]
    custom_paginator: Callable[..., Any]
    INCLUDE: list[str]
    serviceType: str
    resourceType: str
    resourceName: str
    paginator: str
    scanParameters: dict[str, Any]
    idAttribute: str
    data: GenericMetadata
    context: CONTEXT
    id: str
    iac_id: str
    results: list[tuple[str, str, bool]]
    passed: bool
    __name__: str

    def __init__(self, context: CONTEXT, metadata: dict[str, Any]) -> None: ...
    def _set_id(self) -> None: ...
    def _set_infrastructure_as_code_id(self) -> None: ...
    def evaluate(self, evaluation: str) -> bool: ...
    def run_evaluations(self) -> None: ...
    def _build_metadata(
        self, metadata: dict[str, Any] | list[Any] | Any, path: str = ...
    ) -> GenericMetadata | tuple[Any]: ...
    @classmethod
    def _get_metadata_class(cls, name: str = ...) -> GenericMetadata: ...
    @classmethod
    def _get_paginator(cls, context: CONTEXT) -> GenericCustomPaginator: ...
    @classmethod
    async def scan(cls) -> None: ...
    def as_json(self) -> str: ...
    def __eq__(self, __o: object) -> bool: ...
