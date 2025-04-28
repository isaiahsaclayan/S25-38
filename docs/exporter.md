# toolpathExporter.py

This file contains the `ToolpathExporter` class, which handles the final export of formatted toolpath instructions to disk.

# ToolpathExporter Class

The `ToolpathExporter` class is responsible for safely writing a list of machine instructions to a file, exactly as received, without performing any additional formatting or transformation.

It ensures that the toolpath is valid, manages different file extensions depending on printer type (nScrypt or Optomec), and provides robust error handling during the save operation.

ToolpathExporter enables:

- Consistent and reliable export for different printer formats.
- Minimal assumptions about the toolpath structure: it simply writes each string to the file followed by a newline.
- Proper status updates during the export process.

# Key Methods

## `__init__(self, export_path: str, printer_type: str)`

Initializes the exporter with the target export path and the printer type (either "nScrypt" or "Optomec").

It selects the appropriate file extension based on the printer type.

---

## `validate_toolpath(self, toolpath: List[str]) -> bool`

Validates that the input `toolpath` is a non-empty list containing only string elements.

**Notes:**
- Empty lines (empty strings) are allowed to preserve formatting and readability.
- Non-string elements will trigger an error and prevent export.

---

## `export(self, toolpath: List[str]) -> str`

Writes the toolpath instructions exactly as they are received:
- Each string is written on a new line.
- Uses UTF-8 encoding.
- If any I/O error occurs, it catches the exception and returns an error message.

**Status messages are logged** for success or failure.

**Example behavior:**
If toolpath is:
```python
[
    "!Machine Type - Optomec 5-axis Aerosol Jet",
    "OpenDelay = 0",
    "CloseDelay = 0",
    "Start gIntSubBuffer,ShutterOpen;TILL PST(gIntSubBuffer).#RUN = 0",
    "WAIT OpenDelay",
    "XSEG/A (10,11,12,14,15), -0.35, 5.0107142857, 1.225, 0.0, 0.0, CRangle",
    "LINE/V (10,11,12,14,15), -0.35, 5.0107142857, 1.1, 0.0, 0.0, gDblProcessSpeed"
]
```
The output file would look exactly like:
```
!Machine Type - Optomec 5-axis Aerosol Jet
OpenDelay = 0
CloseDelay = 0
Start gIntSubBuffer,ShutterOpen;TILL PST(gIntSubBuffer).#RUN = 0
WAIT OpenDelay
XSEG/A (10,11,12,14,15), -0.35, 5.0107142857, 1.225, 0.0, 0.0, CRangle
LINE/V (10,11,12,14,15), -0.35, 5.0107142857, 1.1, 0.0, 0.0, gDblProcessSpeed
```

# Integration with GUI

In `guiRoot.py`, the `ToolpathExporter` class is used after the toolpath is converted:
- The GUI collects the user’s input and export destination.
- The parsed and converted toolpath is passed directly to the exporter.
- If preview is enabled, the toolpath is displayed before writing.
- Export status messages are displayed to the user through the GUI status panel.

The GUI does not modify the toolpath contents — the exporter writes exactly what it receives.

# Key Design Choices

- **No Reformatting**: Exporter trusts that incoming data is already prepared properly by the converters.
- **Minimal Assumptions**: Supports both nScrypt and Optomec formats without additional formatting logic.
- **Safe File Handling**: Uses Python's `with open(...)` context manager to safely handle files and avoid corruption.
- **Separation of Concerns**: Export logic is isolated from parsing and conversion, supporting modular testing and development.

# Summary

The `ToolpathExporter` is a critical final step in the system, ensuring the machine instructions generated from the converters are saved reliably and without corruption.  
Its simple, robust design allows for future expansions such as new printer types or additional file types with minimal changes.
