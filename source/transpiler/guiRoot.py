'''
Author: Alvin Chung
Created: 01/17/24
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import tkinter as tk
from tkinter import filedialog
from paramClass import Parameters
from paramClass import ParameterGui

WINDOW_TITLE = "S25-38" #TODO - Provide suitable titles
MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x300"

#TODO - Change these to proper extensions
CREO_FILE_TYPE = ("Creo Toolpath Files", '*.ncl.1')
NSCRYPT_FILE_TYPE = ("nScrypt GCODE Files", '*.gcode')
ACSPL_FILE_TYPE = ("ACSPL Files", '*.txt')
IMPORT_FILE_TYPES_LIST = (CREO_FILE_TYPE, NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*"))
EXPORT_FILE_TYPES_LIST = (NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*"))

class GuiRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False) #Resizing is disabled on both axes
        self.params = []
        
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

        #Printer Parameters Button
        self.printParams = tk.Button(self, text="Printer Parameters", command=self.printParamsButtonCallback)
        self.printParams.config(state=tk.DISABLED) #button can't be clicked until file has been imported
        self.printParams.pack(anchor="w", padx=5, pady=5)

        #Start Conversion Button
        self.startConvButton = tk.Button(self, text="Start Conversion", command=self.startConversionButtonCallback)
        self.startConvButton.pack(anchor="center", padx=5, pady=5)

        #Label for Status Text
        self.statusTextArea = tk.Label(self, text="Status:")
        self.statusTextArea.pack(anchor="w", padx=5, pady=5)

        #Status Text Area
        self.statusTextArea = tk.Text(self, wrap=tk.WORD)
        self.statusTextArea.pack(anchor="center", padx=5, pady=5)
        self.statusTextArea.configure(state="disabled") #Prevent user from typing in text box

    def writeStatus(self, text):
        self.statusTextArea.configure(state="normal")   #Enable writing to text box
        self.statusTextArea.delete("1.0", tk.END)       #Clear textbox
        self.statusTextArea.insert(tk.END, text)        #Write new text
        self.statusTextArea.configure(state="disabled") #Disable text box again


    def importButtonCallback(self):
        importFilename = filedialog.askopenfilename(filetypes = IMPORT_FILE_TYPES_LIST)
        self.importFilepathLabel["text"] = importFilename

        self.params = Parameters().params
        self.printParams.config(state=tk.NORMAL) #enables printer parameter button and menu

        self.writeStatus("Import Click")
        print("Import Click")

    def setExportDestinationButtonCallback(self):
        exportFilename = filedialog.asksaveasfilename(filetypes = EXPORT_FILE_TYPES_LIST)
        self.exportFilepathLabel["text"] = exportFilename
        
        self.writeStatus("Export Click")
        print("Export Click")

    def startConversionButtonCallback(self):
        self.writeStatus("Start Conversion Click")
        print("Start Conversion Click")

    def conversionSettingsButtonCallback(self):
        self.writeStatus("Conversion Settings Click")
        print("Conversion Settings Click")

    def printParamsButtonCallback(self):
        self.writeStatus("Printer Parameters Click")
        print("Printer Parameters Click")
        paramWindow = ParameterGui(self)
        paramWindow.eval("tk::PlaceWindow . center")