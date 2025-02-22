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
import guiRoot

import tkinter as tk
import applicationGlobals as globals

class TestGuiButtons(unittest.TestCase):
    def setUp(self):
        self.guiRootObj = guiRoot.GuiRoot()

    def testImport(self):
        importMock = mock.Mock()

        self.guiRootObj.importFileButton.configure(state="normal")
        self.guiRootObj.importFileButton.configure(command = importMock)
        self.guiRootObj.importFileButton.invoke()
        
        importMock.assert_called()
    
    def testExport(self):
        exportMock = mock.Mock()

        self.guiRootObj.exportFileButton.configure(state="normal")
        self.guiRootObj.exportFileButton.configure(command = exportMock)
        self.guiRootObj.exportFileButton.invoke()
        
        exportMock.assert_called()

    def testConvSettings(self):
        convSettingsMock = mock.Mock()

        self.guiRootObj.conversionSettings.configure(state="normal")
        self.guiRootObj.conversionSettings.configure(command = convSettingsMock)
        self.guiRootObj.conversionSettings.invoke()
        
        convSettingsMock.assert_called()

    def testStartConv(self):
        startConvMock = mock.Mock()

        self.guiRootObj.startConvButton.configure(state="normal")
        self.guiRootObj.startConvButton.configure(command = startConvMock)
        self.guiRootObj.startConvButton.invoke()
        
        startConvMock.assert_called()
    
    def testWriteStatus(self):
        self.guiRootObj.clearStatus()
        self.guiRootObj.writeStatus("Alphabetical Characters")
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "Alphabetical Characters\n\n"

        self.guiRootObj.clearStatus()
        self.guiRootObj.writeStatus("Numbers 0123456789")
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "Numbers 0123456789\n\n"

        self.guiRootObj.clearStatus()
        self.guiRootObj.writeStatus("Special Characters `~!@#$%^&*()_+")
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "Special Characters `~!@#$%^&*()_+\n\n"

    def testStatusQueue(self):
        self.guiRootObj.clearStatus()
        globals.writeStatusQueue("TEST1")
        guiRoot.queueLoop(self.guiRootObj) # Have to "artificially" loop through queue 
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "TEST1\n\n"

        self.guiRootObj.clearStatus()
        globals.writeStatusQueue("TEST2")
        guiRoot.queueLoop(self.guiRootObj)
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "TEST2\n\n"

        self.guiRootObj.clearStatus()
        globals.writeStatusQueue("Alphabetical Characters")
        guiRoot.queueLoop(self.guiRootObj)
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "Alphabetical Characters\n\n"

        self.guiRootObj.clearStatus()
        globals.writeStatusQueue("Numbers 0123456789")
        guiRoot.queueLoop(self.guiRootObj)
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "Numbers 0123456789\n\n"

        self.guiRootObj.clearStatus()
        globals.writeStatusQueue("Special Characters `~!@#$%^&*()_+")
        guiRoot.queueLoop(self.guiRootObj)
        assert self.guiRootObj.statusTextArea.get("1.0", tk.END)[11:] == "Special Characters `~!@#$%^&*()_+\n\n"

if __name__ == "__main__":
    unittest.main()