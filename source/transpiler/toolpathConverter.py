"""
Author: Isaiah Amir Saclayan
Created: 1/29/25
File: toolpathConverter.py
Description: Parent class for toolpath conversion
"""
# Imports
from typing import List

# Parent Class for Generic to Language Specific Conversion
class ToolpathConverter:

    def __init__(self, supported_commands: list[str]):
        """
        :param supported_commands: Dictionary of generic command to language specific command
        """

        # Stores the mapping from the generic command to desired machine's command
        self._supported_commands: list[str] = supported_commands

        # Stores the list of translated commands
        self._translated_commands: list[str] = []

    def _process_command(self, command:str, params:dict[str, str]):
        """
        Processes a single command
        To be overwritten in inherited classes
        :param command: string representation of the generic command
        :param params: dictionary of parameters to format command
        """
        pass

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        To be overwritten in inherited classes
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """
        pass
