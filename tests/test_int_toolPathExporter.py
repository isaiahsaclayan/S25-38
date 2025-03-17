import unittest
import os
import tempfile
from guiRoot import GuiRoot
from toolpathExporter import ToolpathExporter

class TestIntegrationToolpathExporter(unittest.TestCase):
    def setUp(self):
        """Set up a GUI root object and temporary directory for integration testing."""
        self.guiRootObj = GuiRoot()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.guiRootObj.export_path = self.temp_dir.name
        self.exporter = ToolpathExporter(self.temp_dir.name, "nScrypt")

    def tearDown(self):
        """Clean up resources after tests."""
        self.temp_dir.cleanup()

    def test_full_import_export_cycle(self):
        """Test full cycle from import to export."""
        # Simulate toolpath import
        self.guiRootObj.toolpath_data = ["MOVE X10 Y10 Z5", "SET SPEED 200"]
        
        # Run the export function
        self.guiRootObj.startConversionButtonCallback()

        # Check if a valid file was created
        exported_files = os.listdir(self.temp_dir.name)
        self.assertTrue(any(file.startswith("nScrypt_toolpath") and file.endswith(".gcode") for file in exported_files))

    def test_error_handling_integration(self):
        """Ensure errors are handled correctly when exporting without import."""
        self.guiRootObj.toolpath_data = None
        self.guiRootObj.startConversionButtonCallback()
        assert "No toolpath imported" in self.guiRootObj.statusTextArea.get("1.0", "end")

if __name__ == "__main__":
    unittest.main()
