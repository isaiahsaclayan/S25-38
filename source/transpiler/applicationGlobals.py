import enum
import queue
import logging
PRINTER_TYPES = ("nScrypt", "Optomec")
printerTypeSelected = 0

class PrinterType(enum.IntEnum):
    NSCRYPT = 0
    OPTOMEC = 1

# The queue that is used by the GUI to get messages from external modules
statusQueue = queue.Queue()

def writeStatusQueue(message):
    statusQueue.put(message)

# The logger that is used by the application
logger = logging.getLogger("main")

def notify_and_log(message):
    writeStatusQueue(message)
    logging.info(message)