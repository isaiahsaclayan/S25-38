import os

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
PART_NUMBER = "PARTNO"
MACHINE_TYPE = "MACHIN"
INCHES_PER_MIN = "IPM"

class genericParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.creoCommands = self.parse_file(self.file_path)
        self.coordinateSystem = ""
        self.coordinateSearch = False
        self.parsedCommands = []

    def parse_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read().split('\n')
        
    def conversion(self):
        for command in self.creoCommands:
            if len(command) == 0:
                    break
            if command[0] != ' ':
                self.coordinateSearch = False
            command = command.split()
            if not self.coordinateSearch:
                if command[0] == TITLE_COMMENT:
                    output = {"title": {"type":command[1], "version":" ".join(command[3:])}}
                    self.parsedCommands.append(output)
                elif command[0] == INFO_COMMENT:
                    self._infoCommentCommand(command)
                elif command[0] == SPINDLE_SPEED:
                    pass
                elif command[0] == COOLANT:
                    self.parsedCommands.append(self._coolantCommand(command))
                elif command[0] == MOVE:
                    self.parsedCommands.append(self._movementCommand(command))
                elif command[0] == MOVEMENT_SPEED:
                    self.parsedCommands.append(self._speedCommand(command))
                elif command[0] == UNIT_INFO:
                    pass
                elif command[0] == ORIENTATION:
                    pass
                elif command[0] == TOOL_NUMBER:
                    pass
            else:
                self._checkOrientationLine(command)
            
    def _movementCommand(self, command):
        command = command[2:]
        if len(command) == 3:
            return {"move": {self.coordinateSystem[0]:command[0], self.coordinateSystem[1]:command[1], self.coordinateSystem[2]:command[2]}}
        elif len(command) == 4:
            return {"move": {self.coordinateSystem[0]:command[0], self.coordinateSystem[1]:command[1], self.coordinateSystem[2]:command[2], self.coordinateSystem[3]:command[3]}}
        elif len(command) == 5:
            return {"move": {self.coordinateSystem[0]:command[0], self.coordinateSystem[1]:command[1], self.coordinateSystem[2]:command[2], self.coordinateSystem[3]:command[3], self.coordinateSystem[4]:command[4]}}
        else:
            return "ERROR"
        
    def _coolantCommand(self, command):
        if command[2] == "ON":
            return {"coolant":{"bool":True}}
        elif command[2] == "OFF":
            return {"coolant":{"bool":False}}
        
    def _speedCommand(self, command):
        command = command[2:]
        if command[1] == INCHES_PER_MIN:
            return {"speed": {"speed":command[0]}}
        else:
            # Convert to INCHES_PER_MIN based on the conversion, something we'll need to implement
            return {"speed": {"speed":command[0]}}
    
    def _infoCommentCommand(self, command):
        command = command[1:]
        if command[0] == ORIENTATION:
            self.coordinateSearch = True
            self.coordinateSystem = ""
            command = command[2:]
            self._checkOrientationLine(command)
            
    def _checkOrientationLine(self, command):
        for i in range(len(command)):
            if command[i][0] == '1':
                if i == 0:
                    self.coordinateSystem += "X"
                elif i == 1:
                    self.coordinateSystem += "Y"
                elif i == 2:
                    self.coordinateSystem += "Z"
                elif i == 3:
                    self.coordinateSystem += "A"
                elif i == 4:
                    self.coordinateSystem += "B"
    
    def __str__(self):
        output = '\n'.join(self.parsedCommands)
        return output


commands = genericParser(FILE)
commands.conversion()
print(commands.coordinateSystem)