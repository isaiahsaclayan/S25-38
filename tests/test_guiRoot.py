'''
Author: Alvin Chung
Created: 01/31/25
File: guiRoot.py
Description: Testing file for the GUI 
'''

import unittest
from unittest import mock
import sys

sys.path.append("../source/transpiler/")
from guiRoot import GuiRoot
import tkinter as tk

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
    
    def testWriteStatus(self):
        self.guiRootObj.writeStatus("Alphabetical Characters")
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END) == "Alphabetical Characters\n"

        self.guiRootObj.writeStatus("Numbers 0123456789")
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END) == "Numbers 0123456789\n"

        self.guiRootObj.writeStatus("Special Characters `~!@#$%^&*()_+")
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END) == "Special Characters `~!@#$%^&*()_+\n"

if __name__ == "__main__":
    unittest.main()