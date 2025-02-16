import unittest
import sys
sys.path.append("../source/transpiler/")
from acsplConverter import AcsplConverter
from acsplConverter import MACHINE_SETUP, STOP, CLOSE_INKJET, OPEN_INKJET, START_COMMENT

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


def _print(results):
    for result in results:
        print(result)


class TestAcsplConverter(unittest.TestCase):
    def setUp(self):
        self.acsplConverter = AcsplConverter()

    def test_acspl_constructor(self):
        self.assertIsNotNone(self.acsplConverter)
        self.assertIsNotNone(self.acsplConverter.machine)

    def test_invalid_command(self):
        # Arrange
        INVALID_COMMAND = {
            "INVALID": {}
        }
        exp_result = [MACHINE_SETUP,
                      START_COMMENT,
                      "!INVALID COMMAND: {'INVALID': {}}",
                      STOP
        ]
        # Act
        result = self.acsplConverter.translate([INVALID_COMMAND])
        # Assert
        self.assertEqual(result, exp_result)

    def test_ptp_command(self):
        # Arrange
        PTP_COMMAND = [
            {"max_speed": {"bool": "True"}},
            {"move": {"x": "10.0", "y": "20.0", "z": "30.0"}}
        ]
        exp_result = [MACHINE_SETUP,
                      START_COMMENT,
                      "PTP/EV (10,11,12,14,15), 10.0, 20.0, 30.0, 0.0, 0.0, gDblRapidSpeed",
                      STOP
        ]
        # Act
        result = self.acsplConverter.translate(PTP_COMMAND)
        # Assert
        self.assertEqual(result, exp_result)

    def test_line_command(self):
        # Arrange
        LINE_COMMAND = [
            {"speed": {"speed": "10.0"}},
            {"move": {"x": "10.0", "y": "20.0", "z": "30.0"}}
        ]
        exp_result = "LINE/V (10,11,12,14,15), 10.0, 20.0, 30.0, 0.0, 0.0, gDblProcessSpeed"
        # Act
        result = self.acsplConverter.translate(LINE_COMMAND)
        # Assert
        self.assertIn(exp_result, result)

    def test_ptp_xseg_line_command(self):
        # Arrange
        XSEG_COMMAND = [
            {"max_speed": {"bool": "True"}},
            {"move": {"x": "10.0", "y": "20.0", "z": "30.0"}},
            {"speed": {"speed": "10.0"}},
            {"move": {"x": "40.0", "y": "50.0", "z": "60.0"}},
            {"max_speed": {"bool": "True"}}
        ]
        exp_result = [MACHINE_SETUP,
                      START_COMMENT,
                      "PTP/EV (10,11,12,14,15), 10.0, 20.0, 30.0, 0.0, 0.0, gDblRapidSpeed",
                      OPEN_INKJET,
                      "XSEG/A (10,11,12,14,15), 10.0, 20.0, 30.0, 0.0, 0.0, CRangle",
                      "LINE/V (10,11,12,14,15), 40.0, 50.0, 60.0, 0.0, 0.0, gDblProcessSpeed",
                      CLOSE_INKJET,
                      STOP
        ]
        # Act
        result = self.acsplConverter.translate(XSEG_COMMAND)
        # Assert
        self.assertEqual(result, exp_result)

    def test_feature_number(self):
        # Arrange
        FEATURE_NUMBER = [
            {"feature_number": {"feature_number": "1234"}}
        ]
        exp_result = "! Feature Number: 1234"
        # Act
        result = self.acsplConverter.translate(FEATURE_NUMBER)
        # Assert
        self.assertIn(exp_result, result)

    def test_manufacturer_number(self):
        # Arrange
        MANUFACTURER_NUMBER = [
            {"manufacturer_number": {"manufacturer_number": "5678"}}
        ]
        exp_result = "! Manufacturer Number: 5678"
        # Act
        result = self.acsplConverter.translate(MANUFACTURER_NUMBER)
        # Assert
        self.assertIn(exp_result, result)

    def test_part_number(self):
        # Arrange
        PART_NUMBER = [
            {"part_number": {"part_number": "9012"}}
        ]
        exp_result = "! Part Number: 9012"
        # Act
        result = self.acsplConverter.translate(PART_NUMBER)
        # Assert
        self.assertIn(exp_result, result)

    def test_end_movement_whileDispensing(self):
        # Arrange
        END_MOVEMENT = [
            {"end_movement": {"bool": "True"}}
        ]
        self.acsplConverter.machine.is_dispensing = True
        # Act
        result = self.acsplConverter.translate(END_MOVEMENT)
        # Assert
        self.assertIn(CLOSE_INKJET, result)

    def test_print_parsed_commands(self):
        results = self.acsplConverter.translate(PARSED_COMMANDS)
        #_print(results)


if __name__ == "__main__":
    unittest.main()
