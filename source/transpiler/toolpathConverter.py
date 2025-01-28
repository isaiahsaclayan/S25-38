from typing import List

# Parent Class for Generic to Language Specific Conversion
class ToolpathConverter:

    # Initializer
    def __init__(self):
        # Stores the mapping from the generic command to desired machine's command
        self.commandMap: dict[str, str] = {}

    def _get_command(self, command: dict[str, dict[str,str]]) -> str:
        """
        Performs translation of a single command
        :param command: individual command to be translated
        :return:
        """
        pass

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return:
        """
        pass
