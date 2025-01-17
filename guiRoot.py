'''
Author: Alvin Chung
Creation Date: 01/17/24
File: guiRoot.py
Description: The root tkinter object for the GUI application
'''

import tkinter as tk

class GuiRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.resizable(False, False)
        
        #Title of the window
        self.title("S25-38") #TODO - Provide suitable window title

        self.testLabel = tk.Label(text="TEST")

        self.testLabel.pack()