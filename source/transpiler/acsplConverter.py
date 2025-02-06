from venv import logger

from toolpathConverter import ToolpathConverter
from typing import List
import logging

# Get the logger instance
logger = logging.getLogger(__name__)

"""
ACSPL Code Blocks
"""
MACHINE_SETUP = """#0
!Machine Type - Optomec 5-axis Aerosol Jet
OpenDelay = 0
CloseDelay = 0

! DONOTMERGE: Understand the code and rewrite the preamble
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

CRangle=2*3.1416"""

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
    "move"
]

class Machine:

    def __init__(self):
        # If the machine is dispensing
        self._is_dispensing: bool = False

        # If printing has occurred
        self._print_started: bool = False

        # If within printing segment
        self._in_printing_segment: bool = False

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
        return self._is_dispensing

    @is_dispensing.setter
    def is_dispensing(self, is_dispensing: bool):
        # Set print started once dispensing starts
        if not self._print_started and is_dispensing:
            self._print_started = True

        # Set the dispensing state
        self._is_dispensing = is_dispensing

    @property
    def in_printing_segment(self):
        return self._in_printing_segment

    @in_printing_segment.setter
    def in_printing_segment(self, in_printing_segment: bool):
        self._in_printing_segment = in_printing_segment

    @property
    def print_started(self):
        return self._print_started

    def set_axis_registers(self, x: any, y: any, z: any, a: any = None, b: any = None):
        self._X = x
        self._Y = y
        self._Z = z
        self._A = a
        self._B = b

    def get_location_and_switchval_str(self, switch: str):
        # TODO: Extend to support 5 axis
        return f"(10,11,12), {self._X}, {self._Y}, {self._Z}, {self._get_switch_value(switch)}"

    def _get_switch_value(self, switch: str):
        """
        Get the corresponding switch value depending on switch type and state of machine
        :return: string representation of switch value
        """
        # If the machine is not dispensing and velocity switch, return the rapid speed string
        if not self._is_dispensing and "V" in switch.upper():
            return "gDblRapidSpeed"
        # If the machine is dispensing return the process speed string
        elif "V" in switch.upper() and self._is_dispensing:
            return "gDblProcessSpeed"
        # If the machine is to dispense and not in printing segment and angle switch
        # return the printing segment speed string
        elif self._is_dispensing and not self.in_printing_segment and "A" in switch.upper():
            return "CRangle"

class AcsplConverter(ToolpathConverter):
    def __init__(self):
        # Initialize Command Map
        super().__init__(SUPPORTED_COMMANDS)

        # Create an Instance of Machine
        self.machine = Machine()

        # Log ACSPL Converter Instantiation
        logger.info("ACSPL Converter Instantiated")

    def _format_and_append_command(self, command: str, switch: str):
        """
        Formats the command with the switch
        :param command: command to be formatted
        :param switch: switch to be added to the command
        :return: formatted command
        """
        acspl_instr = f"{command}/{switch} {self.machine.get_location_and_switchval_str(switch)}"
        self._translated_commands.append(acspl_instr)

    def _process_command(self, command: str, params: dict[str, str]):
        """
        Processes a single command
        :param command: individual command to be translated
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
            # TODO: Extend to support 5 axis

            # Classify the type of move command
            # If not dispensing, the ACSPL movement is "PTP"
            if not self.machine.is_dispensing:

                # Set the location registers for the machine to store desired location
                self.machine.set_axis_registers(params["x"], params["y"], params["z"])
                # Format and append the PTP command
                self._format_and_append_command("PTP", "EV")

            # If to dispense, and not in printing segment, ACSPL command is going to be XSEG...LINE
            elif self.machine.is_dispensing and not self.machine.in_printing_segment:

                # Format and append the XSEG command to dictate the start of the printing segment
                self._format_and_append_command("XSEG", "A")

                # Set the machine to be in printing segment
                self.machine.in_printing_segment = True

                # Set the location registers for the machine to store desired location
                self.machine.set_axis_registers(params["x"], params["y"], params["z"])
                # Format and append the LINE command
                self._format_and_append_command("LINE", "V")

            # If dispensing, the ACSPL movement is "LINE"
            elif self.machine.in_printing_segment:
                # Set the location registers for the machine to store desired location
                self.machine.set_axis_registers(params["x"], params["y"], params["z"])
                # Format and append the LINE command
                self._format_and_append_command("LINE", "V")

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """

        # Add comment to dictate start of toolpath.
        self._translated_commands.append("! Start of Toolpath")

        # Iterate through each command
        for command in parsed_commands:

            # Check if the command is a valid command
            parsed_command = list(command.keys())[0]
            if parsed_command not in SUPPORTED_COMMANDS:
                self._translated_commands.append(f"!INVALID COMMAND: {command}")
                logger.info(f"Invalid command: {command}")
                continue

            # Process the command
            self._process_command(parsed_command, command[parsed_command])

        # Once commands are processed, append STOP ACSPL code block
        self._translated_commands.append(STOP)

        return self._translated_commands