import unittest
import os
import sys

# Append the source directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../source/transpiler")))

from parser import GenericParser
from acsplConverter import AcsplConverter
from nscryptConverter import NscryptConverter
from toolpathExporter import ToolpathExporter

class TestToolpathExporter(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.export_path = "test_exports"
        os.makedirs(self.export_path, exist_ok=True)

        self.exporter_gcode = ToolpathExporter(self.export_path, "nScrypt")
        self.exporter_acspl = ToolpathExporter(self.export_path, "Optomec")

        self.parser = GenericParser("tests/resources/sample_toolpath.ncl.1")  # Mock input file
        self.converter_gcode = NscryptConverter()
        self.converter_acspl = AcsplConverter()

    def tearDown(self):
        """Clean up generated files"""
        for file in os.listdir(self.export_path):
            os.remove(os.path.join(self.export_path, file))
        os.rmdir(self.export_path)

    ### UNIT TESTS ###

    def test_export_gcode(self):
        """Test successful G-Code export"""
        toolpath_data = ["MOVE X10 Y10 Z5 F300", "SET SPEED 100"]
        result = self.exporter_gcode.export_with_formatting(toolpath_data)
        self.assertIn("Export successful", result)

    def test_export_acspl(self):
        """Test successful ACSPL export"""
        toolpath_data = ["MOVE 10,10,5", "SPEED 100"]
        result = self.exporter_acspl.export_with_formatting(toolpath_data)
        self.assertIn("Export successful", result)

    def test_invalid_toolpath_format(self):
        """Test error handling for invalid toolpath format"""
        invalid_toolpath = ["INVALID_COMMAND 123"]
        result = self.exporter_gcode.export_with_formatting(invalid_toolpath)
        self.assertIn("Error", result)

    def test_empty_toolpath(self):
        """Test exporting an empty toolpath file"""
        empty_toolpath = []
        result = self.exporter_gcode.export_with_formatting(empty_toolpath)
        self.assertIn("Error", result)

    def test_toolpath_file_creation(self):
        """Test if the toolpath file is actually created"""
        toolpath_data = ["G1 X10 Y20 Z30"]
        self.exporter_gcode.export_with_formatting(toolpath_data)

        expected_file = os.path.join(self.export_path, "exported_toolpath.gcode")
        self.assertTrue(os.path.exists(expected_file))

    def test_invalid_printer_type(self):
        """Test if an invalid printer type is handled properly"""
        exporter = ToolpathExporter(self.export_path, "InvalidPrinter")
        toolpath_data = ["MOVE X10 Y10 Z5"]
        result = exporter.export_with_formatting(toolpath_data)
        self.assertIn("Error", result)

    ### INTEGRATION TESTS ###

    def test_integration_gcode(self):
        """Test full flow from parsing to exporting G-Code"""
        parsed_toolpath = self.parser.parse_commands()
        converted_toolpath = self.converter_gcode.translate(parsed_toolpath)
        result = self.exporter_gcode.export_with_formatting(converted_toolpath)

        # Check if export is successful
        self.assertIn("Export successful", result)

        # Verify if file was created
        expected_file = os.path.join(self.export_path, "exported_toolpath.gcode")
        self.assertTrue(os.path.exists(expected_file))

    def test_integration_acspl(self):
        """Test full flow from parsing to exporting ACSPL"""
        parsed_toolpath = self.parser.parse_commands()
        converted_toolpath = self.converter_acspl.translate(parsed_toolpath)
        result = self.exporter_acspl.export_with_formatting(converted_toolpath)

        # Check if export is successful
        self.assertIn("Export successful", result)

        # Verify if file was created
        expected_file = os.path.join(self.export_path, "exported_toolpath.txt")
        self.assertTrue(os.path.exists(expected_file))

    def test_integration_invalid_parser(self):
        """Test handling of an invalid parser output"""
        invalid_parser = GenericParser("tests/resources/invalid_toolpath.ncl.1")
        parsed_toolpath = invalid_parser.parse_commands()
        
        result_gcode = self.exporter_gcode.export_with_formatting(parsed_toolpath)
        result_acspl = self.exporter_acspl.export_with_formatting(parsed_toolpath)

        self.assertIn("Error", result_gcode)
        self.assertIn("Error", result_acspl)

    def test_integration_incomplete_toolpath(self):
        """Test handling of an incomplete toolpath"""
        incomplete_toolpath = [{"move": {"x": 10, "y": 20}}]  # Missing required parameters
        result = self.exporter_gcode.export_with_formatting(incomplete_toolpath)

        self.assertIn("Error", result)

if __name__ == "__main__":
    unittest.main()
