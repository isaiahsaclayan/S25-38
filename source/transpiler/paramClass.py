'''
Author: Theo Barrett-Johnson
Created: 02/03/25
File: paramClass.py
Description: The file for the design and implementation of the class that holds the data structures for parameter inputs
'''
import numpy as np
import tkinter as tk
from tkinter import filedialog
class Parameters:
    def __init__(self):
        #params will be a 2 by n array, The first row will be for nScrypt params,
        #second row will be for Optomec params, any param that is not set by user
        #to any specific value will be -1 by default
        #currently making n=16 as a base estimate for the number of relevant parameters for a given printer
        self.params = np.array([[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], dtype=float)


#TESTING
#below is example of calling on Parameters to initialize a Parameter array. This will need to be done upon toolpath import
#tmp = Parameters()
#tmp

WINDOW_TITLE = "S25-38 Parameters" #TODO - Provide suitable titles
MENU_TITLE = "S25-38 Machine Instruction Converter"
GUI_WINDOW_SIZE = "500x250"

class ParameterGui(tk.Tk):
    def __init__(self, gui):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False)
        self.gui = gui #allows for modification of the actual gui params from the overall system gui

        #Title of the window
        self.title(WINDOW_TITLE) 
        self.geometry(GUI_WINDOW_SIZE)

        #Title of Menu
        self.testLabel = tk.Label(self, text = MENU_TITLE)
        self.testLabel.grid(row=0, column=1)

        #parameter Controls
        self.p1label = tk.Label(self, text="Parameter 1: " + str(self.gui.params[0][0])) #shows current param val
        self.p1label.grid(row=1)
        self.param1 = tk.Entry(self,)
        self.param1.grid(row=1, column=1)

        self.p2label = tk.Label(self, text="Parameter 2: " + str(self.gui.params[0][1]))
        self.p2label.grid(row=2)
        self.param2 = tk.Entry(self)
        self.param2.grid(row=2, column=1)

        self.p3label = tk.Label(self, text="Parameter 3: " + str(self.gui.params[0][2]))
        self.p3label.grid(row=3)
        self.param3 = tk.Entry(self)
        self.param3.grid(row=3, column=1)

        self.currlabel = tk.Label(self, text= "Current Parameters:")
        self.currlabel.grid(row=4)
        self.paramlabel = tk.Label(self, text= str(self.gui.params))
        self.paramlabel.grid(row=4, column=1)
        #Ok button closes menu and saves params
        self.okButton =  tk.Button(self, text="OK", command=self.okButtonCallback)
        self.okButton.grid(row=5, column=1)
        #cancel button only closes menu with no save
        self.cancelButton =  tk.Button(self, text="Cancel", command=self.cancelButtonCallback)
        self.cancelButton.grid(row=5, column=2)

    def okButtonCallback(self): #updates params and closes window
        self.gui.params[0][0] = self.param1.get() #must manually type out a get for each parameter
        self.gui.params[0][1] = self.param2.get()
        self.gui.params[0][2] = self.param3.get()
        self.destroy()

    def cancelButtonCallback(self): #closes window and doesnt update params
        self.destroy()