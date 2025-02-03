# Imports
import logging
import os
import datetime as dt

# Instantiate Logger
logger = logging.getLogger("main")
LOG_FORMAT = "[%(asctime)s] - [%(levelname)s] %(message)s" # Ex. [2025-03-04 01:23:45] - [INFO] Message ...

def configureAndStartLogger():
    # Check if log folder is created, if not create it
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configure Logger
    logging.basicConfig(format=LOG_FORMAT,
                        encoding='utf-8',
                        level=logging.INFO)

    now = dt.datetime.now() # Fetch current time
    time = now.strftime("%Y-%m-%d_%H-%M-%S") # Format time

    # Create handler to log in logs folder and format name of log file
    # Ex. it is 1:23:45 on 2025-03-04, the log file name will be "transpiler-2025-03-04_01-23-45.log"
    logHandler = logging.FileHandler(f"logs/transpiler-{time}.log", encoding='utf-8')
    logHandler.setFormatter(logging.Formatter(LOG_FORMAT))
    logHandler.setLevel(logging.INFO)
    logger.addHandler(logHandler)

    # Print Header for Log File
    logger.info("===============TRANSPILER=====================")
    logger.info(f"File Name: transpiler-{time}.log")
    logger.info(f"Start Time: {now.strftime("%c")}")
    logger.info("==============================================")

# Main Entry Point
def main():
    # Start Logger
    configureAndStartLogger()


if __name__ == "__main__":
    main()