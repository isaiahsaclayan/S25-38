import enum
import queue

PRINTER_TYPES = ("nScrypt", "Optomec")
printerTypeSelected = 0

class PrinterType(enum.IntEnum):
    NSCRYPT = 0
    OPTOMEC = 1

# The queue that is used by the GUI to get messages from external modules
statusQueue = queue.Queue()
importFilePath = None
exportFilePath = None

def writeStatusQueue(message):
    statusQueue.put(message)


def setImportFilepath(filePath):
    importFilePath = filePath

def getImportFilepath():
    return importFilePath


def setExportFilepath(filePath):
    exportFilePath = filePath

def getExportFilepath():
    return exportFilePath