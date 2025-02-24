import unittest
from unittest import mock
from toolpathExporter import ToolpathExporter

class TestToolpathExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = ToolpathExporter("test_exports", "nScrypt")

    def test_export_gcode(self):
        """Test successful G-Code export"""
        toolpath_data = ["MOVE X10 Y10 Z5 F300", "SET SPEED 100"]
        result = self.exporter.export_with_formatting(toolpath_data)
        self.assertIn("Export Successful", result)

    def test_export_acspl(self):
        """Test successful ACSPL export"""
        exporter = ToolpathExporter("test_exports", "Optomec")
        toolpath_data = ["MOVE 10,10,5", "SPEED 100"]
        result = exporter.export_with_formatting(toolpath_data)
        self.assertIn("Export Successful", result)

    def test_invalid_toolpath_format(self):
        """Test error handling for invalid toolpath format"""
        invalid_toolpath = ["INVALID_COMMAND 123"]
        result = self.exporter.export_with_formatting(invalid_toolpath)
        self.assertIn("Error", result)

    def test_empty_toolpath(self):
        """Test exporting an empty toolpath file"""
        empty_toolpath = []
        result = self.exporter.export_with_formatting(empty_toolpath)
        self.assertIn("Error", result)

    

if __name__ == "__main__":
    unittest.main()
