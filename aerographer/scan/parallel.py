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

import inspect
import asyncio
from typing import Any, Callable, Coroutine, Iterable

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

    for i in range(60):
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
    """

    if (id_key and not id_values) or (id_values and not id_key):
        raise ValueError('id_key and id_values are both required.')

    paginators: list[Coroutine[Any, Any, Any]] = []
    if id_key:
        paginators.extend(
            [asyncify(paginator.paginate, **{id_key: v}, **kwargs) for v in id_values]
        )
    else:
        paginators.append(asyncify(paginator.paginate, **kwargs))

    logger.trace('Gathering paginators for %s.', paginator.function)  # type: ignore
    pages_iterables = await asyncio.gather(*paginators)

    logger.trace('Resolving pages for %s.', paginator.function)  # type: ignore
    pages = await asyncio.gather(
        *[
            asyncify(_resolve_pages, pager, paginator.context, paginator.function)
            for pager in pages_iterables
        ]
    )
    logger.trace('Pagination for %s complete.', paginator.function)  # type: ignore

    return pages


def _resolve_pages(
    page_iterator: Iterable[Any], context: str, func: str
) -> list[dict[str, Any]]:
    """Resolves pagniator pages.

    Resolves and returns all pages from the provided
    page interator.

    Args:
        page_iterator (Any): Page interactor to resolve.
        context (str): name of context.
        func (str): name of function.

    Return:
        List of pages.
    """

    # TODO: implement retry process for timeouts
    # botocore.exceptions.ClientError: An error occurred (Throttling) when calling the GetPolicyVersion operation (reached max retries: 4): Rate exceeded
    logger.trace('Paging on %s.%s...', context, func)  # type: ignore
    pages = [page for page in page_iterator]
    logger.trace('Done paging %s.%s.', context, func)  # type: ignore

    return pages
