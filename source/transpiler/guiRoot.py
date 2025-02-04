'''
Author: Alvin Chung
Created: 01/17/25
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import applicationGlobals as globals

WINDOW_TITLE = "S25-38" #TODO - Provide suitable titles
MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x300"

#TODO - Change these to proper extensions
CREO_FILE_TYPE = ("Creo Toolpath Files", '*.ncl.1')
NSCRYPT_FILE_TYPE = ("nScrypt GCODE Files", '*.gcode')
ACSPL_FILE_TYPE = ("ACSPL Files", '*.txt')
IMPORT_FILE_TYPES_LIST = (CREO_FILE_TYPE, NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*"))
EXPORT_FILE_TYPES_LIST = (NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*"))

# CONVERSION_SETTINGS_WINDOW_SIZE = "500x300"

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
        self.statusTextArea.configure(state="disabled") #Prevent user from typing in text box

    def writeStatus(self, text):
        self.statusTextArea.configure(state="normal")   #Enable writing to text box
        self.statusTextArea.delete("1.0", tk.END)       #Clear textbox
        self.statusTextArea.insert(tk.END, text)        #Write new text
        self.statusTextArea.configure(state="disabled") #Disable text box again


    def importButtonCallback(self):
        importFilename = filedialog.askopenfilename(filetypes = IMPORT_FILE_TYPES_LIST)
        self.importFilepathLabel["text"] = importFilename

         #TODO - Remove, placeholders
        self.writeStatus("Import Click")
        print("Import Click")

    def setExportDestinationButtonCallback(self):
        exportFilename = filedialog.asksaveasfilename(filetypes = EXPORT_FILE_TYPES_LIST)
        self.exportFilepathLabel["text"] = exportFilename
        
        #TODO - Remove, placeholders
        self.writeStatus("Export Click")
        print("Export Click")

    def startConversionButtonCallback(self):

        #TODO - Remove, placeholders
        self.writeStatus("Start Conversion Click")
        print("Start Conversion Click")

    def conversionSettingsButtonCallback(self):
        
        #TODO - Remove, placeholders
        self.writeStatus("Conversion Settings Click")
        print("Conversion Settings Click")

        #Create new window
        convSettingsWindow = tk.Toplevel()
        self.eval("tk::PlaceWindow {} center".format(str(convSettingsWindow)))

        convSettingsWindow.title("Conversion Settings")
        # convSettingsWindow.geometry(CONVERSION_SETTINGS_WINDOW_SIZE)
        convSettingsWindow.resizable(False, False)

        convSettingsFrame = ConversionSettingsFrame(convSettingsWindow)
        convSettingsFrame.pack()

        convSettingsWindow.wait_window()

        #TODO - Prevent user from opening another window/interacting with main menu until conversion settings are closed

class ConversionSettingsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.titleLabel = tk.Label(self, text= "Conversion Settings")
        self.titleLabel.pack(padx=10, pady=10)
        
        self.printerTypeSelectFrame = tk.Frame(self)

        self.printTypeSelectLabel = tk.Label(self.printerTypeSelectFrame, text="Printer Type: ") 
        self.printTypeSelectLabel.pack(side="left")

        self.printerTypeCombobox = ttk.Combobox(self.printerTypeSelectFrame, values = globals.PRINTER_TYPES, state="readonly")
        self.printerTypeCombobox.current(0)
        self.printerTypeCombobox.pack(side="left")

        self.printerTypeSelectFrame.pack(padx=10, pady=10)

        self.saveButton = tk.Button(self, text="Save", command=self.saveButtonCallback)

        self.saveButton.pack(padx=10, pady=10)

    def saveButtonCallback(self):
        globals.printerTypeSelected = self.printerTypeCombobox.current() #Set global value
        selectedPrinter = globals.PRINTER_TYPES[globals.printerTypeSelected] #Get corresponding string 

        self.master.master.writeStatus("Save Button Click " + selectedPrinter) #TODO - Replace with message queue system
        #TODO - Close window after saving? - Change to "Save and Exit"
        print("Save Button Click", selectedPrinter)