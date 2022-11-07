"""Allows cli use.

Provides compatability with directly calling module
from CLI, including usage text. Not useful with
module import.

    Typical usage example:

    python.exe -m aerographer.scanner -s ec2.vpc -p default -r us-east-1 -v
"""

from aerographer.whiteboard import WHITEBOARD

if __name__ == '__main__':

    import sys
    import re

    import aerographer.config as config
    from aerographer.logger import logger

    def usage(code: int = 1) -> None:
        """Print cli usage."""

        print('-s --service, -h --help, -k --skip, -p --profile, -r --region')
        sys.exit(code)

    def separate(text: str, regex: str = r'\s|,') -> list[str]:
        """Return list from comma seperated string.

        Separates the provided string using regex expression provided as delimiter.

        Args:
            text (str): String to separate.
            regex (str): (optional) regex to use as delimiter.

        Returns:
            A list of strings from the provided string and regex delimiter.
        """

        return re.split(regex, text)

    inputs = sys.argv[1:]
    parameters: dict[str, list[str]] = {}
    keys = (
        ('-h', '--help', 'help'),
        ('-s', '--services', 'services'),
        ('-k', '--skip', 'skip'),
        ('-d', '--service-definitions', 'service-definitions'),
        ('-p', '--profiles', 'profiles'),
        ('-r', '--regions', 'regions'),
        ('-v', '--verbose', 'verbose'),
    )

    key: str = ''
    for i in inputs:
        if input not in sum([k[:2] for k in keys], ()):
            if not key:
                usage()
            parameters[key] += separate(i)
        else:
            key = [k[-1] for k in keys if i in k[:2]][0]
            parameters[key] = []

    if 'help' in parameters:
        usage(0)

    requested_services: list[str] = ['*']
    if 'services' in parameters:
        requested_services = parameters['services']
    else:
        usage(1)

    log_level = (
        'debug' if 'verbose' in parameters else 'info'
    )  # pylint: disable=invalid-name

    from aerographer.logger import log_levels, LogFormatter

    logger.setLevel(log_levels[log_level])
    for handler in logger.handlers:
        handler.setLevel(log_levels[log_level])
    LogFormatter.debug = log_level == 'debug'

    requested_skip: list[str] = parameters['skip'] if 'skip' in parameters else []
    regions: list[str] = (
        parameters['regions'] if 'regions' in parameters else config.REGIONS
    )
    profiles: list[str] = (
        parameters['profiles'] if 'profiles' in parameters else config.PROFILES
    )

    from aerographer.crawler import Crawler

    crawler = Crawler(
        services=requested_services,
        skip=requested_skip,
        profiles=profiles,
        regions=regions,
    )

    crawler.scan()
    WHITEBOARD.print()
