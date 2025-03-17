import unittest
import os
import tempfile

import sys

# Get absolute path to the source/transpiler directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../source/transpiler"))
sys.path.insert(0, BASE_DIR)  # Insert at the beginning of sys.path
import guiRoot
import ToolpathExporter
import nscryptConverter
import parser
import applicationGlobals



class TestToolpathExporter(unittest.TestCase):
    def setUp(self):
        """Creates a temporary directory for testing exports."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.exporter = ToolpathExporter(self.temp_dir.name, "nScrypt")

    def tearDown(self):
        """Cleans up the temporary directory after each test."""
        self.temp_dir.cleanup()

    def test_valid_export(self):
        """Test successful toolpath export with valid data."""
        toolpath_data = ["MOVE X10 Y10 Z5 F300", "SET SPEED 100"]
        result = self.exporter.export_with_formatting(toolpath_data)
        self.assertIn("Export successful", result)

    def test_empty_toolpath(self):
        """Test exporting an empty toolpath fails with an error message."""
        result = self.exporter.export_with_formatting([])
        self.assertIn("Error", result)

    def test_invalid_command(self):
        """Test handling of invalid commands in the toolpath."""
        invalid_toolpath = ["INVALID_COMMAND 123"]
        result = self.exporter.export_with_formatting(invalid_toolpath)
        self.assertIn("Error", result)

    def test_correct_file_creation(self):
        """Ensure the exported file is created with the correct format."""
        toolpath_data = ["MOVE X10 Y10 Z5"]
        result = self.exporter.export_with_formatting(toolpath_data)
        
        # Extract file path from result
        file_path = result.split(": ")[1]
        self.assertTrue(os.path.exists(file_path))
    
    def test_custom_file_naming(self):
        """Ensure generated file name follows the expected pattern."""
        toolpath_data = ["MOVE X10 Y10 Z5"]
        self.exporter.export_with_formatting(toolpath_data)
        
        files = os.listdir(self.temp_dir.name)
        self.assertTrue(any(file.startswith("nScrypt_toolpath") and file.endswith(".gcode") for file in files))

    def test_invalid_export_path(self):
        """Test handling of invalid export directory."""
        invalid_exporter = ToolpathExporter("/invalid/directory", "nScrypt")
        toolpath_data = ["MOVE X10 Y10 Z5"]
        result = invalid_exporter.export_with_formatting(toolpath_data)
        self.assertIn("Error", result)

if __name__ == "__main__":
    unittest.main()
