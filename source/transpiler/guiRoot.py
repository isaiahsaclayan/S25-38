'''
Author: Alvin Chung
Created: 01/17/25
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import tkinter as tk
from tkinter import filedialog, messagebox
from paramClass import NscryptParameters, OptomecParameters
from paramClass import NscryptParameterGui, OptomecParameterGui
from tkinter import ttk
import applicationGlobals as globals
import time
from toolpathExporter import ToolpathExporter  # Import ToolpathExporter
import json

WINDOW_TITLE = "S25-38"  # TODO - Provide suitable titles
MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x300"

QUEUE_LOOP_RATE = 100

# File Types
CREO_FILE_TYPE = ("Creo Toolpath Files", '*.ncl.1')
NSCRYPT_FILE_TYPE = ("nScrypt GCODE Files", '*.gcode')
ACSPL_FILE_TYPE = ("ACSPL Files", '*.txt')
IMPORT_FILE_TYPES_LIST = [CREO_FILE_TYPE, ("All files", "*.*")]
EXPORT_FILE_TYPES_LIST = [("All files", "*.*")]


class GuiRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False)  # Resizing is disabled on both axes
        
        #for the use of parameter subsystem
        self.params = []
        self.hasProfile = False
        self.importFilename = ""

        self.toolpath_data = None
        self.export_path = ""

        # Title of the window
        self.title(WINDOW_TITLE)
        self.geometry(GUI_WINDOW_SIZE)

        # Title of Menu
        self.menuTitleLabel = tk.Label(self, text=MENU_TITLE)
        self.menuTitleLabel.pack(anchor="center")

        # Import button + import filepath
        self.importFrame = tk.Frame(self)

        # Import Button and Label
        self.importFileButton = tk.Button(self.importFrame, text="Select Import File", command=self.importButtonCallback)
        self.importFileButton.pack(side="left")

        self.importFilepathLabel = tk.Label(self.importFrame)
        self.importFilepathLabel.pack(side="left")

        self.importFrame.pack(anchor="w", padx=5, pady=5)

        # Export button + export filepath
        self.exportFrame = tk.Frame(self)

        # Set Export Destination Button and Label
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

        # Label for Status Text
        self.statusTextArea = tk.Label(self, text="Status:")
        self.statusTextArea.pack(anchor="w", padx=5, pady=5)

        # Status Text Area
        self.statusTextArea = tk.Text(self, wrap=tk.WORD)
        self.statusTextArea.pack(anchor="center", padx=5, pady=5)
        self.statusTextArea.configure(state="disabled")  # Prevent user from typing in text box

    def writeStatus(self, text):
        self.statusTextArea.configure(state="normal")   # Enable writing to text box
        self.statusTextArea.delete("1.0", tk.END)       # Clear textbox

        # Adding timestamp to status message
        currentTime = time.localtime()
        
        timeString = "[{}:{}:{}]".format(currentTime.tm_hour, currentTime.tm_min, currentTime.tm_sec)

        fullText = timeString + " " + text

        self.statusTextArea.insert(tk.END, fullText)        # Write new text
        self.statusTextArea.configure(state="disabled") # Disable text box again

    '''
    Function that is called when the "Select Import File" button is clicked
    '''
    def importButtonCallback(self):

        # Opens a dialog for user to select a file to import
        filepath = filedialog.askopenfilename(filetypes = IMPORT_FILE_TYPES_LIST, defaultextension = IMPORT_FILE_TYPES_LIST[0])

        # User Cancels File Selection
        # If the user clicks the cancel button, an empty string is returned
        if(len(filepath) == 0): 
            self.writeStatus("Select Import File Cancelled")

        # A file is selected successfully in the file dialog
        else:
            
            # The file dialog already handles when the user tries to input an invalid file name
            # for redundancy, check if the file can be opened

            try:     
                openedFile = open(file = filepath, mode="r")
                openedFile.close()

                self.writeStatus("Select Import File Successful")
                globals.setImportFilepath(filepath) # Store import filepath
                self.importFilepathLabel["text"] = filepath
                

            except:
                self.writeStatus("Select Import File Error: Unable to Open File")
                self.importFilepathLabel["text"] = filepath

        #first try to open param file, if fail then create the settings file and begin append
        try:
            settingsData = json.loads(open("parameters.json").read())
            #look to see if the opened/imported file is listed in the savedParams file
            #file format is as follows:
            # name_of_file_first: [Optomec/nScrypt, [param1 param2 param3 param4]]
            try:
                jdata = settingsData[self.importFilename]
                self.writeStatus("Found existing parameter profile")
                print("Found existing parameter profile")
                globals.printerTypeSelected = jdata[0] #will equal 0 for nscrypt, 1 for optomec
                if globals.printerTypeSelected == 0:
                    self.params = NscryptParameters()
                elif globals.printerTypeSelected == 1:
                    self.params = OptomecParameters()
                self.params.params = jdata[1]
                self.hasProfile = True
            except (KeyError, json.decoder.JSONDecodeError):
                self.writeStatus("No existing parameter profile")
                print("No existing parameter profile")
                #do the same thing here as file not found, so we append to json later
                self.hasProfile = False
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.writeStatus("No existing parameter profile")
            print("No existing parameter profile")
            #something should happen here such that we make sure to creat the json later
            self.hasProfile = False
        self.writeStatus("Import Click")
        print("Import Click")

    '''
    Function that is called when the "Set Export Destination" button is clicked
    '''
    def setExportDestinationButtonCallback(self):

        # Opens a dialog for user to set a filename and path for export
        filepath = filedialog.asksaveasfilename(filetypes = EXPORT_FILE_TYPES_LIST, defaultextension = EXPORT_FILE_TYPES_LIST[0])
        self.exportFilepathLabel["text"] = filepath

        # User cancels setting export destination
        # If the user clicks the cancel button, an empty string is returned
        if(len(filepath) == 0): 
            self.writeStatus("Set Export Destination Cancelled")

        # User sets export filepath
        else:
            globals.setExportFilepath(filepath) # Store export filepath
            self.writeStatus("Set Export Destination Successful")

    def startConversionButtonCallback(self):
        if not self.toolpath_data:
            messagebox.showerror("Error", "No toolpath imported!")
            return

        if not self.export_path:
            messagebox.showerror("Error", "No export destination set!")
            return

        # Determine printer type
        printer_type = globals.PRINTER_TYPES[globals.printerTypeSelected]
        exporter = ToolpathExporter(self.export_path, printer_type)

        # Export toolpath
        result = exporter.export_with_formatting(self.toolpath_data)

        # Display feedback
        if "Error" in result:
            messagebox.showerror("Export Failed", result)
        else:
            messagebox.showinfo("Success", result)

        self.writeStatus(result)

    def conversionSettingsButtonCallback(self):
        self.writeStatus("Conversion Settings Click")
        print("Conversion Settings Click")

        # Create new window
        convSettingsWindow = tk.Toplevel()
        self.eval("tk::PlaceWindow {} center".format(str(convSettingsWindow)))

        convSettingsWindow.title("Conversion Settings")
        convSettingsWindow.resizable(False, False)

        convSettingsFrame = ConversionSettingsFrame(convSettingsWindow)
        convSettingsFrame.pack()

        convSettingsWindow.wait_window()

        #save/set which parameter type after window is closed
        if globals.printerTypeSelected == 0 and self.hasProfile == False: #this way if someone already has a param profile
                                                                            #it wont be overwritten
            self.params = NscryptParameters()
        elif globals.printerTypeSelected == 1: #dont check for previous profile. We are trusting that even if they had previous profile, if they intentionally select this
                #then they are intending to discard their old profile
            self.params = OptomecParameters()
        self.printParams.config(state=tk.NORMAL)  # enables printer parameter button and menu

    def printParamsButtonCallback(self):
        self.writeStatus("Printer Parameters Click")
        print("Printer Parameters Click")
        paramWindow = tk.Toplevel()
        self.eval("tk::PlaceWindow {} center".format(str(paramWindow)))

        paramWindow.geometry("500x250")
        paramWindow.resizable(False, False)

        if globals.printerTypeSelected == 0:
            paramWindow.title("nScrypt Parameters")
            paramFrame = NscryptParameterGui(paramWindow, self)
        else:
            paramWindow.title("Optomec Parameters")
            paramFrame = OptomecParameterGui(paramWindow, self)

            paramFrame = NscryptParameterGui(paramWindow, self)
        
        paramFrame.grid()
        paramWindow.wait_window()
        #after wait window close need to save new params to file, or need to modify old saved params
        if self.hasProfile == False:
            try:
                try:
                    with open("parameters.json", "r") as settingsFile:
                        prevData = json.load(settingsFile)
                        found = True
                except json.decoder.JSONDecodeError:
                    found = False
            except FileNotFoundError:
                print("Creating new settings file")
                found = False
            with open("parameters.json", "w") as settingsFile:
                jdata = {
                        self.importFilename: [globals.printerTypeSelected, self.params.params]
                }
                if found:
                    prevData.update(jdata)
                    json.dump(prevData, settingsFile)
                else:
                    json.dump(jdata, settingsFile)
                settingsFile.close()
        else:
            #easiest way to update an entry is to write over the whole file, with the one entry updated
            with open("parameters.json", 'r') as settingsFile:
                prevData = json.load(settingsFile)
                del prevData[self.importFilename]
                settingsFile.close()
            jdata = {
                        self.importFilename: [globals.printerTypeSelected, self.params.params]
                }
            prevData.update(jdata)
            with open("parameters.json", "w") as settingsFile:
                json.dump(prevData, settingsFile)



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

        self.printerTypeSelectFrame.pack(padx=50, pady=50)

        #relates to if there are previously saved params or not
        if parent.master.hasProfile == False:
            self.savedSettingsStatusLabel = tk.Label(self.printerTypeSelectFrame, text="No previously saved settings, safe to choose")
        else:
            self.savedSettingsStatusLabel = tk.Label(self.printerTypeSelectFrame, text="There are pre-existing saved settings for the imported file, selecting printer type will override")
        self.savedSettingsStatusLabel.pack(side="left")
        self.saveButton = tk.Button(self, text="Save", command=self.saveButtonCallback)
        self.saveButton.pack(padx=10, pady=10)

    def saveButtonCallback(self):
        globals.printerTypeSelected = self.printerTypeCombobox.current()
        selectedPrinter = globals.PRINTER_TYPES[globals.printerTypeSelected]

        globals.writeStatusQueue("Save Button Click " + selectedPrinter)
        print("Save Button Click", selectedPrinter)


def queueLoop(rootObject):
    while True:
        try:
            message = globals.statusQueue.get(block=False)
            rootObject.writeStatus(message)
        except globals.queue.Empty:
            break
    rootObject.after(QUEUE_LOOP_RATE, queueLoop, rootObject)
