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
from dataclasses import dataclass

import boto3  # type:ignore

@dataclass
class SESSION:
    region: str
    session: boto3.Session

@dataclass
class CONTEXT:
    name: str
    account_id: str
    region: str
    service: str
    client: type
    session: boto3.Session

def get_session(profile: str, region: str) -> boto3.Session: ...
def assume_role(session: boto3.Session, role_arn: str) -> boto3.Session: ...
def get_client(service: str, session: boto3.Session = ...) -> Any: ...
def get_caller_id(session: boto3.Session) -> dict[str, str]: ...
