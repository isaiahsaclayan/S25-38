'''
Main entry point for the program
'''

from guiRoot import GuiRoot

root = GuiRoot()
root.eval("tk::PlaceWindow . center")
root.mainloop()
