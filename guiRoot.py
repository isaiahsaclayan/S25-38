'''
Author: Alvin Chung
Creation Date: 01/17/24
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import tkinter as tk
import globalVariables as globals

class GuiRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False)
        
        #Title of the window
        self.title("S25-38") #TODO - Provide suitable title
        self.geometry(globals.GUI_WINDOW_SIZE)

        self.testLabel = tk.Label(self, text="S25-38 Machine Instruction Converter")
        self.testLabel.pack(anchor="center")

        #Import Button
        self.importFileButton = tk.Button(self, text="Import File")
        self.importFileButton.pack(anchor="w", padx=5, pady=5)

        #Set Export Destination Button
        self.exportFileButton = tk.Button(self, text="Set Export Destination")
        self.exportFileButton.pack(anchor="w", padx=5, pady=5)

        #Conversion Settings Button
        self.conversionSettings = tk.Button(self, text="Conversion Settings")
        self.conversionSettings.pack(anchor="w", padx=5, pady=5)

        #Start Conversion Process Button
        self.startConvButton = tk.Button(self, text="Start Conversion")
        self.startConvButton.pack(anchor="center", padx=5, pady=5)

        #Status Text Area
        self.statusTextArea = tk.Text(self, wrap=tk.WORD)
        self.statusTextArea.pack(side="bottom", padx=5, pady=5)