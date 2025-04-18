"""
Author: Isaiah Amir Saclayan
Created: 02/01/2025
File: acsplConverter.py
Description: Performs generic toolpath to ACSPL conversion.
"""

from toolpathConverter import ToolpathConverter
from applicationGlobals import notify_and_log
from typing import List
import datetime as dt

"""
ACSPL Code Blocks
"""

START_COMMENT = "! Start of Toolpath"

HEADER_COMMENT = """#0
!Machine Type - Optomec 5-axis Aerosol Jet
"""

HEADER_CONFIG="""
VEL(10) = VEL(0); VEL(11) = VEL(1); VEL(12) = VEL(2); VEL(14) = VEL(4); VEL(15) = VEL(5)
ACC(10) = ACC(0); ACC(11) = ACC(1); ACC(12) = ACC(2); ACC(14) = ACC(4); ACC(15) = ACC(5)
DEC(10) = DEC(0); DEC(11) = DEC(1); DEC(12) = DEC(2); DEC(14) = DEC(4); DEC(15) = DEC(5)
KDEC(10) = KDEC(0); KDEC(11) = KDEC(1); KDEC(12) = KDEC(2); KDEC(14) = KDEC(4); KDEC(15) = KDEC(5)
JERK(10) = JERK(0); JERK(11) = JERK(1); JERK(12) = JERK(2); JERK(14) = JERK(4); JERK(15) = JERK(5)
XVEL(10) = XVEL(0); XVEL(11) = XVEL(1); XVEL(12) = XVEL(2); XVEL(14) = XVEL(4); XVEL(15) = XVEL(5)
XACC(10) = XACC(0); XACC(11) = XACC(1); XACC(12) = XACC(2); XACC(14) = XACC(4); XACC(15) = XACC(5)

MFLAGS(10).#DUMMY=1; MFLAGS(11).#DUMMY=1; MFLAGS(12).#DUMMY=1; MFLAGS(14).#DUMMY=1; MFLAGS(15).#DUMMY=1;
PTP/EV (10,11,12,14,15), APOS(X),APOS(Y),APOS(Z),APOS(A),APOS(B),200

GLOBAL REAL ALPHA
ALPHA = 0.9
MASTER MPOS(X) = APOS(10)*(1-ALPHA) + MPOS(X)*ALPHA
MASTER MPOS(Y) = APOS(11)*(1-ALPHA) + MPOS(Y)*ALPHA
MASTER MPOS(Z) = APOS(12)*(1-ALPHA) + MPOS(Z)*ALPHA
MASTER MPOS(A) = APOS(14)*(1-ALPHA) + MPOS(A)*ALPHA
MASTER MPOS(B) = APOS(15)*(1-ALPHA) + MPOS(B)*ALPHA
SLAVE/p X; SLAVE/p Y; SLAVE/p Z; SLAVE/p A; SLAVE/p B

CRangle=2*3.1416
"""

STOP = """
HALT ALL

STOP"""

CLOSE_INKJET = """ENDS (10,11,12,14,15)
TILL (^AST(10).#MOVE) & (^AST(11).#MOVE) & (^AST(12).#MOVE) &(^AST(14).#MOVE) & (^AST(15).#MOVE)
Start gIntSubBuffer,ShutterClose;TILL PST(gIntSubBuffer).#RUN = 0
WAIT CloseDelay
"""

OPEN_INKJET = """
Start gIntSubBuffer,ShutterOpen;TILL PST(gIntSubBuffer).#RUN = 0
WAIT OpenDelay"""

# List of supported commands
SUPPORTED_COMMANDS: List[str] = [
    "max_speed",
    "speed",
    "move",
    "feature_number",
    "manufacturer_number",
    "part_number",
    "end_movement",
    "finish_file"
    #"arc"
]

# List of ignored commands
IGNORED_COMMANDS: List[str] = [
    "tool",
    "tool_size",
    "coordinate_system",
    "spindle_speed",
    "coolant",
    "title",
    "machine_info",
    "geometry_type",
    "units"
]

