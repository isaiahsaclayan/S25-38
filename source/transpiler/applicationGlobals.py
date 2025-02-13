import enum

PRINTER_TYPES = ("nScrypt", "Optomec")
printerTypeSelected = 0

class PrinterType(enum.IntEnum):
    NSCRYPT = 0
    OPTOMEC = 1