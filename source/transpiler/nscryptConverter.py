"""
Author: Andrew Viola
Created: 02/06/2025
File: nscryptConverter.py
Description: Performs generic toolpath to nScrypt conversion.
"""

# Imports
from toolpathConverter import ToolpathConverter # Parent Class
from applicationGlobals import writeStatusQueue
from typing import List

TOOL = "spindle_speed"
INVALID_COMMAND = "INVALID"
DO_NOT_SHOW = "DO_NOT_SHOW"
VERSION = "Version 1.1"
TYPE = "Type Spherical"

SUPPORTED_COMMANDS: List[str] = [
    "move",
    TOOL,
    "units"
]

SUPPORTED_UNITS: List[str] = [
    "MILLIMETERS",
    "INCHES"
]

class NscryptConverter(ToolpathConverter):
    def __init__(self):
        super().__init__(SUPPORTED_COMMANDS)
        self._units = SUPPORTED_UNITS[0] # Millimeters

    def _process_command(self, command: str, params: dict[str, str]):
        """
        Processes a single command
        :param command: individual command to be translated
        """
        if command not in self._supported_commands:
            writeStatusQueue(f"Invalid command: {command}")
            return INVALID_COMMAND
        else:
            if command == SUPPORTED_COMMANDS[0]: # Move
                converted_command = self._translate_move(params)
            elif command == SUPPORTED_COMMANDS[1]: # Tool on/off command
                converted_command = self._tool_on_off(params)
            elif command == SUPPORTED_COMMANDS[2]: # Units
                converted_command = self._change_units(params)
            return converted_command
    
    def _translate_move(self, params: dict[str, str]):
        """
        Translate move command to nScrypt format
        :param params: dictionary of move command parameters
        """
        conversion_factor = 1
        if self._units == SUPPORTED_UNITS[1]: # Inches
            conversion_factor = 25.4
        elif self._units == SUPPORTED_UNITS[0]: # Millimeters
            conversion_factor = 1
        # nScrypt will always do XYZ X'Y'Z' or XYZ 0W
        converted_command = f"{float(params['x'])*conversion_factor} {float(params['y'])*conversion_factor} {float(params['z'])*conversion_factor}"
        params.pop('x')
        params.pop('y')
        params.pop('z')
        # Not sure what the remaining axis would be labeled from Creo, so I just append all remaining axis
        remaining_axis = list(params.keys())
        append0 = 2
        if len(remaining_axis) == 1:
            append0 = 1
        elif len(remaining_axis) == 2:
            append0 = 0
        remaining_axis.sort()
        for axis in remaining_axis:
            converted_command += f" {float(params[axis])*conversion_factor}"
        for i in range(append0):
            converted_command += " 0.0"
        return converted_command
                
    
    def _change_units(self, params: dict[str, str]):
        """
        Change units for nScrypt
        :param params: dictionary of units command parameters
        """
        if params["units"] not in SUPPORTED_UNITS:
            writeStatusQueue(f"Invalid units: {params['units']}")
            return INVALID_COMMAND
        else:
            self._units = params["units"]
            return DO_NOT_SHOW
        
    def _tool_on_off(self, params: dict[str, str]):
        """
        Translate tool on/off command to nScrypt format
        :param params: dictionary of tool on/off command parameters
        """
        if params["control"][:3] == "OFF":
            return "TOOL OFF"
        else:
            return "TOOL ON"
        

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """
        if len(parsed_commands) == 0:
            return []
        nScrypt_commands = []
        nScrypt_commands.append(VERSION)
        nScrypt_commands.append(TYPE) # TODO: Eventually determine between Vector and Spherical, for now just Vector
        for command_info in parsed_commands:
            command = list(command_info.keys())[0]
            params = command_info[command]
            converted_command = self._process_command(command, params)
            if converted_command != INVALID_COMMAND and converted_command != DO_NOT_SHOW:
                nScrypt_commands.append(converted_command)
                self._translated_commands.append(converted_command)
            elif converted_command == INVALID_COMMAND:
                pass #nScrypt_commands.append(f"!INVALID COMMAND: {command_info}") Notes: I'm not sure this is necessary, if the export handled invalid commands it would be fine, but for simplicity sake I think we should just remove invalid but nonbreaking commands
            
        return nScrypt_commands