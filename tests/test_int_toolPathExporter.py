import unittest
from unittest import mock
import os
import sys
from tkinter import messagebox

sys.path.append("../source/transpiler/")
from guiRoot import GuiRoot
from toolpathExporter import ToolpathExporter
from nscryptConverter import NscryptConverter
from acsplConverter import AcsplConverter

class TestIntegrationToolpathExporter(unittest.TestCase):
    def setUp(self):
        self.export_path = "test_exports"
        self.gui = GuiRoot()
        self.nscrypt_converter = NscryptConverter()
        self.acspl_converter = AcsplConverter()
        os.makedirs(self.export_path, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.export_path):
            for file in os.listdir(self.export_path):
                os.remove(os.path.join(self.export_path, file))
            os.rmdir(self.export_path)

    # def test_export_includes_machine_parameters(self):
    #     """Test if ToolpathExporter integrates machine parameters correctly."""
    #     toolpath_data = ["MOVE X10 Y10 Z5", "SPEED 100"]
    #     exporter = ToolpathExporter(self.export_path, "nScrypt")
    #     result = exporter.export(toolpath_data)
    #     self.assertIn("Export successful", result)
        
    #     output_files = os.listdir(self.export_path)
    #     self.assertGreater(len(output_files), 0)
        
    #     with open(os.path.join(self.export_path, output_files[0]), "r") as f:
    #         content = f.read()
    #         self.assertIn("G0 MOVE X10 Y10 Z5", content)
    #         self.assertIn("G0 SPEED 100", content)

    # @mock.patch("tkinter.messagebox.showinfo")
    # def test_export_status_message_shown_in_gui(self, mock_messagebox):
    #     """Test if the GUI displays export status messages correctly."""
    #     self.gui.toolpath_data = ["MOVE X10 Y10 Z5"]
    #     self.gui.export_path = self.export_path
        
    #     self.gui.startConversionButtonCallback()
        
    #     mock_messagebox.assert_called_once()
    #     self.assertIn("Export successful", self.gui.statusTextArea.get("1.0", "end"))

    def test_nscrypt_output_passed_correctly_to_toolpath_export(self):
        """Test if nScrypt converted data is correctly passed to ToolpathExporter."""
        toolpath_data = [{"move": {"x": 10, "y": 10, "z": 5}}]
        converted_data = self.nscrypt_converter.translate(toolpath_data)
        
        exporter = ToolpathExporter(self.export_path, "nScrypt")
        result = exporter.export(converted_data)
        self.assertIn("Export successful", result)

        output_files = os.listdir(self.export_path)
        self.assertGreater(len(output_files), 0)
        
        with open(os.path.join(self.export_path, output_files[0]), "r") as f:
            content = f.read()
            self.assertIn("10.0 10.0 5.0 0.0 0.0", content)

    # def test_acspl_output_passed_correctly_to_toolpath_export(self):
    #     """Test if ACSPL converted data is correctly passed to ToolpathExporter."""
    #     toolpath_data = [{"move": {"x": 10, "y": 10, "z": 5}}]
    #     converted_data = self.acspl_converter.translate(toolpath_data)
        
    #     exporter = ToolpathExporter(self.export_path, "Optomec")
    #     result = exporter.export(converted_data)
    #     self.assertIn("Export successful", result)

    #     output_files = os.listdir(self.export_path)
    #     self.assertGreater(len(output_files), 0)
        
    #     with open(os.path.join(self.export_path, output_files[0]), "r") as f:
    #         content = f.read()
    #         self.assertIn("MOVE 10,10,5", content)

    def test_parser_converter_exporter_integration(self):
        """Test end-to-end integration from parsing -> conversion -> exporting."""
        toolpath_data = [{"move": {"x": 20, "y": 30, "z": 10}}]
        converted_data = self.nscrypt_converter.translate(toolpath_data)
        
        exporter = ToolpathExporter(self.export_path, "nScrypt")
        result = exporter.export(converted_data)
        self.assertIn("Export successful", result)

        output_files = os.listdir(self.export_path)
        self.assertGreater(len(output_files), 0)
        
        with open(os.path.join(self.export_path, output_files[0]), "r") as f:
            content = f.read()
            self.assertIn("20.0 30.0 10.0 0.0 0.0", content)

if __name__ == "__main__":
    unittest.main()