class Machine:

    def __init__(self):
        # Flag if the machine is dispensing
        self._is_dispensing: bool = False

        # Flag if printing has occurred
        self._print_started: bool = False

        # Flag if within printing segment
        self._in_printing_segment: bool = False

        # Flag if done with processing toolpath
        self._done: bool = False

        # Units
        self._units = "mm"

        # Axis Registers
        self._X: any = None
        self._Y: any = None
        self._Z: any = None
        self._A: any = None
        self._B: any = None

    """
    Getters and Setters for is_dispensing, in_printing_segment, and axis registers
    """
    @property
    def is_dispensing(self):
        """
        Getter for _is_dispensing
        :return: value of _is_dispensing
        """
        return self._is_dispensing

    @is_dispensing.setter
    def is_dispensing(self, is_dispensing: bool):
        """
        Setter for _is_dispensing
        :param is_dispensing: value to be set
        :return: none
        """
        # Set print started once dispensing starts
        if not self._print_started and is_dispensing:
            self._print_started = True

        # Set the dispensing state
        self._is_dispensing = is_dispensing

    @property
    def in_printing_segment(self):
        """
        Getter for _in_printing_segment
        :return: value of _in_printing_segment
        """
        return self._in_printing_segment

    @in_printing_segment.setter
    def in_printing_segment(self, in_printing_segment: bool):
        """
        Setter for _in_printing_segment
        :param in_printing_segment: value to be set
        :return: none
        """
        self._in_printing_segment = in_printing_segment

    @property
    def print_started(self):
        """
        Getter for _print_started
        :return: value of _print_started
        """
        return self._print_started

    @property
    def done(self):
        """
        Getter for _done
        :return: value of _done
        """
        return self._done

    @done.setter
    def done(self, done: bool):
        """
        Setter for _done
        :param done: value to be set
        :return: none
        """
        self._done = done

    @property
    def units(self):
        """
        Getter for units
        :return: units
        """
        return self._units

    @units.setter
    def units(self, units: str):
        """
        Setter for units
        :param units: units to be set
        :return: none
        """
        self._units = units

    def set_axis_registers(self, x: any, y: any, z: any, a: any, b: any) -> None:
        """
        Set the axis registers for the machine
        :param x: desired location for x-axis
        :param y: desired location for y-axis
        :param z: desired location for z-axis
        :param a: desired location for a-axis
        :param b: desired location for b-axis
        :return: none
        """
        # If the units are inches, convert to mm with nanometer accuracy
        if self._units == "inches":
            self._X = round(float(x) * 25.4, 9)
            self._Y = round(float(y) * 25.4, 9)
            self._Z = round(float(z) * 25.4, 9)
            self._A = round(float(a) * 25.4, 9)
            self._B = round(float(b) * 25.4, 9)

        # If the units are mm, set the axis registers to the desired location with nanometer accuracy
        elif self._units == "mm":
            self._X = round(float(x), 9)
            self._Y = round(float(y), 9)
            self._Z = round(float(z), 9)
            self._A = round(float(a), 9)
            self._B = round(float(b), 9)


    def get_axis_registers(self) -> tuple[float, float, float, float, float]:
        """
        Get the axis registers for the machine
        :return: tuple of axis registers
        """
        return self._X, self._Y, self._Z, self._A, self._B

    def get_location_and_switchval_str(self, switch: str = "") -> str:
        """
        Formats the location and switch value for ACSPL command
        :param switch: switch type ex. "A", "V"
        :return: formatted string of location and switch value for command
        """
        # If switch is not provided
        if switch == "":
            # Format location string with no switch value
            return f"(10,11,12,14,15), {self._X}, {self._Y}, {self._Z}, {self._A}, {self._B}"
        # If switch is not provided
        else:
            # Format location string with switch value
            return f"(10,11,12,14,15), {self._X}, {self._Y}, {self._Z}, {self._A}, {self._B}, {self._get_switch_value(switch)}"

    def _get_switch_value(self, switch: str) -> str:
        """
        Get the corresponding switch value depending on switch type and state of machine
        :return: string representation of switch value
        """
        # If the machine is not dispensing and velocity switch, return the rapid speed string
        if not self._is_dispensing and "V" in switch.upper():
            return "gDblRapidSpeed"
        # If the machine is dispensing return the process speed string
        elif self._is_dispensing and "V" in switch.upper():
            return "gDblProcessSpeed"
        # If the machine is to dispense and not in printing segment and angle switch
        # return the printing segment speed string
        elif self._is_dispensing and not self.in_printing_segment and "A" in switch.upper():
            return "CRangle"

