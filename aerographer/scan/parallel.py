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

"""Contains components required for asycronous calls.

Contains the functions require to support asyncronous
web calls during AWS crawling. Not meant for external
use.
"""

import time
import inspect
import asyncio
from typing import Any, Callable, Coroutine, Iterable

from botocore.exceptions import ClientError  # type: ignore

from aerographer.logger import logger
from aerographer.exceptions import (
    ActiveCrawlerScanError,
    TimeOutCrawlerScanError,
    PaginatorNotFoundError,
    FailedCrawlerScanError,
)


async def asyncify(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Run function ansyncronously.

    Run the provided funtion in an asyncio thread.

    Args:
        func: fucntion to run in asyncio thread.

    Return:
        results of function.
    """

    if inspect.iscoroutinefunction(func):
        logger.trace('%s is already coroutine', func.__name__)  # type: ignore
        return await func(*args, **kwargs)
    logger.trace('%s is not coroutine, running in thread.', func.__name__)  # type: ignore
    return await asyncio.to_thread(func, *args, **kwargs)


async def async_scan(cls: Any) -> None:
    """Run asyncronous scan.

    Runs the scan function of the web crawler class provided asyncrously.
    If the web crawler already has a scan in process, wait for up to 120
    seconds to allow the scan to complete.

    Args:
        cls (GenericCrawler): web crawler class to run scan from.

    Raises:
        FailedCrawlerScanError: Scan failed.
        TimeOutCrawlerScanError: Scan timed out.
    """

    for _ in range(60):
        try:
            return await cls.scan()
        except ActiveCrawlerScanError:
            await asyncio.sleep(2)
        except PaginatorNotFoundError as err:
            raise FailedCrawlerScanError(err) from err

    raise TimeOutCrawlerScanError


async def async_paginate(
    paginator: Any,
    id_key: str | None = None,
    id_values: Iterable[Any] | None = None,
    **kwargs: Any,
) -> tuple[list[dict[str, Any]], ...]:
    """Run asyncronous pagination.

    Runs the paginator class provided asyncrously. If is list of
    ids are provided, it will build and run a paginator for every
    id and return a zip of ids and results.

    Args:
        paginator (Any): Paginator class to run.
        id_key (str): (Optional) value to use for id key.
        id_values (list[str]): (Optional) list to use for id values.
        **kwargs: (Optional) additional arguments to pass to paginator.

    Return:
        Tuple containing lists of pages.

    Raises:
        FailedCrawlerScanError: Scan failed.
        Boto3.ClientError: Scan failed.
    """

    if (id_key and not id_values) or (id_values and not id_key):
        raise ValueError('id_key and id_values are both required.')

    logger.debug('Paginating for %s.%s.', paginator.context, paginator.function)

    for attempt in range(4):
        if attempt:
            logger.trace(  # type: ignore
                'Pager %s.%s. attempt: %s',
                paginator.context,
                paginator.function,
                attempt + 1,
            )

        # number of retries * 2 seconds
        stagger_delay: int = attempt * 2
        # number of attempts * 50 milliseconds
        pager_delay: float = ((attempt + 1) * 50) / 1000

        paginators: dict[str, Coroutine[Any, Any, Any]] = {}
        if id_key:
            paginators.update(
                {
                    v: asyncify(paginator.paginate, **{id_key: v}, **kwargs)
                    for v in id_values
                }
            )
        else:
            paginators = {'resource': asyncify(paginator.paginate, **kwargs)}

        logger.trace('Gathering paginators for %s.%s.', paginator.context, paginator.function)  # type: ignore
        pages_iterables = []
        for index, item in enumerate(
            dict(
                zip(paginators.keys(), await asyncio.gather(*paginators.values()))
            ).items()
        ):
            key, pager = item
            pages_iterables.append(
                asyncify(
                    _resolve_pages,
                    pager,
                    paginator.context,
                    paginator.function,
                    key,
                    stagger_delay * index,
                    pager_delay,
                )
            )

        try:
            logger.trace('Resolving pages for %s.%s.', paginator.context, paginator.function)  # type: ignore
            pages = await asyncio.gather(*pages_iterables)
        except ClientError as err:
            if err.response['Error']['Code'] == 'Throttling':
                logger.trace('Coroutine queue size: %s', len(asyncio.all_tasks()))  # type: ignore
                logger.warning(
                    'Pagination for %s.%s call limit exceeded; backing off and retrying...',
                    paginator.context,
                    paginator.function,
                )
                time.sleep((attempt + 1) * 30)
                continue
            raise

        logger.trace('Pagination for %s.%s complete.', paginator.context, paginator.function)  # type: ignore
        return pages

    raise FailedCrawlerScanError(
        f'{paginator.context}.{paginator.function}: Max retries exceeded.'
    )


def _resolve_pages(
    page_iterator: Iterable[Any],
    context: str,
    func: str,
    key: str,
    task_delay: int,
    page_delay: float,
) -> list[dict[str, Any]]:
    """Resolves pagniator pages.

    Resolves and returns all pages from the provided
    page interator.

    Args:
        page_iterator (Any): Page interactor to resolve.
        context (str): name of context.
        func (str): name of function.
        key(str): resource id.
        task_delay (int): number of seconds to delay job execution.
        page_delay(float): number of seconds to pause between each page.

    Return:
        List of pages.

    Raises:
        Boto3.CleintError: Pagination failed.
    """

    time.sleep(task_delay)

    logger.trace('Paging on %s.%s.%s...', context, func, key)  # type: ignore

    try:
        pages = []
        for page in page_iterator:
            time.sleep(page_delay)
            pages.append(page)
    except ClientError as err:
        logger.trace(  # type: ignore
            'Pager %s.%s.%s experienced ClientError: %s', context, func, key, err
        )
        raise

    logger.trace('Done paging %s.%s.%s.', context, func, key)  # type: ignore

    return pages
