import unittest
import sys
sys.path.append("../source/transpiler/")
from acsplConverter import AcsplConverter

PARSED_COMMAND_LIST = [
    {'coolant': {'bool': True}},
    {'max_speed': {'bool': True}},
    {'move': {'x': -0.35, 'y': 5.0107142857, 'z': 1.225}},
    {'speed': {'speed': 10.0}},
    {'move': {'x': -0.35, 'y': 5.0107142857, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 5.0107142857, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 5.0107142857, 'z': 1.2}},
    {'max_speed': {'bool': True}},
    {'move': {'x': 3.35, 'y': 5.0107142857, 'z': 1.225}},
    {'max_speed': {'bool': True}},
    {'move': {'x': -0.35, 'y': 4.7714285714, 'z': 1.225}},
    {'speed': {'speed': 10.0}},
    {'move': {'x': -0.35, 'y': 4.7714285714, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 4.7714285714, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 4.7714285714, 'z': 1.2}},
    {'max_speed': {'bool': True}},
    {'move': {'x': 3.35, 'y': 4.7714285714, 'z': 1.225}},
    {'max_speed': {'bool': True}},
    {'move': {'x': -0.35, 'y': 4.5321428571, 'z': 1.225}},
    {'speed': {'speed': 10.0}},
    {'move': {'x': -0.35, 'y': 4.5321428571, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 4.5321428571, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 4.5321428571, 'z': 1.2}},
    {'max_speed': {'bool': True}},
    {'move': {'x': 3.35, 'y': 4.5321428571, 'z': 1.225}},
    {'max_speed': {'bool': True}},
    {'move': {'x': -0.35, 'y': 4.2928571429, 'z': 1.225}},
    {'speed': {'speed': 10.0}},
    {'move': {'x': -0.35, 'y': 4.2928571429, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 4.2928571429, 'z': 1.1}},
    {'move': {'x': 3.35, 'y': 4.2928571429, 'z': 1.2}},
    {'max_speed': {'bool': True}},
    {'move': {'x': 3.35, 'y': 4.2928571429, 'z': 1.225}}
   ]

MOVE_COMMAND = {
        "move": {
            "X": "10",
            "Y": "20",
            "Z": "30",
            "A": "40",
            "B": "50"
        }
    }

INVALID_COMMAND = {
        "INVALID": {
            "X": "10",
            "Y": "20",
            "Z": "30",
            "A": "40",
            "B": "50"
        }
    }

class TestAcsplConverter(unittest.TestCase):
    def setUp(self):
        self.acsplConverter = AcsplConverter()

    def test_constructor(self):
        self.assertIsNotNone(self.acsplConverter)

    def test_invalid_command(self):
        result_error_str = self.acsplConverter.translate([INVALID_COMMAND])[1]
        exp_error_str = "!INVALID COMMAND: {'INVALID': {'X': '10', 'Y': '20', 'Z': '30', 'A': '40', 'B': '50'}}"
        self.assertEqual(result_error_str, exp_error_str)

    def test_small_parsed_commands(self):
        result_str = self.acsplConverter.translate(PARSED_COMMAND_LIST)


if __name__ == "__main__":
    unittest.main()