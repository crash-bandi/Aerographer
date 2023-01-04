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

"""Contains components related to evaluations.

Contains classes and decorators related to custom built evaluations
for web crawler classes.
"""
from functools import wraps
from typing import Any, Callable
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Result:
    """Result of evaluation.

    Creates a dataclass representing a result of an evaluation.

    Attributes:
        message (str): (Optional) Evaluation message. Default: ''.
        status (bool): (Optional) If evaluation passed. Default: True
    """

    message: str = field(default='')
    status: bool = field(default=True)


def evaluation(
    service: str, resource: str, includes: list[str] | None = None
) -> Callable[..., Any]:
    """Evaluation decorator.

    Decorator for evalutions to set custom function attributes.

    Args:
        service (str): Value to set for __service__ attribute.
        resource (str): Value to set for __resource__ attribute.
        includes (list): Value to set for __includes__ attributes.

    Return:
        Decorated function.
    """

    if includes is None:
        includes = []

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        setattr(func, '__evaluation__', True)
        setattr(func, '__service__', service)
        setattr(func, '__resource__', resource)
        setattr(func, '__includes__', includes)

        @wraps(func)
        def wrapper(*args: list[Any], **kwargs: dict[str, Any]) -> Any:
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
