"""
Author: Bozhidar Dimov
Created:
File: toolpathExporter.py
Description:
"""

import os
import logging
from typing import List

# Logger for export process
logger = logging.getLogger("toolpathExporter")

class ToolpathExporter:
    """
    Handles exporting toolpaths to machine-readable formats (G-Code & ACSPL).
    Includes error handling, file saving, and formatting.
    """
    
    def __init__(self, export_path: str, printer_type: str):
        self.export_path = export_path
        self.printer_type = printer_type
        self.supported_formats = {"nScrypt": ".gcode", "Optomec": ".txt"}

    def validate_toolpath(self, toolpath: List[str]) -> bool:
        """
        Checks if the toolpath is valid before exporting.
        """
        if not toolpath:
            logger.error("Toolpath is empty. Cannot export.")
            return False
        for line in toolpath:
            if not isinstance(line, str) or len(line.strip()) == 0:
                logger.error("Invalid command in toolpath. Export failed.")
                return False
        return True
    
    def export(self, toolpath: List[str]):
        """
        Saves the toolpath in the appropriate format based on the printer type.
        """
        if not self.validate_toolpath(toolpath):
            return "Error: Invalid toolpath. Export aborted."

        file_extension = self.supported_formats.get(self.printer_type, ".txt")
        file_name = os.path.join(self.export_path, f"exported_toolpath{file_extension}")

        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.writelines([line + "\n" for line in toolpath])
            logger.info(f"Successfully exported toolpath to {file_name}")
            return f"Export successful: {file_name}"
        except Exception as e:
            logger.error(f"Failed to export toolpath: {e}")
            return f"Error: {str(e)}"
    
    def format_gcode(self, toolpath: List[str]) -> List[str]:
        """
        Converts generic toolpath instructions to nScrypt-compatible G-Code.
        """
        formatted_toolpath = []
        for command in toolpath:
            formatted_toolpath.append(f"G0 {command}")  # Example transformation
        return formatted_toolpath

    def format_acspl(self, toolpath: List[str]) -> List[str]:
        """
        Converts generic toolpath instructions to Optomec-compatible ACSPL.
        """
        formatted_toolpath = []
        for command in toolpath:
            formatted_toolpath.append(f"MOVE {command}")  # Example transformation
        return formatted_toolpath
    
    def map_commands(self, toolpath: List[str]) -> List[str]:
        """
        Maps toolpath instructions based on printer type.
        """
        if self.printer_type == "nScrypt":
            return self.format_gcode(toolpath)
        elif self.printer_type == "Optomec":
            return self.format_acspl(toolpath)
        else:
            logger.error("Unsupported printer type. Cannot map commands.")
            return []
    
    def export_with_formatting(self, toolpath: List[str]):
        """
        Exports the formatted toolpath.
        """
        formatted_toolpath = self.map_commands(toolpath)
        return self.export(formatted_toolpath)
