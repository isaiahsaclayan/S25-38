# guiRoot.py
Contains the definition of a GuiRoot() object which defines a root TKinter object along with other TKinter frame objects that encapsulate sub menus

## GuiRoot() 
The core of the GUI. This is used to create the root of a TKinter GUI.

### __init__(self, parent)
### writeStatus(self, text)
### clearStatus(self)
### setImportFilepathDisplay(self, filepath)
### setExportFilepathDisplay(self, filepath)
### exitProgramButtonCallback(self)
### importButtonCallback(self)
### setExportDestinationButtonCallback(self)
### conversionSettingsButtonCallback(self)
### startConversionButtonCallback(self)

## ConversionSettingsFrame(tk.Frame)
### __init__(parent)
### saveButtonCallback(self)
### cancelButtonCallback(self)

## ToolpathPreviewFrame(tk.Frame)
### continueButtonCallback(self)
### cancelButtonCallback(self)

## queueLoop(rootObject)
## conversionProcess(file_path, parameters, printer_type)