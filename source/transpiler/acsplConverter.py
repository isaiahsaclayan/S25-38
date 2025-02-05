from . import ToolpathConverter
from typing import List

# ACSPL Code Blocks, from gcodetoacspl repo provided
MACHINE_SETUP = """
#0
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

CRangle=2*3.1416
"""

STOP = """
HALT ALL
STOP
"""

CLOSE_INKJET = """
ENDS (10,11,12,14,15)
TILL (^AST(10).#MOVE) & (^AST(11).#MOVE) & (^AST(12).#MOVE) &(^AST(14).#MOVE) & (^AST(15).#MOVE)
Start gIntSubBuffer,ShutterClose;TILL PST(gIntSubBuffer).#RUN = 0
WAIT CloseDelay
"""

OPEN_INKJET = """
Start gIntSubBuffer,ShutterOpen;TILL PST(gIntSubBuffer).#RUN = 0
WAIT OpenDelay
"""

# Dictionary mapping generic commands to ACSPL commands
COMMAND_MAP: dict[str,str] = {
    "MACHINE_SETUP": MACHINE_SETUP,
    "STOP": STOP,
    "CLOSE_INKJET": CLOSE_INKJET,
    "OPEN_INKJET": OPEN_INKJET,
    "GOTO" : "PTP"
}

class AcsplConverter(ToolpathConverter):
    def __init__(self):
        super().__init__(COMMAND_MAP)

    def _get_command(self, command: dict[str, dict[str, str]]) -> str:
        """
        Performs translation of a single command
        :param command: individual command to be translated
        :return: string representation of the translated command
        """
        # TODO: perform translation of single command
        pass

    def translate(self, parsed_commands: List[dict[str, dict[str, str]]]) -> List[str]:
        """
        Translates generic toolpath to list of formatted commands
        :param parsed_commands: list of commands to be translated from generic parser
        :return: list of strings that are translated commands
        """
        # Stores the ACSPL Commands in a list of strings
        acspl = []

        # Iterate through each command
        for command in parsed_commands:

            # Check if the command is a valid command
            if command.keys not in COMMAND_MAP:
                acspl.append(f"INVALID COMMAND: {command}")
                continue

            # Get the ACSPL equivalent of the command
            acspl.append(self._get_command(command))

        return acspl