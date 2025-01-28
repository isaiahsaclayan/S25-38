from typing import List

# Parent Class for Generic to Language Specific Conversion
class ToolpathConverter:

    # Initializer
    def __init__(self):
        # Stores the mapping from the generic command to desired machine's command
        self.commandMap: dict[str, str] = {}
        # Stores list of translated commands
        self.convertedCommands: List[str] = []

    # Performs translation of a single command
    def _getCommand(self):
        pass

    # Translates generic toolpath to list of formatted commands
    def translate(self):
        pass
