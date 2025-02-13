"""
Author: Andrew Viola
Created:
File: nscryptConverter.py
Description:
"""

# Imports
from . import ToolpathConverter # Parent Class
from typing import List

SUPPORTED_COMMANDS: List[str] = [
    "GenericCommand",
    "GenericCommand2"
]

class NscryptConverter(ToolpathConverter):
    def __init__(self):
        super().__init__(SUPPORTED_COMMANDS)

    def _process_command(self, command: str, params: dict[str, str]):
        """
        Processes a single command
        :param command: individual command to be translated
        """
        # TODO: perform processing of single command
        pass

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """
        # TODO: perform translation of list of commands
        pass