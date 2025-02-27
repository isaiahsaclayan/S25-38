'''
Author: Alvin Chung
Created: 01/17/25
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import tkinter as tk
from tkinter import filedialog
from paramClass import NscryptParameters, OptomecParameters
from paramClass import NscryptParameterGui, OptomecParameterGui
from tkinter import ttk
import applicationGlobals as globals

WINDOW_TITLE = "S25-38" #TODO - Provide suitable titles
MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x300"

# CONVERSION_SETTINGS_WINDOW_SIZE = "500x300"

#TODO - Change these to proper extensions
CREO_FILE_TYPE = ("Creo Toolpath Files", '*.ncl.1')
NSCRYPT_FILE_TYPE = ("nScrypt GCODE Files", '*.gcode')
ACSPL_FILE_TYPE = ("ACSPL Files", '*.txt')
IMPORT_FILE_TYPES_LIST = (CREO_FILE_TYPE, NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*"))
EXPORT_FILE_TYPES_LIST = (NSCRYPT_FILE_TYPE, ACSPL_FILE_TYPE, ("All files", "*.*"))

QUEUE_LOOP_RATE = 100

class GuiRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False) #Resizing is disabled on both axes
        self.params = []
        self.saved_line = -1 #necessary for parameter saving functionality
        
        #Title of the window
        self.title(WINDOW_TITLE) 
        self.geometry(GUI_WINDOW_SIZE)

        #Title of Menu
        self.menuTitleLabel = tk.Label(self, text = MENU_TITLE)
        self.menuTitleLabel.pack(anchor="center")

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

         #TODO - Remove, placeholders
        #first try to open file, if fail then create the settings file and begin append
        try:
            with open("savedParams.txt", 'r') as settingsFile:
                #proceed parse here, look to see if the opened/imported file is listed in the savedParams file
                #file format is as follows:
                # name_of_file_first Optomec/nScrypt param1 param2 param3 param4 \n
                #each line will follow suit if a parse error occurs, it will discard the whole savedParams file
                #and the params for the current imported file will be saved as the only params
                #this should only happen if someone has manually gone in and changed the .txt file
                self.saved_line = -1 #later we will check to see if saved_line is different than -1, if it is then we know
                                #that the file had saved settings, so we know to update those settings instead of appending
                                #new settings
                temp_line = 0
                for line in settingsFile:
                    words = line.split(' ')
                    if words[0] == self.importFilepathLabel:
                        self.saved_line = temp_line
                        #at this point, import params data from savedParams
                        if words[1] == "nscrypt":
                            globals.printerTypeSelected = 0
                            self.params = NscryptParameters()
                        elif words[1] == "optomec":
                            globals.printerTypeSelected = 1
                            self.params = OptomecParameters()
                        #TODO add an elif for error handle
                        for i in range(self.params.params.size()):
                            self.params.params[i] = words[2+i] #first 2 words are the imported file and Optomec/Nscrypt
                        break #we found the file saved in settings, stop looking through the file now
                    else:
                        temp_line += 1
            settingsFile.close()
        except FileNotFoundError:
            #there is no settings file yet, so when we open file later, a new file will be created
            #make sure to mimic the above process where it is found but imported file is not yet saved
            self.saved_line = -1
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

        #save/set which parameter type after window is closed
        if globals.printerTypeSelected == 0:
            self.params = NscryptParameters()
        else:
            self.params = OptomecParameters()
        self.printParams.config(state=tk.NORMAL) #enables printer parameter button and menu

        #TODO - Prevent user from opening another window/interacting with main menu until conversion settings are closed

    def printParamsButtonCallback(self):
        self.writeStatus("Printer Parameters Click")
        print("Printer Parameters Click")
        if globals.printerTypeSelected == 0:
            paramWindow = tk.Toplevel()
            self.eval("tk::PlaceWindow {} center".format(str(paramWindow)))

            paramWindow.title("nScrypt Parameters")
            paramWindow.geometry("500x250")
            paramWindow.resizable(False, False)

            paramFrame = NscryptParameterGui(paramWindow, self)
            paramFrame.grid()

            paramWindow.wait_window()
        else:
            paramWindow = tk.Toplevel()
            self.eval("tk::PlaceWindow {} center".format(str(paramWindow)))

            paramWindow.title("Optomec Parameters")
            paramWindow.geometry("500x250")
            paramWindow.resizable(False, False)

            paramFrame = NscryptParameterGui(paramWindow, self)
            paramFrame.grid()

            paramWindow.wait_window()
        #after wait window close need to save new params to file, or need to modify old saved params

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

        self.printerTypeSelectFrame.pack(padx=50, pady=50)

        if parent.master.saved_line == -1:
            self.savedSettingsStatusLabel = tk.Label(self.printerTypeSelectFrame, text="No previously saved settings, safe to choose")
        else:
            self.savedSettingsStatusLabel = tk.Label(self.printerTypeSelectFrame, text="There are pre-existing saved settings for the imported file, selecting printer type will override")
        self.savedSettingsStatusLabel.pack(side="left")
        self.saveButton = tk.Button(self, text="Save", command=self.saveButtonCallback)

        self.saveButton.pack(padx=10, pady=10)

    def saveButtonCallback(self):
        globals.printerTypeSelected = self.printerTypeCombobox.current() #Set global value
        selectedPrinter = globals.PRINTER_TYPES[globals.printerTypeSelected] #Get corresponding string 

        globals.writeStatusQueue("Save Button Click " + selectedPrinter) #TODO - Replace with message queue system
        #TODO - Close window after saving? - Change to "Save and Exit"
        print("Save Button Click", selectedPrinter)

def queueLoop(rootObject):
    # Loop through all available messages until queue is empty
    while(True):
        try:
            message = globals.statusQueue.get(block=False)
            rootObject.writeStatus(message)
        except globals.queue.Empty:
            break

    # Follow the underlying loop of the GUI
    rootObject.after(QUEUE_LOOP_RATE, queueLoop, rootObject)