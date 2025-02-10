'''
Author: Alvin Chung
Created: 01/17/25
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import os
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
from paramClass import Parameters
from paramClass import ParameterGui
from tkinter import ttk
import applicationGlobals as globals
from toolpathExporter import ToolpathExporter  # Import the new exporter subsystem

WINDOW_TITLE = "S25-38"  # TODO - Provide suitable titles
MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x300"

# TODO - Change these to proper extensions
CREO_FILE_TYPE = ("Creo Toolpath Files", '*.ncl.1')
NSCRYPT_FILE_TYPE = ("nScrypt GCODE Files", '*.gcode')
ACSPL_FILE_TYPE = ("ACSPL Files", '*.txt')
IMPORT_FILE_TYPES_LIST = (CREO_FILE_TYPE, NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*")) 
EXPORT_FILE_TYPES_LIST = (NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*"))

class GuiRoot(tk.Tk):
    """
    Root class for the GUI, handling toolpath import, export, and conversion settings.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False)  # Resizing is disabled on both axes
        self.params = []
        self.export_path = ""  # Store export file path
        self.toolpath_data = None  # Store imported toolpath data
        self.printer_type = "nScrypt"  # Default printer type

        # Title of the window
        self.title(WINDOW_TITLE)
        self.geometry(GUI_WINDOW_SIZE)

        # Title of Menu
        self.testLabel = tk.Label(self, text=MENU_TITLE)
        self.testLabel.pack(anchor="center")

        # Import button + import filepath
        self.importFrame = tk.Frame(self)
        self.importFileButton = tk.Button(self.importFrame, text="Import File", command=self.importButtonCallback)
        self.importFileButton.pack(side="left")

        self.importFilepathLabel = tk.Label(self.importFrame)
        self.importFilepathLabel.pack(side="left")

        self.importFrame.pack(anchor="w", padx=5, pady=5)

        # Export button + export filepath
        self.exportFrame = tk.Frame(self)
        self.exportFileButton = tk.Button(self.exportFrame, text="Set Export Destination", command=self.setExportDestinationButtonCallback)
        self.exportFileButton.pack(side="left")

        self.exportFilepathLabel = tk.Label(self.exportFrame)
        self.exportFilepathLabel.pack(side="left")

        self.exportFrame.pack(anchor="w", padx=5, pady=5)

        # Conversion Settings Button
        self.conversionSettings = tk.Button(self, text="Conversion Settings", command=self.conversionSettingsButtonCallback)
        self.conversionSettings.pack(anchor="w", padx=5, pady=5)

        # Printer Parameters Button
        self.printParams = tk.Button(self, text="Printer Parameters", command=self.printParamsButtonCallback)
        self.printParams.config(state=tk.DISABLED)  # button can't be clicked until file has been imported
        self.printParams.pack(anchor="w", padx=5, pady=5)

        # Start Conversion Button
        self.startConvButton = tk.Button(self, text="Start Conversion", command=self.startConversionButtonCallback)
        self.startConvButton.pack(anchor="center", padx=5, pady=5)

        # Start Export Button (New)
        self.startExportButton = tk.Button(self, text="Start Export", command=self.startExportButtonCallback)
        self.startExportButton.pack(anchor="center", padx=5, pady=5)

        # Label for Status Text
        self.statusTextArea = tk.Label(self, text="Status:")
        self.statusTextArea.pack(anchor="w", padx=5, pady=5)

        # Status Text Area
        self.statusTextArea = tk.Text(self, wrap=tk.WORD)
        self.statusTextArea.pack(anchor="center", padx=5, pady=5)
        self.statusTextArea.configure(state="disabled")  # Prevent user from typing in text box

    def writeStatus(self, text):
        """ Updates the status text box in the GUI. """
        self.statusTextArea.configure(state="normal")  # Enable writing to text box
        self.statusTextArea.delete("1.0", tk.END)  # Clear textbox
        self.statusTextArea.insert(tk.END, text)  # Write new text
        self.statusTextArea.configure(state="disabled")  # Disable text box again

    def importButtonCallback(self):
        """ Handles toolpath file import. """
        importFilename = filedialog.askopenfilename(filetypes=IMPORT_FILE_TYPES_LIST)
        self.importFilepathLabel["text"] = importFilename

        if importFilename:
            with open(importFilename, "r", encoding="utf-8") as file:
                self.toolpath_data = file.readlines()

        self.writeStatus("File Imported: " + importFilename)
        self.printParams.config(state=tk.NORMAL)  # Enables printer parameter button and menu

    def setExportDestinationButtonCallback(self):
        """ Sets the export file destination. """
        exportFilename = filedialog.asksaveasfilename(filetypes=EXPORT_FILE_TYPES_LIST)
        self.exportFilepathLabel["text"] = exportFilename
        self.export_path = exportFilename  # Store the path

        self.writeStatus("Export Path Set: " + exportFilename)

    def startConversionButtonCallback(self):
        """ Placeholder function for initiating conversion. """
        self.writeStatus("Start Conversion Clicked")

    def conversionSettingsButtonCallback(self):
        """ Handles opening conversion settings window. """
        self.writeStatus("Conversion Settings Clicked")
        convSettingsWindow = tk.Toplevel()
        self.eval("tk::PlaceWindow {} center".format(str(convSettingsWindow)))

        convSettingsWindow.title("Conversion Settings")
        convSettingsWindow.resizable(False, False)

        convSettingsFrame = ConversionSettingsFrame(convSettingsWindow)
        convSettingsFrame.pack()

        convSettingsWindow.wait_window()

    def printParamsButtonCallback(self):
        """ Opens the printer parameters window. """
        self.writeStatus("Printer Parameters Clicked")
        paramWindow = ParameterGui(self)
        paramWindow.eval("tk::PlaceWindow . center")

    def startExportButtonCallback(self):
        """ Starts the export process using the Toolpath Exporter subsystem. """
        if not self.toolpath_data:
            messagebox.showerror("Error", "No toolpath imported!")
            return

        if not self.export_path:
            messagebox.showerror("Error", "No export destination set!")
            return

        # Determine the selected printer type
        self.printer_type = globals.PRINTER_TYPES[globals.printerTypeSelected]

        # Initialize the exporter
        exporter = ToolpathExporter(self.export_path, self.printer_type)
        result = exporter.export_with_formatting(self.toolpath_data)

        # Provide feedback to the user
        if "Error" in result:
            messagebox.showerror("Export Failed", result)
        else:
            messagebox.showinfo("Success", result)

        self.writeStatus(result)

class ConversionSettingsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.titleLabel = tk.Label(self, text="Conversion Settings")
        self.titleLabel.pack(padx=10, pady=10)

        self.printerTypeSelectFrame = tk.Frame(self)

        self.printTypeSelectLabel = tk.Label(self.printerTypeSelectFrame, text="Printer Type: ")
        self.printTypeSelectLabel.pack(side="left")

        self.printerTypeCombobox = ttk.Combobox(self.printerTypeSelectFrame, values=globals.PRINTER_TYPES, state="readonly")
        self.printerTypeCombobox.current(0)
        self.printerTypeCombobox.pack(side="left")

        self.printerTypeSelectFrame.pack(padx=10, pady=10)

        self.saveButton = tk.Button(self, text="Save", command=self.saveButtonCallback)
        self.saveButton.pack(padx=10, pady=10)

    def saveButtonCallback(self):
        globals.printerTypeSelected = self.printerTypeCombobox.current()
        selectedPrinter = globals.PRINTER_TYPES[globals.printerTypeSelected]
        self.master.master.writeStatus("Save Button Clicked: " + selectedPrinter)

if __name__ == "__main__":
    app = GuiRoot()
    app.mainloop()
