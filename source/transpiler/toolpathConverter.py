from typing import List

# Parent Class for Generic to Language Specific Conversion
class ToolpathConverter:

    def __init__(self, command_map: dict[str,str]):
        """
        :param command_map: Dictionary of generic command to language specific command
        """

        # Stores the mapping from the generic command to desired machine's command
        self._command_map: dict[str, str] = command_map

    def _get_command(self, command: dict[str, dict[str,str]]) -> str:
        """
        Performs translation of a single command
        To be overwritten in inherited classes
        :param command: individual command to be translated
        :return: string representation of the translated command
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
