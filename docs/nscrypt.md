# nscryptConverter.py
Inherits from the ToolpathConverter parent class and implements _process_command and translate. Additionally there are helper functions to help translate various parsed commands

## __init__()
This initializes the nScrypt Converter with the parent class along with a units private member, which determines which units to be used.

## _translate_move(self, params: dict[str, str])
This function translates a parsed move command into the nScrypt format. nScrypt machines require toolpaths to be written in the following format:

For vectors:
- XYZ X'Y'Z'

For spherical coordinates:
- XYZ 0W

Current implementation only supports the spherical coordinates, which indicates 5 axis being used. The _translate_move function will then place the corresponding X Y and Z coordinates into their respective spots. It then appends the remaining axis in a sorted order into the command. Additionally, this function will convert whatever unit is currently enabled into millimeters.

## _change_units(self, params: dict[str, str])
Sets the private unit member to the specified unit if supported by the parser.

## _tool_on_off(self, params: dict[str, str])
Takes a control command from the parser and will output "TOOL OFF" or "TOOL ON" dependent on status

## _process_command(self, command: str, params: dict[str, str])
Takes the parsed command and will place it the correct function as necessary. Will output an invalid command status if any invalid command is found.

## translate(self, parsed_commands: List[dict[str, dict[str, str]]])
Returns a list of translated commands. Appends the initial version and type as specified by the parsed information, then loops through all the commands and translates them. 
