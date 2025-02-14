import unittest
import sys
sys.path.append("../source/transpiler/")
from nscryptConverter import NscryptConverter, VERSION, TYPE

PARSED_COMMANDS = [
    {'title': {'type': 'Pro/CLfile', 'version': '11.0 - 11.0.0.0'}},
    {'manufacturer_number': {'manufacturer_number': 'MFG0006'}},
    {'part_number': {'part_number': 'MFG0006'}},
    {'feature_number': {'feature_number': '402'}},
    {'machine_info': {'machine_type': 'UNCX01', 'machine_number': '1'}},
    {'geometry_type': {'geometry_type': 'OUTPUT_ON_CENTER'}},
    {'units': {'units': 'INCHES'}},
    {'tool': {'tool': '1'}},
    {'tool_size': {'tool_size': '0.500000'}},
    {'coordinate_system': {'coordinate_system': 'xyz'}},
    {'spindle_speed': {'control': 'RPM,', 'speed': 1000.0, 'direction': 'CLW'}},
    {'coolant': {'bool': True}},
    {'max_speed': {'bool': True}},
    {'move': {'x': -0.35, 'y': 5.0107142857, 'z': 1.225}},
    {'speed': {'speed': 10.0}},
    {'move': {'x': -0.35, 'y': 5.0107142857, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 5.0107142857, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 5.0107142857, 'z': 1.2}},
    {'spindle_speed': {'control': 'OFF,'}}
   ]


def _print(results):
    for result in results:
        print(result)


class TestnScryptConverter(unittest.TestCase):
    def setUp(self):
        self.nScryptConverter = NscryptConverter()

    def test_nScrypt_constructor(self):
        self.assertIsNotNone(self.nScryptConverter)
        self.assertIsNotNone(self.nScryptConverter._units)

    def test_invalid_command(self):
        # Arrange
        INVALID_COMMAND = {
            "INVALID": {}
        }
        exp_result = [VERSION,
                      TYPE,
                      "!INVALID COMMAND: {'INVALID': {}}",
        ]
        # Act
        result = self.nScryptConverter.translate([INVALID_COMMAND])
        # Assert
        self.assertEqual(result, exp_result)

    def test_move_command(self):
        # Arrange
        MOVE_COMMAND = [
            {"move": {"x": "10.0", "y": "20.0", "z": "30.0"}}
        ]
        exp_result = [VERSION,
                      TYPE,
                      "10.0 20.0 30.0 0.0 0.0",
        ]
        # Act
        result = self.nScryptConverter.translate(MOVE_COMMAND)
        # Assert
        self.assertEqual(result, exp_result)

    def test_unit_command(self):
        # Arrange
        MOVE_COMMAND = [
            {"units": {"units": "INCHES"}}
        ]
        exp_result = [VERSION,
                      TYPE,
        ]
        exp_units = "INCHES"
        # Act
        result = self.nScryptConverter.translate(MOVE_COMMAND)
        units = self.nScryptConverter._units
        # Assert
        self.assertEqual(result, exp_result)
        self.assertEqual(units, exp_units)
        
    def test_unit_move_command(self):
        # Arrange
        MOVE_COMMAND = [
            {"units": {"units": "INCHES"}},
            {"move": {"x": "10.0", "y": "20.0", "z": "30.0"}}
        ]
        exp_result = [VERSION,
                      TYPE,
                      "254.0 508.0 762.0 0.0 0.0",
        ]
        exp_units = "INCHES"
        # Act
        result = self.nScryptConverter.translate(MOVE_COMMAND)
        units = self.nScryptConverter._units
        # Assert
        self.assertEqual(result, exp_result)
        self.assertEqual(units, exp_units)
        
    def test_initial_output(self):
        # Arrange
        exp_result = [VERSION,
                      TYPE,
        ]
        # Act
        result = self.nScryptConverter.translate([])
        # Assert
        self.assertEqual(result, exp_result)

    def test_tool_on_off_command(self):
        # Arrange
        TOOL_ON_OFF_COMMAND = [
            {"spindle_speed": {"control":"RPM"}},
            {"spindle_speed": {"control": "OFF"}}
        ]
        exp_result = [VERSION,
                      TYPE,
                      "TOOL ON",
                      "TOOL OFF"
        ]
        # Act
        result = self.nScryptConverter.translate(TOOL_ON_OFF_COMMAND)
        # Assert
        self.assertEqual(result, exp_result)
    
    def test_sample_output(self):
        # Arrange
        exp_result = [VERSION,
                      TYPE,
                      "!INVALID COMMAND: {'title': {'type': 'Pro/CLfile', 'version': '11.0 - 11.0.0.0'}}",
                      "!INVALID COMMAND: {'manufacturer_number': {'manufacturer_number': 'MFG0006'}}",
                      "!INVALID COMMAND: {'part_number': {'part_number': 'MFG0006'}}",
                      "!INVALID COMMAND: {'feature_number': {'feature_number': '402'}}",
                      "!INVALID COMMAND: {'machine_info': {'machine_type': 'UNCX01', 'machine_number': '1'}}",
                      "!INVALID COMMAND: {'geometry_type': {'geometry_type': 'OUTPUT_ON_CENTER'}}",
                      "!INVALID COMMAND: {'tool': {'tool': '1'}}",
                      "!INVALID COMMAND: {'tool_size': {'tool_size': '0.500000'}}",
                      "!INVALID COMMAND: {'coordinate_system': {'coordinate_system': 'xyz'}}",
                      "TOOL ON",
                      "!INVALID COMMAND: {'coolant': {'bool': True}}",
                      "!INVALID COMMAND: {'max_speed': {'bool': True}}",
                      "-8.889999999999999 127.27214285678 31.115000000000002 0.0 0.0",
                      "!INVALID COMMAND: {'speed': {'speed': 10.0}}",
                      "-8.889999999999999 127.27214285678 27.94 0.0 0.0",
                      "85.09 127.27214285678 27.94 0.0 0.0",
                      "85.09 127.27214285678 30.479999999999997 0.0 0.0",
                      "TOOL OFF"
        ]
        # Act
        result = self.nScryptConverter.translate(PARSED_COMMANDS)
        # Assert
        self.assertEqual(result, exp_result)

if __name__ == "__main__":
    unittest.main()