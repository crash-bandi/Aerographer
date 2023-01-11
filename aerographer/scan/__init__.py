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

Contains the functions required to establish, track, and
distribute sessions with the target AWS accounts for
scanning. Also contains the `SURVEY` data
structure where all data retrived by the web crawlers
is stored. Not meant for external use.
"""

from typing import Any
from aerographer.scan.context import (
    SESSION,
    CONTEXT,
    get_client,
    assume_role,
    get_session,
    get_caller_id,
)
from aerographer.logger import logger
from aerographer.config import ACCOUNTS, SERVICE_DEFINITIONS


SURVEY: dict[str, Any] = {}
CONTEXTS: tuple[CONTEXT, ...]


def _init_sessions(accounts: list[dict[str, Any]] = ACCOUNTS) -> tuple[SESSION, ...]:
    """Create scan sessions.

    Creates a collection of `SESSION` instances using list of account
    properties provided.

    Args:
        accounts (list[dict]): List of account properties to use for creating
            `SESSION` instances.

    Return:
        Tuple containing created `SESSION` instances.
    """

    sessions: list[SESSION] = []
    for account in accounts:
        for region in account['regions']:
            session = get_session(profile=account['profile'], region=region)

            if account['role']:
                session = assume_role(session=session, role_arn=account['role'])

            account_id = get_caller_id(session=session)['Account']

            logger.trace('Initializing session %s.%s...', account_id, region)  # type: ignore
            sessions.append(
                SESSION(
                    region=region,
                    session=session,
                )
            )
    return tuple(sessions)


def _init_contexts(
    sessions: tuple[SESSION, ...], services: set[str]
) -> tuple[CONTEXT, ...]:
    """Create scan contexts.

    Creates a collection of `CONTEXT` instances using list of sessions
    properties provided.

    Args:
        sessions (tuple): List of `SESSION` instances to use for creating
            `CONTEXT` instances.
        services (set[str]): Set of services to use for creating
            `CONTEXT` instances.

    Return:
        Tuple containing created `CONTEXT` instances.
    """

    contexts: list[CONTEXT] = []
    for session in sessions:
        caller_id = get_caller_id(session.session)
        for service in services:
            logger.trace(  # type: ignore
                'Initializing context %s:%s:%s...',
                caller_id["Account"],
                service,
                session.region,
            )
            contexts.append(
                CONTEXT(
                    name=f'{caller_id["Account"]}:{session.region}:{service}',
                    account_id=caller_id['Account'],
                    region=session.region,
                    service=service,
                    client=get_client(service=service, session=session.session),
                    session=session.session,
                )
            )
    return tuple(contexts)


def init(accounts: list[dict[str, Any]], services: set[str]) -> tuple[CONTEXT, ...]:
    """Initializes scan contexts.

    Initializes contexts for current scan.

    Args:
        accounts (list[dict]): List of account properties to use for initialization.
        services (set[str]): Set of services to use for initialization.

    Return:
        Tuple containing created `CONTEXT` instances.
    """

    sessions = _init_sessions(accounts)
    return _init_contexts(sessions, services)
