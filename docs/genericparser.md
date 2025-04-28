# parser.py
Parses Creo Parametric files and converts them into a structured list of dictionaries to be translated later

## __init__(self, file_path)
Initializes the parser with a given file path. Sets up internal states such as:
- `creoCommands`: raw lines from the Creo file.
- `coordinateSystem`: defaulted to "xyz".
- `coordinateSearch`: flag indicating if orientation block is being processed.
- `parsedCommands`: list of successfully parsed commands.
- `unparsedCommands`: list of commands that could not be parsed.

## verify_file(self)
Checks that the provided file has a supported extension (`.ncl.1` or `.ncl`). Logs an error if not.

## parse_file(self, file_path)
Reads the specified Creo file and returns its contents split by lines.

## conversion(self)
Main parsing routine. Iterates through each line of the file and parses the command to the appropriate handler based on command keywords. Appends structured command dictionaries to `parsedCommands`. Unrecognized commands are logged and stored in `unparsedCommands`.

## _movementCommand(self, command)
Parses GOTO movement commands and returns a dictionary with axis-labeled coordinate data. Supports up to 5 axes, labeled according to the current `coordinateSystem`

## _spindleSpeed(self, command)
Parses spindle speed commands. This function supports either
- Control command
- Control with speed
- Control with speed and direction

## _coolantCommand(self, command)
Parses coolant commands and converts them into Boolean
`"ON"` - `True`
`"OFF"` - `False`

## _speedCommand(self, command)
Parses the feed rate commands. This function assumes that feed rates are in inches per minute (IPM). There is a placeholder for unit conversion if there are other possible formats.

## _infoCommentCommand(self, command)
Handles comments and information blocks marked with `$$->`. It parses other data such as:
- Orientation systems
- Feature number
- Manufacturer number
- Tool size
- End movement
- Geometry type


## _checkOrientationLine(self, command)
Used with the coordinate system detection. Checks orientation lines and sets the correct axis labels based on binary markers.
Normal Orientation -  (`x`, `y`, `z`, `a`, `b`)


## __str__(self)
Returns the string representation of the parsed command list, each on its own line.

## save(self, fileName)
Writes the parsed command list to the specified file, each command dictionary on a new line.

## parse_commands(self)
Triggers the parsing process and returns the list of parsed command dictionaries.
