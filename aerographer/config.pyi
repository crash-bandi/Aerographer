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

MODULE_PATH: str
LOGGING_LEVEL: str
PROFILES: list[str | None]
ROLES: list[str | None]
REGIONS: list[str | None]
ACCOUNTS: list[dict[str, Any]]
SERVICE_DEFINITIONS_CONFIG: str
SERVICE_DEFINITIONS: dict[str, Any]

def separate(text: str, regex: str = ...) -> list[str]: ...
