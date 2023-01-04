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

WHITEBOARD: Whiteboard

class Whiteboard:
    board: dict[str, Any]

    def __init__(self) -> None: ...
    def new_section(self, section: str) -> None: ...
    def get_section(self, section: str) -> dict[str, Any]: ...
    def remove_section(self, section: str) -> None: ...
    def write(
        self,
        section: str,
        title: str,
        msg: Any,
        signature: str = ...,
        overwrite: bool = ...,
    ) -> None: ...
    def get(
        self, section: str, title: str = ..., signature: str = ...
    ) -> list[Any]: ...
    def erase(self, section: str, title: str = ..., signature: str = ...) -> None: ...
    def scribble(self, title: str, msg: Any) -> None: ...
    def get_scribble(self, title: str) -> Any: ...
    def print(self) -> None: ...
