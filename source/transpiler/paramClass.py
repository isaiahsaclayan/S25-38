'''
Author: Theo Barrett-Johnson
Created: 02/03/25
File: paramClass.py
Description: The file for the design and implementation of the class that holds the data structures for parameter inputs
'''
#import numpy as np #potentially no longer using/need np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class NscryptParameters:
    def __init__(self):
        #params will be a 1D n-length array,
        #any param that is not set by user to any specific value will be -1 by default
        #currently making n=16 as a base estimate for the number of relevant parameters for a given printer
        self.params = [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]

class OptomecParameters:
    def __init__(self):
        #params will be a 1D n-length array,
        #any param that is not set by user to any specific value will be -1 by default
        #currently making n=18 as a base estimate for the number of relevant parameters for a given printer
        self.params = [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]

MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x250"

class NscryptParameterGui(tk.Frame):
    def __init__(self, parent, gui):
        super().__init__(parent)
        self.container = tk.Frame(self)
        self.gui = gui #allows for modification of the actual gui params from the overall system gui

        #Title of Menu
        self.testLabel = tk.Label(self, text = MENU_TITLE)
        self.testLabel.grid(row=0, column=1)

        #parameter Controls
        self.p1label = tk.Label(self, text="Vector[0] or Spherical[1]: ")
        self.p1label.grid(row=1)
        #self.param1 = tk.Entry(self)
        #self.param1.insert(0,str(gui.params.params[0]))
        #self.param1.grid(row=1, column=1)
        self.cType = tk.Entry(self)
        self.cType.insert(0,str(gui.params.params[0]))
        self.cType.grid(row=1, column=1)

        self.p2label = tk.Label(self, text="Parameter 2: ")
        self.p2label.grid(row=2)
        self.param2 = tk.Entry(self)
        self.param2.insert(0,str(gui.params.params[1]))
        self.param2.grid(row=2, column=1)

        self.p3label = tk.Label(self, text="Parameter 3: ")
        self.p3label.grid(row=3)
        self.param3 = tk.Entry(self)
        self.param3.insert(0,str(gui.params.params[2]))
        self.param3.grid(row=3, column=1)

        self.currlabel = tk.Label(self, text= "Current Parameters:")
        self.currlabel.grid(row=4)
        self.paramlabel = tk.Label(self, text= str(gui.params.params))
        self.paramlabel.grid(row=4, column=1)
        #Ok button closes menu and saves params
        self.okButton =  tk.Button(self, text="OK", command=self.okButtonCallback)
        self.okButton.grid(row=5, column=1)
        #cancel button only closes menu with no save
        self.cancelButton =  tk.Button(self, text="Cancel", command=self.cancelButtonCallback)
        self.cancelButton.grid(row=5, column=2)

    def okButtonCallback(self): #updates params and closes window
        temp1 = self.cType.get() #must manually type out a get for each parameter
        temp2 = self.param2.get()
        temp3 = self.param3.get()

        if float(temp1) != 1 and float(temp1) != 0:
            #create an error message telling them to go below allowed limit
            self.gui.writeStatus("Type must be 0 or 1")
            print("Coordinate Type must be 0 or 1")
        elif float(temp2) >= 100:
            self.gui.writeStatus("Parameter out of bounds")
            print("Parameter 2 too high!")
        elif float(temp3) >= 100:
            self.gui.writeStatus("Parameter out of bounds")
            print("Parameter 3 too high!")
        else:
            self.gui.params.params[0] = float(temp1)
            self.gui.params.params[1] = float(temp2)
            self.gui.params.params[2] = float(temp3)
            self.master.destroy()

    def cancelButtonCallback(self): #closes window and doesnt update params
        self.master.destroy()

class OptomecParameterGui(tk.Frame):
    def __init__(self, parent, gui):
        super().__init__(parent)
        self.container = tk.Frame(self)
        self.gui = gui #allows for modification of the actual gui params from the overall system gui

        #Title of Menu
        self.testLabel = tk.Label(self, text = MENU_TITLE)
        self.testLabel.grid(row=0, column=1)

        #parameter Controls
        self.p1label = tk.Label(self, text="Parameter 1: ")
        self.p1label.grid(row=1)
        self.param1 = tk.Entry(self)
        self.param1.insert(0,str(gui.params.params[0]))
        self.param1.grid(row=1, column=1)

        self.p2label = tk.Label(self, text="Parameter 2: ")
        self.p2label.grid(row=2)
        self.param2 = tk.Entry(self)
        self.param2.insert(0,str(gui.params.params[1]))
        self.param2.grid(row=2, column=1)

        self.p3label = tk.Label(self, text="Parameter 3: ")
        self.p3label.grid(row=3)
        self.param3 = tk.Entry(self)
        self.param3.insert(0,str(gui.params.params[2]))
        self.param3.grid(row=3, column=1)

        self.currlabel = tk.Label(self, text= "Current Parameters:")
        self.currlabel.grid(row=4)
        self.paramlabel = tk.Label(self, text= str(gui.params.params))
        self.paramlabel.grid(row=4, column=1)
        #Ok button closes menu and saves params
        self.okButton =  tk.Button(self, text="OK", command=self.okButtonCallback)
        self.okButton.grid(row=5, column=1)
        #cancel button only closes menu with no save
        self.cancelButton =  tk.Button(self, text="Cancel", command=self.cancelButtonCallback)
        self.cancelButton.grid(row=5, column=2)

    def okButtonCallback(self): #updates params and closes window
        temp1 = self.param1.get() #must manually type out a get for each parameter
        temp2 = self.param2.get()
        temp3 = self.param3.get()

        if float(temp1) >= 100:
            #create an error message telling them to go below allowed limit
            self.gui.writeStatus("Parameter out of bounds")
            print("Parameter 1 too high!")
        elif float(temp2) >= 100:
            self.gui.writeStatus("Parameter out of bounds")
            print("Parameter 2 too high!")
        elif float(temp3) >= 100:
            self.gui.writeStatus("Parameter out of bounds")
            print("Parameter 3 too high!")
        else:
            self.gui.params.params[0] = float(temp1)
            self.gui.params.params[1] = float(temp2)
            self.gui.params.params[2] = float(temp3)
            self.master.destroy()

    def cancelButtonCallback(self): #closes window and doesnt update params
        self.master.destroy()