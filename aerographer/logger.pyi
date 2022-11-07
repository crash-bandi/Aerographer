"""Type stub file"""

from typing import Any
import logging

log_levels: dict[str, Any]
logger: logging.Logger
handler: type
formatter: type

class LogFormatter(logging.Formatter):
    debug_format: str
    info_format: str
    default_format: str
    debug: bool

    def __init__(self) -> None: ...
    def format(self, record: logging.LogRecord) -> str: ...

def _add_logging_level(
    levelName: str, levelNum: int, methodName: str | None = ...
) -> None: ...
