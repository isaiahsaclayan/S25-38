from . import ToolpathConverter
from typing import List

COMMAND_MAP: dict[str,str] = {
    "GenericCommand" : "nScrypt Command"
}

class NscryptConverter(ToolpathConverter):
    def __init__(self):
        super().__init__(COMMAND_MAP)

    def _get_command(self, command: dict[str, dict[str, str]]) -> str:
        """
        Performs translation of a single command
        :param command: individual command to be translated
        :return: string representation of the translated command
        """
        # TODO: perform translation of single command
        pass

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """
        # TODO: perform translation of list of commands
        pass