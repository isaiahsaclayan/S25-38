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
        self.export_path = "test_exports"
        self.exporter = ToolpathExporter(self.export_path, "nScrypt")
        os.makedirs(self.export_path, exist_ok=True)

    def tearDown(self):
        # Cleanup exported files after each test
        for file in os.listdir(self.export_path):
            os.remove(os.path.join(self.export_path, file))
        os.rmdir(self.export_path)

    def test_export_success(self):
        """Test exporting a valid toolpath for nScrypt"""
        toolpath_data = ["MOVE X10 Y10 Z5 F300", "SET SPEED 100", ""]  # Includes empty line
        result = self.exporter.export(toolpath_data)
        self.assertIn("Export successful", result)

        file_path = os.path.join(self.export_path, "exported_toolpath.gcode")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().splitlines()
        self.assertEqual(content, toolpath_data)  # Ensure file contents match exactly

    def test_export_acspl_success(self):
        """Test exporting a valid ACSPL toolpath for Optomec"""
        exporter = ToolpathExporter(self.export_path, "Optomec")
        toolpath_data = ["!Machine Type - Optomec 5-axis Aerosol Jet", "XSEG/A (10,11,12,14,15)", ""]
        result = exporter.export(toolpath_data)
        self.assertIn("Export successful", result)

        file_path = os.path.join(self.export_path, "exported_toolpath.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().splitlines()
        self.assertEqual(content, toolpath_data)

    def test_export_empty_toolpath(self):
        """Test exporting an empty toolpath, which should fail"""
        result = self.exporter.export([])
        self.assertIn("Error", result)

    def test_export_no_export_path(self):
        """Test handling of missing export path"""
        exporter = ToolpathExporter("", "nScrypt")
        result = exporter.export(["MOVE X10 Y10 Z5 F300"])
        self.assertIn("Error", result)

if __name__ == "__main__":
    unittest.main()
