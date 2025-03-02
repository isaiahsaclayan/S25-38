# S25-38

# User Manual

## Requisites
Ensure you have the neccessary requirements installed. Navigate to the project root and execute the following command.
``` bash
    pip install -r requirements.txt
```

## How to Use the Transpiler
1. Launch the program.
2. Click `Import File` to select a file to transpile.
3. Click `Set Export Destination` to select the directory and name of the generated transpiled file.
4. Click `Conversion Settings` to select the desired printer.
5. Click `Printer Parameters` to set any desired parameters to be included in the output.
6. Click `Start Conversion`.
7. Observe the status window for any errors and feedback during the conversion process.
8. If successful, view obtained transpiled file in the previously selected directory in step 3.    

---
# Developer Notes
`/source/transpiler/__main__.py` is the main entry point of the program.
`/source/transpiler` contains all the source code for our system.  
`/tests` contains all the test code for our system.

## System Breakdown

### GUI
TODO

### Parameters
TODO

### Parser
TODO

### ACSPL Converter
TODO

### nScrypt Converter
TODO

### Toolpath Export
TODO

## Install Requirements
Navigate to project root, then execute the following command.
``` bash
    pip install -r requirements.txt
```

## To Run Tests
Navigate to tests/ReadME.md to reference testing instructions. 

## To Implement Logger Into Your Subsystem
1. Import logging to your python file.
``` python
import logging
```
2. Get logger instance. 
``` python
logger = logging.getLogger("main")
```
3. Log whatever you need.
``` python
logger.info("Message") # Info level message
logger.debug("Debug Message") # Debug level message
```

### Example
``` python
import logging

logger = logging.getLogger("main")

def exampleFunction():
    logger.info("Some Message")
    logger.debug("Some Debug Message")
```
