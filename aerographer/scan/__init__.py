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
import asyncio
from aerographer.scan.parallel import asyncify
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


def _init_session(profile: str, region: str, role: str) -> SESSION:
    """Create a scan session.

    Creates a `SESSION` instances using profile, region and role provided.

    Args:
        profile (str): profile to use to create `SESSION` instance.
        region (str): region to use to create `SESSION` instance.
        role (str): role to use to create `SESSION` instance.

    Return:
        `SESSION` instances.
    """
    session = get_session(profile=profile, region=region)

    if role:
        session = assume_role(session=session, role_arn=role)

    account_id = get_caller_id(session=session)['Account']

    logger.trace('Initializing session %s.%s...', account_id, region)  # type: ignore

    return SESSION(region=session.region_name, session=session)


def _init_service_contexts(session: SESSION, services: set[str]) -> list[CONTEXT]:
    caller_id = get_caller_id(session.session)
    """Create a collection scan contexts for the context and services provided.

    Creates a collection of `CONTEXT` instances using session and list of
    services provided.

    Args:
        session (SESSION): `SESSION` instance to use for creating
            `CONTEXT` instances.
        services (set[str]): Set of services to use for creating
            `CONTEXT` instances.

    Return:
        list containing created `CONTEXT` instances.
    """

    contexts: list[CONTEXT] = []
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

    return contexts


async def _init_sessions(
    accounts: list[dict[str, Any]] = ACCOUNTS
) -> tuple[SESSION, ...]:
    """Create scan sessions.

    Creates a collection of `SESSION` instances using list of account
    properties provided.

    Args:
        accounts (list[dict]): List of account properties to use for creating
            `SESSION` instances.

    Return:
        Tuple containing created `SESSION` instances.
    """

    logger.debug('Initializing sessions...')
    return tuple(
        await asyncio.gather(
            *(
                asyncify(_init_session, account['profile'], region, account['role'])
                for account in accounts
                for region in account['regions']
            )
        )
    )


async def _init_contexts(
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

    logger.debug('Initializing contexts...')
    return tuple(
        sum(
            await asyncio.gather(
                *(
                    asyncify(_init_service_contexts, session, services)
                    for session in sessions
                )
            ),
            [],
        )
    )


def init(accounts: list[dict[str, Any]], services: set[str]) -> tuple[CONTEXT, ...]:
    """Initializes scan contexts.

    Initializes contexts for current scan.

    Args:
        accounts (list[dict]): List of account properties to use for initialization.
        services (set[str]): Set of services to use for initialization.

    Return:
        Tuple containing created `CONTEXT` instances.
    """
    # TODO: exception handling doesn't work due to asyncio use.
    sessions = asyncio.run(_init_sessions(accounts))
    return asyncio.run(_init_contexts(sessions, services))
