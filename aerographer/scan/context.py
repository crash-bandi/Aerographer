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

"""Contains components required to crawling AWS.

Contains the classes required to establish sessions
with the target AWS accounts for scanning. Also contains
functions for session information retrieval. Not meant
for external use.
"""

import sys
from dataclasses import dataclass
from typing import Any

import boto3  # type: ignore
from botocore.exceptions import ProfileNotFound, NoCredentialsError, NoRegionError, ClientError, EndpointConnectionError  # type: ignore

from aerographer.logger import logger


@dataclass(frozen=True, slots=True)
class SESSION:
    """Dataclass representing boto3 session.

    Dataclass that contains boto3 session and associated data.

    Attributes:
        region (str): (class attribute) Region of session.
        session (boto3.Session): (class attribute) boto3 session instance.
    """

    region: str
    session: boto3.Session


@dataclass(frozen=True, slots=True)
class CONTEXT:
    """Dataclass representing scan context.

    Dataclass that contains associated data about unique scan context.

    Attributes:
        name (str): (class attribute) Profile name of context.
        account_id (str): Account id of context.
        region (str): (class attribute) Region of context.
        service (boto3.Session): (class attribute) service of context.
        client (boto3.Session.Client): boto3 client instance of context.
    """

    name: str
    account_id: str
    region: str
    service: str
    client: type
    session: boto3.Session


def get_session(region: str, profile: str | None = None) -> boto3.Session:
    """Get a boto3 session.

    Returns a boto3 session using provided profile and region.

    Args:
        profile (str): Profile to get session for.
        region (str): (optional) Region to get session for. Default: `default`

    Return:
        boto3 session.
    """

    try:
        logger.trace('Building boto3 session for %s - %s.', profile, region)  # type: ignore
        return boto3.Session(profile_name=profile, region_name=region)
    except ProfileNotFound as err:
        logger.error(err)
        sys.exit(1)


def assume_role(session: boto3.Session, role_arn: str) -> boto3.Session:
    """Get a boto3 session from assuming the provided role.

    Returns a boto3 session that has assumed the provided role.

    Args:
        session (boto3.Session): Session to use to assume the role.
        role_arn (str): Arn of the role to assume.

    Return:
        boto3 session.
    """

    client = get_client('sts', session)

    try:
        logger.trace(  # type: ignore
            'Retrieving STS credentials for %s with Session(profile_name=%s, region_name=%s).',
            role_arn,
            session.profile_name,
            session.region_name,
        )
        assumed_role_object = client.assume_role(
            RoleArn=role_arn, RoleSessionName="AerographerAssumedSession"
        )
    except (NoCredentialsError, ClientError) as err:
        logger.error(err)
        sys.exit(1)

    credentials = assumed_role_object['Credentials']

    logger.trace('Building boto3 session with STS credentials.')  # type: ignore
    return boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )


def get_client(service: str, session: boto3.Session = boto3.Session) -> Any:
    """Get a boto3 service client.

    Returns a boto3 client instance if the requested service
    using the provided session.

    Args:
        service (str): Service to get client for.
        session (boto3.Session): Session to use to get client.

    Return:
        boto3 client.
    """

    try:
        logger.trace(  # type: ignore
            'Building boto3 client for %s with Session(profile_name=%s, region_name=%s).',
            service,
            session.profile_name,
            session.region_name,
        )
        return session.client(service_name=service)
    except NoRegionError as err:
        logger.error(err)
        sys.exit(1)


def get_caller_id(session: boto3.Session) -> dict[str, str]:
    """Get caller identity.

    Queries the AWS STS endpoint using the provided session
    for the caller identity.
    https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html

    Args:
        session (boto3.Session): Session to use.

    Return:
        Caller identity data structure.

    Raises:
        NoCredentialsError: unable to locate AWS credentials
        ClientError: Client error when connecting to AWS API
        EndpointConnectionError: Connection error when conntecting to AWS API
    """

    try:
        logger.trace(  # type: ignore
            'Getting caller id with Session(profile_name=%s, region_name=%s).',
            session.profile_name,
            session.region_name,
        )
        client = get_client('sts', session)
        identity = client.get_caller_identity()
    except (NoCredentialsError, ClientError, EndpointConnectionError) as err:
        logger.error(err)
        sys.exit(1)
    return identity
