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

"""Contains module logger.

Builds and configures module logger and
custom log formatter on initialization.
"""

import sys
import logging
from typing import Any

from aerographer.config import LOGGING_LEVEL
from aerographer.exceptions import InvalidLoggingLevelError


def addLoggingLevel(levelName: str, levelNum: int) -> None:
    """Add new logging level.

    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Args:
        levelName (str): name of level.
        levelNum (int): level numeric value.

    Example:
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    """

    # Method pulled from https://stackoverflow.com/a/35804945/1691778

    methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError(f'{levelName} already defined in logging module')
    if hasattr(logging, methodName):
        raise AttributeError(f'{methodName} already defined in logging module')
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError(f'{methodName} already defined in logger class')

    def logForLevel(self: Any, message: str, *args: Any, **kwargs: Any):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message: str, *args: Any, **kwargs: Any):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


TRACE = logging.DEBUG - 5
addLoggingLevel('TRACE', TRACE)

log_levels: dict[str, Any] = {
    'none': logging.NOTSET,
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARN,
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'trace': TRACE,
}


class LogFormatter(logging.Formatter):
    """Custom logging formatter.

    Custom paginator used to retrieve resource information from AWS.


    Attributes:
        debug_format (str): (class attribute) Logging format applied when in debug is enabled.
        info_format_format (str): (class attribute) Logging format for logging info messages.
        default_format (str): (class attribute) Logging format for everything other than info messages.
        debug (bool): (class attribute) Sets debug to enabled or disabled.

    Methods:
        format(record): format log record.
    """

    debug_format: str = '[%(filename)s:%(lineno)s - %(funcName)s() ]%(asctime)s: %(levelname)s - %(message)s'
    info_format: str = '%(message)s'
    default_format: str = '%(levelname)s - %(message)s'
    debug: bool = False

    def __init__(self) -> None:
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record: logging.LogRecord) -> str:
        """Create custom logging formatter.

        Create a custom logging formatter to dynamically change
        log format based on logging level.

        Args:
            record (logging.LogRecord): log record.

        Returns:
            Formatted log record.
        """

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if self.debug:
            self._style._fmt = LogFormatter.debug_format
        else:
            if record.levelno == logging.INFO:
                self._style._fmt = LogFormatter.info_format
            else:
                self._style._fmt = LogFormatter.default_format

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)

try:
    logger.setLevel(log_levels[LOGGING_LEVEL.lower()])
    handler.setLevel(log_levels[LOGGING_LEVEL.lower()])
except KeyError as err:
    raise InvalidLoggingLevelError(
        f'{LOGGING_LEVEL.lower()} is an invalid logging level.'
    ) from err

formatter = LogFormatter()
if logger.level in (log_levels['debug'], log_levels['trace']):
    formatter.debug = True

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.trace('Logger created.')  # type: ignore
