"""Type stub file"""

from typing import Any
from aerographer.scan.context import SESSION, CONTEXT
from aerographer.crawler.generic import GenericCrawler

SURVEY: dict[str, dict[str, dict[str, GenericCrawler]]]
CONTEXTS: tuple[CONTEXT, ...]

def _init_sessions(accounts: list[dict[str, Any]] = ...) -> tuple[SESSION, ...]: ...
def _init_contexts(sessions: tuple[SESSION, ...]) -> tuple[CONTEXT, ...]: ...
def init(accounts: list[dict[str, Any]]) -> tuple[CONTEXT, ...]: ...
