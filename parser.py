import os
import logging

FILE = 'op010.ncl.1'
TITLE_COMMENT = "$$*"
INFO_COMMENT = "$$->"
SPINDLE_SPEED = "SPINDL"
COOLANT = "COOLNT"
MOVE = "GOTO"
MOVEMENT_SPEED = "FEDRAT"
UNIT_INFO = "UNITS"
ORIENTATION = "CSYS"
TOOL_NUMBER = "LOADTL"
FEATURE_NUMBER = "FEATNO"
MANUFACTURER_NUMBER = "MFGNO"
PART_NUMBER = "PARTNO"
MACHINE_TYPE = "MACHIN"
INCHES_PER_MIN = "IPM"
FINISH_FILE = "FINI"
END_MOVEMENT = "END"
TOOL_SIZE = "CUTTER"
GEOMETRY_TYPE = "CUTCOM_GEOMETRY_TYPE"
MAX_SPEED = "RAPID"

logger = logging.getLogger("main")


class genericParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.creoCommands = self.parse_file(self.file_path)
        self.coordinateSystem = ""
        self.coordinateSearch = False
        self.parsedCommands = []
        self.unparsedCommands = []


    def verify_file(self):
        file_name, file_extension = os.path.splitext(self.file_path)
        if file_extension.lower() != '.1':
            logger.error("File type not supported")
    
    def parse_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read().split('\n')
        
    def conversion(self):

        self.verify_file()

        for command in self.creoCommands:
            if len(command) == 0:
                    break
            if command[0] != ' ' and self.coordinateSearch:
                self.coordinateSearch = False
                self.parsedCommands.append({"coordinate_system":{"coordinate_system":self.coordinateSystem}})
            command = command.split()
            if not self.coordinateSearch:
                if command[0] == TITLE_COMMENT:
                    output = {"title": {"type":command[1], "version":" ".join(command[3:])}}
                    self.parsedCommands.append(output)
                elif command[0] == INFO_COMMENT:
                    self._infoCommentCommand(command)
                elif command[0] == SPINDLE_SPEED:
                    self.parsedCommands.append(self._spindleSpeed(command))
                elif command[0] == COOLANT:
                    self.parsedCommands.append(self._coolantCommand(command))
                elif command[0] == MOVE:
                    self.parsedCommands.append(self._movementCommand(command))
                elif command[0] == MOVEMENT_SPEED:
                    self.parsedCommands.append(self._speedCommand(command))
                elif command[0] == UNIT_INFO:
                    self.parsedCommands.append({"units":{"units":command[2]}})
                elif command[0] == TOOL_NUMBER:
                    self.parsedCommands.append({"tool":{"tool":command[2]}})
                elif command[0] == MACHINE_TYPE:
                    self.parsedCommands.append({"machine_info":{"machine_type":command[2][:-1], "machine_number":command[3]}})
                elif command[0] == PART_NUMBER:
                    self.parsedCommands.append({"part_number":{"part_number":command[2]}})
                elif command[0] == FINISH_FILE:
                    self.parsedCommands.append({"finish_file":{"bool":True}})
                elif command[0] == MAX_SPEED:
                    self.parsedCommands.append({"max_speed":{"bool":True}})
                else:
                    self.unparsedCommands.append(command)
            else:
                self._checkOrientationLine(command)
            
    def _movementCommand(self, command):
        command = command[2:]
        if len(command) == 3:
            return {"move": {self.coordinateSystem[0]:float(command[0][:-1]), self.coordinateSystem[1]:float(command[1][:-1]), self.coordinateSystem[2]:float(command[2])}}
        elif len(command) == 4:
            return {"move": {self.coordinateSystem[0]:float(command[0][:-1]), self.coordinateSystem[1]:float(command[1][:-1]), self.coordinateSystem[2]:float(command[2][:-1]), self.coordinateSystem[3]:float(command[3])}}
        elif len(command) == 5:
            return {"move": {self.coordinateSystem[0]:float(command[0][:-1]), self.coordinateSystem[1]:float(command[1][:-1]), self.coordinateSystem[2]:float(command[2][:-1]), self.coordinateSystem[3]:float(command[3][:-1]), self.coordinateSystem[4]:float(command[4])}}
        else:
            return "ERROR"
    
    def _spindleSpeed(self, command):
        command = command[2:]
        if len(command) == 1:
            return {"spindle_speed":{"control":command[0]}}
        elif len(command) == 2:
            return {"spindle_speed":{"control":command[0], "speed":float(command[1])}}
        elif len(command) == 3:
            return {"spindle_speed":{"control":command[0], "speed":float(command[1][:-1]), "direction":command[2]}}
        
    def _coolantCommand(self, command):
        if command[2] == "ON":
            return {"coolant":{"bool":True}}
        elif command[2] == "OFF":
            return {"coolant":{"bool":False}}
        
    def _speedCommand(self, command):
        command = command[2:]
        if command[1] == INCHES_PER_MIN:
            return {"speed": {"speed":float(command[0][:-1])}}
        else:
            # TODO: Convert to INCHES_PER_MIN based on the conversion, something we'll need to implement
            return {"speed": {"speed":float(command[0][:-1])}}
    
    def _infoCommentCommand(self, command):
        command = command[1:]
        if command[0] == ORIENTATION:
            self.coordinateSearch = True
            self.coordinateSystem = ""
            command = command[2:]
            self._checkOrientationLine(command)
        elif command[0] == FEATURE_NUMBER:
            self.parsedCommands.append({"feature_number":{"feature_number":command[2]}})
        elif command[0] == MANUFACTURER_NUMBER:
            self.parsedCommands.append({"manufacturer_number":{"manufacturer_number":command[2]}})
        elif command[0] == TOOL_SIZE:
            self.parsedCommands.append({"tool_size":{"tool_size":command[2]}})
        elif command[0] == END_MOVEMENT:
            self.parsedCommands.append({"end_movement":{"bool":True}})
        elif command [0] == GEOMETRY_TYPE:
            self.parsedCommands.append({"geometry_type":{"geometry_type":command[2]}})
        else:
            self.unparsedCommands.append(command)
            
    def _checkOrientationLine(self, command):
        for i in range(len(command)):
            if command[i][0] == '1':
                if i == 0:
                    self.coordinateSystem += "x"
                elif i == 1:
                    self.coordinateSystem += "y"
                elif i == 2:
                    self.coordinateSystem += "z"
                elif i == 3:
                    self.coordinateSystem += "a"
                elif i == 4:
                    self.coordinateSystem += "b"
    
    def __str__(self):
        output = ""
        for command in self.parsedCommands:
            output += str(command) + "\n"
        return output
    
    def save(self,fileName):
        with open(fileName, 'w') as file:
            for command in self.parsedCommands:
                file.write(str(command) + "\n")


commands = genericParser(FILE)
commands.conversion()
commands.save("output.txt")