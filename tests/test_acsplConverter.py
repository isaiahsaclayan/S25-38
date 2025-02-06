import unittest
import sys
sys.path.append("../source/transpiler/")
from acsplConverter import AcsplConverter
from acsplConverter import MACHINE_SETUP, STOP, CLOSE_INKJET, OPEN_INKJET

PARSED_COMMANDS = [
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

SMALL_PARSED_COMMANDS = PARSED_COMMANDS[:8]


PTP_COMMAND = [
    {"max_speed": {"bool": "True"}},
    {"move": {"x": "10.0","y": "20.0","z": "30.0"}}
]

INVALID_COMMAND = {
        "INVALID": {}
    }

class TestAcsplConverter(unittest.TestCase):
    def setUp(self):
        self.acsplConverter = AcsplConverter()

    def test_constructor(self):
        self.assertIsNotNone(self.acsplConverter)

    def test_invalid_command(self):
        result_error_str = self.acsplConverter.translate([INVALID_COMMAND])[1]
        exp_error_str = "!INVALID COMMAND: {'INVALID': {}}"
        self.assertEqual(result_error_str, exp_error_str)

    def test_PTP_command(self):
        result = self.acsplConverter.translate(PTP_COMMAND)[1]
        exp_result = f"PTP/EV (10,11,12), 10.0, 20.0, 30.0, gDblRapidSpeed"
        self.assertEqual(result, exp_result)

    def test_LINE_command(self):
        pass

    def test_small_parsed_commands(self):
        results = self.acsplConverter.translate(SMALL_PARSED_COMMANDS)


if __name__ == "__main__":
    unittest.main()