# Derived Class for ACSPL Conversion
class AcsplConverter(ToolpathConverter):

    def __init__(self,params=None):
        # Initialize Supported Commands List
        super().__init__(SUPPORTED_COMMANDS,params)

        # Create an Instance of Machine
        self.machine = Machine()

        # Parse the open and close delay
        if params:
            self._open_delay = int(self._parameters.params[0] if (self._parameters.params[0] != -1.0) else 0)
            self._close_delay = int(self._parameters.params[1] if (self._parameters.params[1] != -1.0) else 0)
        else:
            self._open_delay = 0
            self._close_delay = 0

        # Log ACSPL Converter Instantiation
        notify_and_log("ACSPL Converter Instantiated")

        # Log Open and Close Parameters
        notify_and_log(f"Received Open Delay: {self._open_delay} \t Received Close Delay: {self._close_delay}")

    def _get_header(self) -> str:
        """
        Returns the ACSPL header
        :return: string representation of the ACSPL header
        """
        # Get current date
        date = dt.datetime.now().strftime("%d-%m-%Y")
        # Get current time
        time = dt.datetime.now().strftime("%H:%M")

        # Format ACSPL Header
        return (HEADER_COMMENT +
                f"!Date=DD-MM-YY - {date} Time=HH:MM - {time}\n" +
                f"OpenDelay = {self._open_delay}\n" +
                f"CloseDelay = {self._close_delay}\n" +
                HEADER_CONFIG)

    def _format_and_append_command(self, command: str, switch: str = "") -> None:
        """
        Formats the command and appends to the translated commands list
        :param command: ACSPL command
        :param switch: switch to be added to the command
        :return: None
        """
        # If no switch was provided
        if switch == "":
            # Format the command with no switch
            acspl_instr = f"{command} {self.machine.get_location_and_switchval_str()}"
        # If a switch was provided
        else:
            # Format the command with switch and switch value
            acspl_instr = f"{command}/{switch} {self.machine.get_location_and_switchval_str(switch)}"
        # Append the command to the translated commands list
        self._translated_commands.append(acspl_instr)

    def _validate_translate_arg(self, args: any) -> bool:
        """
        Validates the arguments provided to translate function
        :param args: arguments provided to translate function
        :return: None
        """
        # Type check, must be type List[Dict[str,Dict[str,str]]
        type_err = "Invalid argument type provided to translate function - must be type List[Dict[str,Dict[str,str]]"
        if not isinstance(args, list):
            notify_and_log(type_err)
            return False
        for item in args:
            if not isinstance(item, dict):
                notify_and_log(type_err)
                return False
            for key, value in item.items():
                if not isinstance(key, str) or not isinstance(value, dict):
                    notify_and_log(type_err)
                    return False

        # Check if list is empty
        if len(args) == 0:
            notify_and_log("No commands provided to ACSPL translate function")
            return False

        # If all checks pass
        return True

    def _set_units(self, commands) -> None:
        """
        Set the units for the machine
        :param commands: list of commands to be processed
        :return: None
        """

        # Iterate through the commands
        for command in commands:
            # If the command is a units command
            if "units" in command:
                # If the units are inches
                if command["units"]["units"] == "INCHES":
                    # Set the units for the machine
                    self.machine.units = "inches"
                    # Notify user of the units
                    notify_and_log(f"Units found in input file = '{command["units"]["units"]}', will convert to mm.")
                    return
                # If the units are mm
                elif command["units"]["units"] == "MILLIMETERS":
                    # Set the units for the machine
                    self.machine.units = "mm"
                    # Notify user of the units
                    notify_and_log(f"Units found in input file = '{command["units"]["units"]}', will convert to mm.")
                    return

        # If no units command is found, set the default units to mm
        self.machine.units = "mm"
        notify_and_log("Units not provided, defaulting to mm")

    def _process_command(self, command: str, params: dict[str, str]) -> None:
        """
        Processes a single command
        :param command: individual command to be processed
        """
        # If the command is a max speed command
        if command == "max_speed":
            # Check if machine is currently dispensing or in a printing segment
            if self.machine.is_dispensing or self.machine.in_printing_segment:
                # If so, close the inkjet, and end the printing segment and dispensing
                self.machine.is_dispensing = False
                self.machine.in_printing_segment = False
                self._translated_commands.append(CLOSE_INKJET)
                return

        # If the command is a speed command
        elif command == "speed":
            # If normal speed command, machine is going to start dispensing
            self.machine.is_dispensing = True
            # Open the inkjet
            self._translated_commands.append(OPEN_INKJET)
            return

        # If the command is a move command
        elif command == "move":

            # Classify the type of move command
            # If not dispensing, the ACSPL movement is "PTP"
            if not self.machine.is_dispensing:
                # Set the location registers for the machine to store desired location
                self.machine.set_axis_registers(params["x"],
                                                params["y"],
                                                params["z"],
                                                params.get("a", 0.0),
                                                params.get("b", 0.0))
                # Format and append the PTP command
                self._format_and_append_command("PTP", "EV")
                return

            # If to dispense, and not in printing segment, ACSPL command is going to be XSEG...LINE
            elif self.machine.is_dispensing and not self.machine.in_printing_segment:
                # Format and append the XSEG command to dictate the start of the printing segment
                self._format_and_append_command("XSEG", "A")
                # Set the machine to be in printing segment
                self.machine.in_printing_segment = True
                # Set the location registers for the machine to store desired location
                self.machine.set_axis_registers(params["x"],
                                                params["y"],
                                                params["z"],
                                                params.get("a", 0.0),
                                                params.get("b", 0.0))
                # Format and append the LINE command
                self._format_and_append_command("LINE", "V")
                return

            # If dispensing, the ACSPL movement is "LINE"
            elif self.machine.in_printing_segment:
                # Set the location registers for the machine to store desired location
                self.machine.set_axis_registers(params["x"],
                                                params["y"],
                                                params["z"],
                                                params.get("a", 0.0),
                                                params.get("b", 0.0))
                # Format and append the LINE command
                self._format_and_append_command("LINE", "V")
                return

        # If the command is a feature number command
        elif command == "feature_number":
            # Parse the feature number
            feature_number = params["feature_number"]
            # Append the feature number
            self._translated_commands.append(f"! Feature Number: {feature_number}")

        # If the command is a manufacturer number command
        elif command == "manufacturer_number":
            # Parse the manufacturer number
            manufacturer_number = params["manufacturer_number"]
            # Append the manufacturer number
            self._translated_commands.append(f"! Manufacturer Number: {manufacturer_number}")

        # If the command is a part number command
        elif command == "part_number":
            # Parse the part number
            part_number = params["part_number"]
            # Append the part number
            self._translated_commands.append(f"! Part Number: {part_number}")

        # If the command is an arc command
        elif command == "arc":
            # Set the location registers for the machine to store desired location
            self.machine.set_axis_registers(params["x"],
                                            params["y"],
                                            params["z"],
                                            params.get("a", 0.0),
                                            params.get("b", 0.0))
            # Format and append the ARC command
            self._format_and_append_command("ARC")

        # If the command is an end movement command
        elif command == "end_movement":
            # If the end movement command is true
            if params["bool"] == "True":
                # If the machine is dispensing, close the inkjet
                if self.machine.is_dispensing:
                    # Append the close inkjet command
                    self._translated_commands.append(CLOSE_INKJET)
                    # Set the machine to not be dispensing
                    self.machine.is_dispensing = False

        # If the command is a finish file command
        elif command == "finish_file":
            # If the finish file command is true
            if params["bool"] == "True":
                # If the machine is dispensing, close the inkjet
                if self.machine.is_dispensing:
                    # Append the close inkjet command
                    self._translated_commands.append(CLOSE_INKJET)
                    # Set the machine to not be dispensing
                    self.machine.is_dispensing = False
                # Set the machine to be done
                self.machine.done = True
            # If false, return

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """

        # Notify user of start of transpiling
        notify_and_log("Transpiling to ACSPL...")

        # Set the units for the machine
        self._set_units(parsed_commands)

        # Check if the provided parsed commands is valid
        if not self._validate_translate_arg(parsed_commands):
            notify_and_log("Invalid argument provided to ACSPL translate function")
            return []

        # Append the machine setup code block
        self._translated_commands.append(self._get_header())

        # Add comment to dictate start of toolpath.
        self._translated_commands.append(START_COMMENT)

        # Iterate through each command
        for command in parsed_commands:

            # If done, break
            if self.machine.done:
                break

            # Parse the command
            parsed_command = list(command.keys())[0]

            # Do not process cases
            # If the command is to be ignored, skip
            if parsed_command in IGNORED_COMMANDS:
                continue
            # If the command is not supported command
            if parsed_command not in SUPPORTED_COMMANDS:
                self._translated_commands.append(f"!INVALID COMMAND: {command}")
                # Notify user of invalid command
                notify_and_log(f"{parsed_command} not supported")
                continue

            # Process the command
            self._process_command(parsed_command, command[parsed_command])

        # If the machine is dispensing, close the inkjet
        # Only invoked if parsed toolpath does not end properly by providing end movement or finish file command
        if self.machine.is_dispensing:
            self._translated_commands.append(CLOSE_INKJET)

        # Once commands are processed, append STOP ACSPL code block
        self._translated_commands.append(STOP)

        # Notify user of completion
        notify_and_log("Success! File is transpiled to ACSPL.")

        return self._translated_commands