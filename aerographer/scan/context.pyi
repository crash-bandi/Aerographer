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
