"""Type stub file"""

from typing import Any

MODULE_PATH: str
LOGGING_LEVEL: str
PROFILES: list[str | None]
ROLE: str | None
REGIONS: list[str | None]
ACCOUNTS: list[dict[str, Any]]
SERVICE_DEFINITIONS_CONFIG: str
SERVICE_DEFINITIONS: dict[str, Any]

def separate(text: str, regex: str = ...) -> list[str]: ...
