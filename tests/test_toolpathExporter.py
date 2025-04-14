import unittest
import os
import sys

# Get absolute path to the source/transpiler directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../source/transpiler"))
sys.path.insert(0, BASE_DIR)  # Insert at the beginning of sys.path
from toolpathExporter import ToolpathExporter

class TestToolpathExporter(unittest.TestCase):
    def setUp(self):
        self.tempDir = "tempDir"
        os.makedirs(self.tempDir, exist_ok=True)

    def tearDown(self):
        # Cleanup exported files after each test
        for file in os.listdir(self.tempDir):
            os.remove(os.path.join(self.tempDir, file))
        os.rmdir(self.tempDir)

    def test_export_success(self):
        """Test exporting a valid toolpath for nScrypt"""
        filepath = self.tempDir + "/exported_toolpath.nff"
        exporter = ToolpathExporter(filepath, "nScrypt")
        toolpath_data = ["MOVE X10 Y10 Z5 F300", "SET SPEED 100", ""]  # Includes empty line
        result = exporter.export(toolpath_data)
        self.assertIn("Export successful", result)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().splitlines()
        self.assertEqual(content, toolpath_data)  # Ensure file contents match exactly

    def test_export_acspl_success(self):
        """Test exporting a valid ACSPL toolpath for Optomec"""
        filepath = self.tempDir + "/exported_toolpath.prg"
        exporter = ToolpathExporter(filepath, "Optomec")
        toolpath_data = ["!Machine Type - Optomec 5-axis Aerosol Jet", "XSEG/A (10,11,12,14,15)", ""]
        result = exporter.export(toolpath_data)
        self.assertIn("Export successful", result)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().splitlines()
        self.assertEqual(content, toolpath_data)

    def test_export_empty_toolpath(self):
        """Test exporting an empty toolpath, which should fail"""
        filepath = self.tempDir + "/test_empty.nff"
        exporter = ToolpathExporter(filepath, "nScrypt")
        result = exporter.export([])
        self.assertIn("Error", result)

    def test_export_no_export_path(self):
        """Test handling of missing export path"""
        exporter = ToolpathExporter("", "nScrypt")
        result = exporter.export(["MOVE X10 Y10 Z5 F300"])
        self.assertIn("Error", result)

if __name__ == "__main__":
    unittest.main()
