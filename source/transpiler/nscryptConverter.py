"""
Author: Andrew Viola
Created: 02/06/2025
File: nscryptConverter.py
Description: Performs generic toolpath to nScrypt conversion.
"""

# Imports
from toolpathConverter import ToolpathConverter # Parent Class
from typing import List

TOOL = "spindle_speed"
INVALID_COMMAND = "INVALID"

SUPPORTED_COMMANDS: List[str] = [
    "move",
    TOOL,
    "units"
]

class NscryptConverter(ToolpathConverter):
    def __init__(self):
        super().__init__(SUPPORTED_COMMANDS)
        self._units = None

    def _process_command(self, command: str, params: dict[str, str]):
        """
        Processes a single command
        :param command: individual command to be translated
        """
        # TODO: perform processing of single command
        if command not in self._supported_commands:
            return INVALID_COMMAND
        else:
            if command == SUPPORTED_COMMANDS[0]:
                pass
            elif command == SUPPORTED_COMMANDS[1]:
                pass
            elif command == SUPPORTED_COMMANDS[2]:
                pass
        pass

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """
        # TODO: perform translation of list of commands
        nScrypt_commands = []
        for command_info in parsed_commands:
            command = list(command_info.keys())[0]
            params = command_info[command]
            converted_command = self._process_command(command, params)
            if converted_command != INVALID_COMMAND:
                nScrypt_commands.append(converted_command)
                self._translated_commands.append(converted_command)
        return nScrypt_commands
            
            
test1 = ToolpathConverter(SUPPORTED_COMMANDS)
test2 = NscryptConverter()

commands = [{"move":{"x":"1","y":"2","z":"3"}}]

test2.translate(commands)