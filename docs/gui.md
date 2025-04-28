## GUI General Sequence of Operations
The GUI is expected to be operated in a specific sequence for the first start of the program. The underlying processes depend on this order for proper function.

1. Setting Import File
2. Setting Conversion Settings 
3. Setting Printer Parameters
4. Setting Export Destination
5. Start Conversion Process.

So, all the buttons except the Select Import File button are disabled until the proper preceding action is completed. After an action is completed, the button for the next action will be made available.

After a full sequence is completed, the program has checks to account for actions that would be considered out of order.

# guiRoot.py
Contains the definition of a GuiRoot() object which defines a root TKinter object along with other TKinter frame objects that encapsulate sub menus
<br><br>
## GuiRoot(tk.Tk)
The core of the GUI. Represents the main menu. This is a root object of a TKinter GUI for this system.

### __init__(self, parent)
Called when the GuiRoot() object is constructed. Initializes all of the interfaces. This is where changes to the main GUI should be made.

### writeStatus(self, text)
Writes text to the status text box with a timestamp.

### clearStatus(self)
Clears the status text box completely.

### setImportFilepathDisplay(self, filepath)
Sets the displayed imported filepath on the main menu.

### setExportFilepathDisplay(self, filepath)
Sets the displayed export destination filepath on the main menu.

### exitProgramButtonCallback(self)
Exits the entire program by "destroying" the TKinter root object.

### importButtonCallback(self)
Connected to the Select Import File button. Opens a file dialog for the user to select which file to import and stores the filepath.

### setExportDestinationButtonCallback(self)
Connected to the Set Export Destination button. Opens a file dialog for the user to name and set the save location of a file after it is exported. 

### conversionSettingsButtonCallback(self)
Connected to the Conversion Settings button. Opens a Conversion Settings window.

### startConversionButtonCallback(self)
Connected to the Start Conversion button. Starts the conversion process.
If Preview Toolpath is set (checked), then a Toolpath Preview Window will open before a file is exported. 


<br><br>
## ConversionSettingsFrame(tk.Frame)
### __init__(parent)
Called when the ConversionSettingsFrame() object is constructed. Initializes all of the interfaces. This is where changes to the Conversion Settings window should be made. Contains a flag that can be access externally, designed to be used for checking if settings were actually saved or not.

### saveButtonCallback(self)
Saves the settings from the Conversion Settings menu and closes the window.

### cancelButtonCallback(self)
Closes the Conversion Settings menu without saving any settings.


<br><br>
## ToolpathPreviewFrame(tk.Frame)
### __init__(self, parent, toolpath)
Called when the ToolpathPreviewFrame() object is constructed. Initializes all of the interfaces. This is where changes to the Toolpath Preview Window should be made. Primary function is to display the converted toolpath before export. Contains a flag that can be access externally, designed to be used for checking if the export process should continue or not.

### continueButtonCallback(self)
The conversion process is allowed to continue. A file will be exported from the system.

### cancelButtonCallback(self)
The conversion process will be halted. A file will not be exported from the system.

<br><br>
## queueLoop(rootObject)
Pass in a root TKinter GUI object to have that GUI periodically check a queue for status messages. Checks a loop located in applicationGlobals.py.

<br><br>
## conversionProcess(file_path, parameters, printer_type)
Contains the operations for toolpath conversion.