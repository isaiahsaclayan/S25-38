# S25-38, Transpiler
**Developers:** Isaiah Amir Saclayan, Alvin Chung, Andrew Viola, Theo Barrett-Johnson, John Otooni, Bozhidar Dimov

# User Manual

## Requisites
Ensure you have the neccessary requirements installed. Navigate to the project root and execute the following command.
``` bash
    pip install -r requirements.txt
```

## How to Use the Transpiler
1. Launch the program.
2. Click `Select Import File` to select a file to transpile.
3. Click `Conversion Settings` to select the desired printer.
4. Click `Printer Parameters` to set any desired parameters to be included in the output.
5. Click `Set Export Destination` to select the directory and name of the generated transpiled file.
6. Click `Start Conversion`.
7. Observe the status window for any errors and feedback during the conversion process.
8. If successful, view obtained transpiled file in the previously selected directory in step 5.    

## How to Run the Transpiler via Command Line

Navigate to the project root, then execute the following command.
``` bash
    python .\source\transpiler\
```

or

Navigate to sources directory.
``` bash
    python .\transpiler\
```

## How to Build the Executable (.exe)
1. Open a terminal.
2. Navigate to the project root.
3. Execute the batch file `generate-exe.bat`.
4. Wait for the process to complete. Ensure a successful build is indicated in the terminal.
5. Navigate to the `\build\output` directory.
6. Locate the `transpiler.exe` file.

---
# Developer Notes

# System Documentation
1. [GUI](docs)
2. [Printer Parameters](docs)
3. [Generic Toolpath Parser](docs)
4. [nScrypt Converter](docs/nscrypt.md)
5. [ACSPL Converter](docs/acspl/acspl.md)
6. [Toolpath Export](docs)
   
## Structure Notes
`/source/transpiler/__main__.py` is the main entry point of the program.  
`/source/transpiler` contains all the source code for our system.  
`/tests` contains all the test code for our system.

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
