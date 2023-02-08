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

from typing import Any
from dataclasses import make_dataclass, field

from aerographer.exceptions import FrozenInstanceError


def make_survey(scan_data: dict[str, Any]) -> type:
    service_classes = []
    for service, resources in scan_data.items():
        service_class_name = service
        resource_fields = [
            (resource, FrozenDict, field(default_factory=FrozenDict))
            for resource in resources.keys()
        ]
        service_class = make_dataclass(
            service_class_name, resource_fields, slots=True, frozen=True
        )
        service_classes.append(
            service_class(**{r: FrozenDict(resources[r]) for r in resources})
        )

    survey_fields = [c.__class__.__name__ for c in service_classes]
    Survey = make_dataclass('Survey', survey_fields, slots=True, frozen=True)

    return Survey(**{c.__class__.__name__: c for c in service_classes})


class FrozenDict(dict):
    def __init__(self, *args, **kwargs):
        super(FrozenDict, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, *args, **kwargs):
        raise FrozenInstanceError(f"cannot assign to field '{args[0]}'")

    def __delitem__(self, *args, **kwargs) -> None:
        raise FrozenInstanceError(f"cannot delete field '{args[0]}'")

    # def __type__(self, *args, **kwargs):
    #     return dict
