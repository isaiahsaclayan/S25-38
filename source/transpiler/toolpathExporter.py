"""
Author: Bozhidar Dimov
Updated: [Insert Date]
File: toolpathExporter.py
Description: Efficient and safe toolpath export system.
"""

import os
import logging
import io
import shutil
import time
from typing import List
from applicationGlobals import writeStatusQueue

logger = logging.getLogger("toolpathExporter")

class ToolpathExporter:
    def __init__(self, export_path: str, printer_type: str):
        self.export_path = export_path
        self.printer_type = printer_type
        self.supported_formats = {"nScrypt": ".gcode", "Optomec": ".txt"}

        # Ensure export directory exists
        os.makedirs(self.export_path, exist_ok=True)

    def validate_toolpath(self, toolpath: List[str]) -> bool:
        """Validates the toolpath before exporting."""
        if not toolpath:
            writeStatusQueue("Error: Toolpath is empty. Export aborted.")
            logger.error("Toolpath validation failed: Empty toolpath.")
            return False
        for line in toolpath:
            if not isinstance(line, str) or len(line.strip()) == 0:
                writeStatusQueue("Error: Invalid command in toolpath. Export failed.")
                logger.error(f"Invalid command detected: {line}")
                return False
        return True

    def get_unique_filename(self, base_name: str, extension: str) -> str:
        """
        Generates a unique filename using timestamp to prevent overwriting.
        Example: nScrypt_20250303_153045.gcode
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.export_path, f"{base_name}_{timestamp}{extension}")

    def export(self, toolpath: List[str]):
        """Exports the toolpath to a file safely with robust error handling."""
        if not self.validate_toolpath(toolpath):
            return "Error: Invalid toolpath."

        file_extension = self.supported_formats.get(self.printer_type, ".txt")
        base_name = f"{self.printer_type}_toolpath"
        final_file = self.get_unique_filename(base_name, file_extension)
        temp_file = final_file + ".tmp"

        try:
            # Buffered writing to optimize large files
            with open(temp_file, "w", encoding="utf-8", buffering=io.DEFAULT_BUFFER_SIZE) as file:
                file.writelines("\n".join(toolpath) + "\n")

            # Ensure successful write before replacing the final file
            shutil.move(temp_file, final_file)

            file_size = os.path.getsize(final_file)
            writeStatusQueue(f"Export successful: {final_file} ({file_size} bytes)")
            logger.info(f"Toolpath exported successfully: {final_file} ({file_size} bytes)")

            return f"Export successful: {final_file} ({file_size} bytes)"

        except Exception as e:
            logger.error(f"Failed to export toolpath: {e}")
            writeStatusQueue(f"Error: {str(e)}")
            return f"Error: {str(e)}"

    def format_gcode(self, toolpath: List[str]) -> List[str]:
        """
        Converts generic toolpath instructions to nScrypt-compatible G-Code.
        """
        return [f"G0 {command}" for command in toolpath]

    def format_acspl(self, toolpath: List[str]) -> List[str]:
        """
        Converts generic toolpath instructions to Optomec-compatible ACSPL.
        """
        return [f"MOVE {command}" for command in toolpath]

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
