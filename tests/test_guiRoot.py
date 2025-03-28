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

'''
Helper function to easily test different strings
for testing internally, when writing directly to status within the GUI, set internal to true
for testing with the status queue, set internal to false
'''
def testStatusWithString(testString, guiRootObject, internal):
    guiRootObject.clearStatus()

    match (internal):
        case True:
            guiRootObject.writeStatus(testString)
            
        case False:
            globals.writeStatusQueue(testString)
            guiRoot.queueLoop(guiRootObject) # Have to "artificially" loop through queue
        case _:
            raise ValueError("Invalid Value for \"internal\"")
    
    testStartIndex = len(testString) * -1

    receivedString = guiRootObject.statusTextArea.get("1.0", tk.END).strip()    # Get string from status area, remove whitespace(including newline characters)
    receivedString = receivedString[testStartIndex:]                            # Extract only the target string

    assert  testString == receivedString # Check

class TestGuiRoot(unittest.TestCase):
    def setUp(self):
        self.guiRootObj = guiRoot.GuiRoot()
        self.testStringList = ["TEST1", "TEST2", "Alphabetical Characters", "Numbers 0123456789", "Special Characters `~!@#$%^&*()_+"]
        guiRoot.queueLoop(self.guiRootObj)
        self.guiRootObj.clearStatus()
    
    '''
    Test Select Import File Button
    '''
    def test_Import(self):
        importMock = mock.Mock()

        self.guiRootObj.importFileButton.configure(state="normal")
        self.guiRootObj.importFileButton.configure(command = importMock)
        self.guiRootObj.importFileButton.invoke()
        
        importMock.assert_called()
    
    '''
    Test Set Export Destination Button
    '''
    def test_Export(self):
        exportMock = mock.Mock()

        self.guiRootObj.exportFileButton.configure(state="normal")
        self.guiRootObj.exportFileButton.configure(command = exportMock)
        self.guiRootObj.exportFileButton.invoke()
        
        exportMock.assert_called()

    '''
    Test Conversion Settings Button
    '''
    def test_ConvSettings(self):
        convSettingsMock = mock.Mock()

        self.guiRootObj.conversionSettings.configure(state="normal")
        self.guiRootObj.conversionSettings.configure(command = convSettingsMock)
        self.guiRootObj.conversionSettings.invoke()
        
        convSettingsMock.assert_called()
    
    '''
    Test Start Conversion Button
    '''
    def test_StartConv(self):
        startConvMock = mock.Mock()

        self.guiRootObj.startConvButton.configure(state="normal")
        self.guiRootObj.startConvButton.configure(command = startConvMock)
        self.guiRootObj.startConvButton.invoke()
        
        startConvMock.assert_called()

    '''
    Test the internal writeStatus() function
    '''
    def test_WriteStatus(self):
        for string in self.testStringList:
            testStatusWithString(string, self.guiRootObj, internal=True)

    '''
    Test writing to the status area via the status queue
    '''
    def test_StatusQueue(self):
        for string in self.testStringList:
            testStatusWithString(string, self.guiRootObj, internal=False)

if __name__ == "__main__":
    unittest.main()