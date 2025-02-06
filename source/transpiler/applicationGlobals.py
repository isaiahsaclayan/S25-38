import enum
import queue

PRINTER_TYPES = ("nScrypt", "Optomec")
printerTypeSelected = 0

class PrinterType(enum.IntEnum):
    NSCRYPT = 0
    OPTOMEC = 1

statusQueue = queue.Queue()

def writeStatusQueue(message):
    statusQueue.put(message)