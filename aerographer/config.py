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

"""Module configurations file.

Central location for global configuration values.
"""

import os
import pathlib
import json
from typing import Any


def separate(text: str | None, delimiter: str = ',') -> list[str | None]:
    """Return list from comma seperated string.

    Separates the provided string using the provided as delimiter and
    remove whitespace.

    Args:
        text (str): String to separate.
        delimiter (str): (optional) character to use as delimiter.

    Returns:
        A list of strings from the provided string.
    """
    if text is None:
        return [None]
    return [s.strip() for s in text.split(sep=delimiter)]


# internal properties
MODULE_PATH: str = str(pathlib.Path(__file__).parent.absolute())
# legacy -- MODULE_PATH: str = __loader__.path.replace('\\', '/').rsplit('/', 1)[0]

# external properties
LOGGING_LEVEL: str = os.getenv('AG_LOGGING_LEVEL', 'none')
PROFILES: list[str | None] = separate(os.getenv('AG_AWS_PROFILES', None))
ROLE: str | None = os.getenv('AG_AWS_ROLE', None)
REGIONS: list[str | None] = separate(
    os.getenv('AG_AWS_REGIONS', os.getenv('AWS_REGION', None))
)
SERVICE_DEFINITIONS_CONFIG: str = os.getenv(
    'AG_SERVICE_DEFINITIONS', f"{MODULE_PATH}/service_definitions.json"
)
ACCOUNTS: list[dict[str, Any]] = [
    {'profile': profile, 'regions': REGIONS, 'role': ROLE} for profile in PROFILES
]


with open(SERVICE_DEFINITIONS_CONFIG, 'r', encoding="utf-8") as f:
    SERVICE_DEFINITIONS: dict[str, Any] = json.load(f)
