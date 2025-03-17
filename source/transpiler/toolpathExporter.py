"""
Author: Bozhidar Dimov
Created:
File: toolpathExporter.py
Description: Exports formatted toolpaths with error handling.
"""

import os
import logging
from typing import List
from applicationGlobals import writeStatusQueue

logger = logging.getLogger("toolpathExporter")

class ToolpathExporter:
    def __init__(self, export_path: str, printer_type: str):
        """
        Initializes the ToolpathExporter with an export path and printer type.
        
        :param export_path: Directory where the file will be saved.
        :param printer_type: Type of printer (nScrypt or Optomec) to determine file extension.
        """
        self.export_path = export_path
        self.printer_type = printer_type
        self.supported_formats = {"nScrypt": ".gcode", "Optomec": ".txt"}

    def validate_toolpath(self, toolpath: List[str]) -> bool:
        """
        Validates the toolpath data before writing to file.
        
        :param toolpath: List of strings representing toolpath commands.
        :return: True if valid, False if invalid.
        """
        if not toolpath:
            writeStatusQueue("Error: Toolpath is empty. Export aborted.")
            return False
        for line in toolpath:
            if not isinstance(line, str) :
                writeStatusQueue("Error: Invalid command in toolpath. Export failed.")
                return False
        return True

    def export(self, toolpath: List[str]) -> str:
        """
        Writes the toolpath instructions to a file exactly as they are received.
        
        :param toolpath: List of strings containing toolpath instructions.
        :return: Success or error message.
        """
        if not self.validate_toolpath(toolpath):
            return "Error: Invalid toolpath."

        file_extension = self.supported_formats.get(self.printer_type, ".txt")
        file_name = os.path.join(self.export_path, f"exported_toolpath{file_extension}")

        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.writelines("\n".join(toolpath) + "\n")  # Ensures correct line endings
            writeStatusQueue(f"Export successful: {file_name}")
            return f"Export successful: {file_name}"
        except Exception as e:
            writeStatusQueue(f"Error: {str(e)}")
            return f"Error: {str(e)}"
