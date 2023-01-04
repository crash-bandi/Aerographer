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

"""Contains Whiteboard class.

Provides an instance of the Whiteboard class. This is
where evalutation results written. It can also be used
directly to store and display custom data.

    Typical usage example:

    from Whiteboard import WHITEBOARD
    WHITEBOARD.scribble(
        title="pondering",
        msg="Does anyone even read docstrings?"
    )
    WHITEBOARD.print()
"""

from copy import deepcopy
from pprint import pprint
from typing import Any

from aerographer.logger import logger
from aerographer.exceptions import (
    WhiteboardCreateSectionError,
    WhiteboardGetSectionError,
    WhiteboardRemoveSectionError,
    WhiteboardWriteError,
    WhiteboardGetError,
    WhiteboardEraseError,
)


class Whiteboard:
    """Simple data storage class.

    Provides convient way to collect and display data.


    Methods:
        new_section(section:str): Create new section.
        get_section(section:str): Get section.
        remove_section(section:str): Remove section.
        write(section:str, title:str, msg:Any, signature:str overwrite:bool): Write entry.
        get(section:str,  title:str signature:str): Get entry.
        erase(section:str,  title:str signature:str): Remove entry.
        scribble(title:str, msg:Any): Write entry to scribble section.
        get_scribble(title: str): Get entry from scribble section.
        print(): Print entire whiteboard.
    """

    def __init__(self) -> None:
        self.board: dict[str, Any] = {}
        self.new_section('scribbles')

    def new_section(self, section: str) -> None:
        """Create new section.

        Create a new section in the whiteboard.

        Args:
            section (str): Name for new section.

        Raises:
            WhiteboardCreateSectionError: section parameter not of type string.
        """
        if section == '':
            raise WhiteboardCreateSectionError('Section cannot be blank.')

        try:
            if section not in self.board:
                self.board[section] = {}
        except TypeError as err:
            raise WhiteboardCreateSectionError('Section must be a string.') from err

    def get_section(self, section: str) -> dict[str, Any]:
        """Get section.

        Get everything in a section in the whiteboard.

        Args:
            section (str): Name of section to get.

        Return:
            Copy of dictionary containing section data.
        """

        try:
            return deepcopy(self.board[section])
        except KeyError as err:
            raise WhiteboardGetSectionError(f'section {section} not found') from err
        except TypeError as err:
            raise WhiteboardGetSectionError('Section must be a string.') from err

    def remove_section(self, section: str) -> None:
        """Remove section.

        Deletes a section in the whiteboard.

        Args:
            section (str): Name for section to delete.

        """

        try:
            del self.board[section]
        except KeyError as err:
            raise WhiteboardRemoveSectionError(f'section {section} not found') from err
        except TypeError as err:
            raise WhiteboardRemoveSectionError('Section must be a string.') from err

    def write(
        self,
        section: str,
        title: str,
        msg: Any,
        signature: str = '',
        overwrite: bool = False,
    ) -> None:
        """Write entry.

        Writes and entry into a section.

        Args:
            section (str): Name for section to write to.
            title (str): Title of new entry.
            msg (str): Text of new entry.
            signature (str): Signature for new entry.
            overwrite (bool): (optional) allows overwriting existing entry. Default: False.
        """

        if not isinstance(signature, str):
            raise WhiteboardWriteError('Signature must be string.')
        if title == '':
            raise WhiteboardWriteError('Title cannot be blank.')

        self.new_section(section=section)

        try:
            if title in self.board[section]:
                if overwrite:
                    logger.debug(
                        'Write on existing entry %s requested, overwritting.', title
                    )
                else:
                    logger.debug(
                        'Write on existing entry %s requested without overwrite set. Skipping...',
                        title,
                    )
                    return
            self.board[section][title] = {'message': msg, 'signature': signature}
        except TypeError as err:
            raise WhiteboardWriteError('Title must be string.') from err

    def get(self, section: str, title: str = '', signature: str = '') -> list[Any]:
        """Get entry.

        Gets an entry in a section. Will return all entries that match
        provided parameters.

        Args:
            section (str): Name for section to get entry from.
            title (str): Title of entry to get.
            signature (str): Signature of entry to get.

        Return:
            List of found entries.
        """

        if not isinstance(signature, str):
            raise WhiteboardGetError('Signature must be string.')

        data = self.get_section(section=section)

        try:
            if title and signature:
                entry = data[title]
                if entry['signature'] == signature:
                    return [deepcopy(entry)]
            if title:
                return [deepcopy(data[title])]
            if signature:
                return [
                    deepcopy(entry)
                    for entry in data.values()
                    if entry['signature'] == signature
                ]
        except TypeError as err:
            raise WhiteboardGetError('Title must be string.') from err
        except KeyError:
            pass

        return []

    def erase(self, section: str, title: str = '', signature: str = '') -> None:
        """Delete entry.

        Deletes an entry in a section. Will delete all entries that match
        provided parameters.

        Args:
            section (str): Name for section to delete entry from.
            title (str): Title of entry to delete.
            signature (str): Signature of entry to delete.
        """

        if not isinstance(signature, str):
            raise WhiteboardEraseError('Signature must be string.')

        data = self.get_section(section=section)

        try:
            if title and signature:
                entry = data[title]
                if entry['signature'] == signature:
                    del self.board[section][title]
            elif title:
                del self.board[section][title]
            elif signature:
                for _t, entry in data.items():
                    if entry['signature'] == signature:
                        del self.board[section][_t]
        except TypeError as err:
            raise WhiteboardEraseError('Title must be string.') from err
        except KeyError as err:
            raise WhiteboardEraseError('Entry does not exist.') from err

    def scribble(self, title: str, msg: Any) -> None:
        """Write scribble.

        Writes and entry into the scribble section.

        Args:
            title (str): Title of new scribble.
            msg (str): Text of new scribble.
        """

        if title == '':
            raise WhiteboardWriteError('Title cannot be blank.')

        try:
            self.board['scribbles'][title] = msg
        except TypeError as err:
            raise WhiteboardWriteError('Title must be string.') from err

    def get_scribble(self, title: str) -> Any:
        """Get scribble.

        Gets an entry from the scribble section.

        Args:
            title (str): Title of entry to get.

        Return:
            scribble entry.
        """
        scribble = self.get(section='scribbles', title=title)
        if scribble:
            return scribble[0]

    def print(self) -> None:
        """Print whiteboard.

        Prints entire whiteboard with section headers. Uses pprint for formatting.
        """

        for section, body in self.board.items():
            print(
                f'============================================== {section} =============================================='
            )
            pprint(body)
            print()


WHITEBOARD = Whiteboard()
