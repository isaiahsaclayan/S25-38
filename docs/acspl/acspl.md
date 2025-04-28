# acsplConverter.py
Inherits from the ToolpathConverter parent class and implements _process_command and translate to perform generic toolpath to ACSPL format conversion. Additionally defines a Machine class to manage machine state information for 5-axis control.

## Machine Class
Handles internal machine state including position registers, dispensing status, printing segments, units, and formatting of ACSPL movement commands.

### init(self)
Initializes a Machine object with default flags (dispensing, printing, etc.) set to False, default units as millimeters (mm), and initializes axis registers (X, Y, Z, A, B) to None.

### is_dispensing (property)
Getter method that returns the current dispensing state of the machine (True or False).

### is_dispensing (setter)
Setter method that updates the dispensing state. Also sets the print_started flag to True when dispensing begins.

### in_printing_segment (property)
Getter method that returns whether the machine is currently within a printing segment.

### in_printing_segment (setter)
Setter method that updates whether the machine is within a printing segment.

### print_started (property)
Getter method that returns whether printing has started at any point.

### done (property)
Getter method that returns whether the machine has finished processing the toolpath.

### done (setter)
Setter method that updates the done state (True or False).

### units (property)
Getter method that returns the current unit system being used (mm or inches).

### units (setter)
Setter method that updates the unit system (mm or inches).

### set_axis_registers(self, x, y, z, a, b)
Sets the axis register values (X, Y, Z, A, B) based on the provided coordinates.
Automatically converts inches to millimeters if necessary and rounds values to 4 decimal places.

### get_axis_registers(self) -> tuple
Returns a tuple containing the current values of (X, Y, Z, A, B).

### get_location_and_switchval_str(self, switch: str = "") -> str
Formats and returns a string representing the current axis register values for ACSPL commands.
Optionally includes a switch value (like "A" or "V") based on the machine state.

### _get_switch_value(self, switch: str) -> str
Returns the appropriate ACSPL switch value depending on the current machine state:

`gDblRapidSpeed` if moving rapidly without dispensing,

`gDblProcessSpeed` if moving while dispensing,

`CRangle` if beginning a printing segment.

## ACSPL Converter
Main derived class that translates parsed toolpath commands into formatted ACSPL output by managing the machine's internal state.

### init(self, params=None)
Initializes the AcsplConverter by calling the parent ToolpathConverter constructor.
Creates a Machine instance, parses open and close delays (if provided), and logs initialization information.

### _get_header(self) -> str
Generates the ACSPL file header, which includes:
- Machine information comment
- Date and time of generation
- Open and close delay settings
- Motion configuration block

### _format_and_append_command(self, command: str, switch: str = "")
Formats a command and appends it to the list of translated commands.
Includes the machine's current position registers and an optional switch value when formatting.

### _validate_translate_arg(self, args: any) -> bool
Validates the input to the translate function, ensuring it is a properly structured list of dictionaries.
Logs an error and returns False if the structure is invalid.

### _set_units(self, commands)
Iterates through the parsed commands to determine whether the units are set to "inches" or "millimeters".
Defaults to "millimeters" if no unit is specified.

### _process_command(self, command: str, params: dict[str, str])
Processes a single command and updates the translation list or the machine state accordingly:
- Handles speed changes (open/close inkjet)
- Movement commands (PTP, LINE, XSEG)
- Metadata comments (feature number, manufacturer number, part number)
- Ending commands (closing inkjet, marking processing as done)

### translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]
Main translation function that processes a full list of parsed commands:
- Validates the input
- Sets the units
- Adds the header
- Processes all commands
- Handles closing inkjet tool if necessary
- Appends the STOP block to end the program.
- Returns a full list of formatted ACSPL instructions.