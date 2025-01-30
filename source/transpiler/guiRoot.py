'''
Author: Alvin Chung
Created: 01/17/24
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import tkinter as tk
from tkinter import filedialog

WINDOW_TITLE = "S25-38" #TODO - Provide suitable titles
MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x300"

class GuiRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False) #Resizing is disabled on both axes
        
        #Title of the window
        self.title(WINDOW_TITLE) 
        self.geometry(GUI_WINDOW_SIZE)

        #Title of Menu
        self.testLabel = tk.Label(self, text = MENU_TITLE)
        self.testLabel.pack(anchor="center")

        #Import button + import filepath
        self.importFrame = tk.Frame(self)

        #Import Button and Label
        self.importFileButton = tk.Button(self.importFrame, text="Import File", command=self.importButtonCallback)
        self.importFileButton.pack(side="left")

        self.importFilepathLabel = tk.Label(self.importFrame)
        self.importFilepathLabel.pack(side="left")

        self.importFrame.pack(anchor="w", padx=5, pady=5)

        #Export button + export filepath
        self.exportFrame = tk.Frame(self)

        #Set Export Destination Button and Label
        self.exportFileButton = tk.Button(self.exportFrame, text="Set Export Destination", command=self.setExportDestinationButtonCallback)
        self.exportFileButton.pack(side="left")

        self.exportFilepathLabel = tk.Label(self.exportFrame)
        self.exportFilepathLabel.pack(side="left")

        self.exportFrame.pack(anchor="w", padx=5, pady=5)

        #Conversion Settings Button
        self.conversionSettings = tk.Button(self, text="Conversion Settings", command=self.conversionSettingsButtonCallback)
        self.conversionSettings.pack(anchor="w", padx=5, pady=5)

        #Start Conversion Button
        self.startConvButton = tk.Button(self, text="Start Conversion", command=self.startConversionButtonCallback)
        self.startConvButton.pack(anchor="center", padx=5, pady=5)

        #Label for Status Text
        self.statusTextArea = tk.Label(self, text="Status:")
        self.statusTextArea.pack(anchor="w", padx=5, pady=5)

        #Status Text Area
        self.statusTextArea = tk.Text(self, wrap=tk.WORD)
        self.statusTextArea.pack(anchor="center", padx=5, pady=5)

    def importButtonCallback(self):
        filetypesList = (("Text Files", '*.txt'), ("All files", "*.*"))
        importFilename = filedialog.askopenfilename(filetypes = filetypesList)
        self.importFilepathLabel["text"] = importFilename
        print("Import Click")

    def setExportDestinationButtonCallback(self):
        filetypesList = (("Text Files", '*.txt'), ("All files", "*.*"))
        exportFilename = filedialog.asksaveasfilename(filetypes = filetypesList)
        self.exportFilepathLabel["text"] = exportFilename
        print("Export Click")

    def startConversionButtonCallback(self):
        print("Start Conversion Click")

    def conversionSettingsButtonCallback(self):
        print("Conversion Settings Click")