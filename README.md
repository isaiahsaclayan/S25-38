# S25-38

# Developer Notes

`__main__.py` is the main entry point of the program.

`transpiler` is the python module that will house our code.

`python -m transpiler` to run main, must be in source directory.

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
