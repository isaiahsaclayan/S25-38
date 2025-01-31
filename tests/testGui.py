import unittest
from unittest import mock
import sys

sys.path.append("../source/transpiler/")
from guiRoot import GuiRoot

class TestGuiButtons(unittest.TestCase):
    def setUp(self):
        self.guiRootObj = GuiRoot()

    def testImport(self):
        importMock = mock.Mock()

        self.guiRootObj.importFileButton.configure(command = importMock)
        self.guiRootObj.importFileButton.invoke()
        
        importMock.assert_called()
    
    def testExport(self):
        exportMock = mock.Mock()

        self.guiRootObj.exportFileButton.configure(command = exportMock)
        self.guiRootObj.exportFileButton.invoke()
        
        exportMock.assert_called()

    def testConvSettings(self):
        convSettingsMock = mock.Mock()

        self.guiRootObj.conversionSettings.configure(command = convSettingsMock)
        self.guiRootObj.conversionSettings.invoke()
        
        convSettingsMock.assert_called()

    def testStartConv(self):
        startConvMock = mock.Mock()

        self.guiRootObj.startConvButton.configure(command = startConvMock)
        self.guiRootObj.startConvButton.invoke()
        
        startConvMock.assert_called()
    
if __name__ == "__main__":
    unittest.main()