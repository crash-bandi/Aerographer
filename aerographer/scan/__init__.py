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
            account_id = get_caller_id(session=session)['Account']

            if account['role']:
                role_arn = f'arn:aws:iam::{account_id}:role/{account["role"]}'
                session = assume_role(session=session, role_arn=role_arn)

            logger.trace('Initializing session %s.%s...', account_id, region)  # type: ignore
            sessions.append(
                SESSION(
                    region=region,
                    session=session,
                )
            )
    return tuple(sessions)


def _init_contexts(sessions: tuple[SESSION, ...]) -> tuple[CONTEXT, ...]:
    """Create scan contexts.

    Creates a collection of `CONTEXT` instances using list of sessions
    properties provided.

    Args:
        sessions (tuple): List of `SESSION` instances to use for creating
            `CONTEXT` instances.

    Return:
        Tuple containing created `CONTEXT` instances.
    """

    contexts: list[CONTEXT] = []
    for session in sessions:
        caller_id = get_caller_id(session.session)
        for service in SERVICE_DEFINITIONS:
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


def init(accounts: list[dict[str, Any]]) -> tuple[CONTEXT, ...]:
    """Initializes scan contexts.

    Initializes contexts for current scan.

    Args:
        accounts (list[dict]): List of account properties to use for initialization.

    Return:
        Tuple containing created `CONTEXT` instances.
    """

    sessions = _init_sessions(accounts)
    return _init_contexts(sessions)
