import unittest
import os
import sys
# sys.path.append("../source/transpiler/")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../source/transpiler/")))

from parser import GenericParser

class TestParser(unittest.TestCase):
    def setUp(self):
        #set up temporary files
        self.test_file = "test.ncl.1"
        self.sample_content = """$$* TITLE / 1.0
$$-> CSYS / 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000,  $
            0.0000000000, 1.0000000000, 0.0000000000, 0.0000000000,  $
            0.0000000000, 0.0000000000, 1.0000000000, 0.0000000000
SPINDL / RPM, 1000, FWD
COOLNT / ON
GOTO / -0.3500000000, 5.0107142857, 1.2250000000
FEDRAT / 10.0, IPM
UNITS / INCH
LOADTL / 5
MACHIN / XYZ, 100
PARTNO / 12345
RAPID
FINI
"""
        with open(self.test_file, "w") as f:
            f.write(self.sample_content)
        
        self.parser = GenericParser(self.test_file)

        # Invalid test file
        self.invalid_file = "invalid.txt"
        self.invalid_content = "This is an invalid test file for parser verification."
        with open(self.invalid_file, "w") as f:
            f.write(self.invalid_content)

    def tearDown(self):
        for file in [self.test_file, self.invalid_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_verify_file_valid(self):
        self.parser.verify_file()  

    def test_verify_file_invalid(self):
        parser = GenericParser(self.invalid_file)
        with self.assertLogs("main", level="ERROR") as log:
            parser.verify_file()
        self.assertIn("File type not supported", log.output[0])

    def test_parse_file(self):
        commands = self.parser.parse_file(self.test_file)
        self.assertEqual(len(commands), len(self.sample_content.split("\n")))

    def test_conversion(self):
        self.parser.conversion()
        self.assertGreater(len(self.parser.parsedCommands), 0)

    def test_movement_command(self):
        # Invalid movement command
        move_cmd_invalid = self.parser._movementCommand(["GOTO", "/", "1.0,", "3.0"])
        self.assertIn("ERROR", move_cmd_invalid)

        self.parser.coordinateSystem = "xyz"
        move_cmd_valid = self.parser._movementCommand(["GOTO", "/", "1.0,", "2.0,", "3.0"])
        expected_output = {"move": {"x": 1.0, "y": 2.0, "z": 3.0}}
        self.assertEqual(move_cmd_valid, expected_output)

        self.parser.coordinateSystem = "xyza"
        move_cmd_valid_4d = self.parser._movementCommand(["GOTO", "/", "1.0,", "2.0,", "3.0,", "4.0"])
        expected_output_4d = {"move": {"x": 1.0, "y": 2.0, "z": 3.0, "a": 4.0}}
        self.assertEqual(move_cmd_valid_4d, expected_output_4d)

        self.parser.coordinateSystem = "xyzab"
        move_cmd_valid_5d = self.parser._movementCommand(["GOTO", "/", "1.0,", "2.0,", "3.0,", "4.0,", "5.0"])
        expected_output_5d = {"move": {"x": 1.0, "y": 2.0, "z": 3.0, "a": 4.0, "b": 5.0}}
        self.assertEqual(move_cmd_valid_5d, expected_output_5d)

    def test_spindle_speed(self):
        speed_cmd = self.parser._spindleSpeed(["SPINDL", "/", "ON", "1000"])
        self.assertEqual(speed_cmd["spindle_speed"]["control"], "ON")
        self.assertEqual(speed_cmd["spindle_speed"]["speed"], 1000.0)

    def test_coolant_command(self):
        coolant_on = self.parser._coolantCommand(["COOLNT", "/", "ON"])
        coolant_off = self.parser._coolantCommand(["COOLNT","/", "OFF"])
        self.assertTrue(coolant_on["coolant"]["bool"])
        self.assertFalse(coolant_off["coolant"]["bool"])

    def test_speed_command(self):
        speed_cmd = self.parser._speedCommand(["FEDRAT", "/", "10.0", "IPM"])
        self.assertEqual(speed_cmd["speed"]["speed"], 10.0)

    def test_info_comment(self):
        self.parser._infoCommentCommand(["$$->", "FEATNO", "/", "123"])
        self.assertIn({"feature_number": {"feature_number": "123"}}, self.parser.parsedCommands)

        self.parser._infoCommentCommand(["$$->", "MFGNO", "/", "456"])
        self.assertIn({"manufacturer_number": {"manufacturer_number": "456"}}, self.parser.parsedCommands)

        self.parser._infoCommentCommand(["$$->", "CUTTER", "/", "10.5"])
        self.assertIn({"tool_size": {"tool_size": "10.5"}}, self.parser.parsedCommands)

        self.parser._infoCommentCommand(["$$->", "END"])
        self.assertIn({"end_movement": {"bool": True}}, self.parser.parsedCommands)

        self.parser._infoCommentCommand(["$$->", "CUTCOM_GEOMETRY_TYPE", "/", "SPHERE"])
        self.assertIn({"geometry_type": {"geometry_type": "SPHERE"}}, self.parser.parsedCommands)

        self.parser._infoCommentCommand(["$$->", "CSYS", "/", "1", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0"])
        self.assertTrue(self.parser.coordinateSearch) 

        self.parser._infoCommentCommand(["$$->", "UNKNOWN_CMD", "/", "DATA"])
        self.assertIn(["UNKNOWN_CMD", "/", "DATA"], self.parser.unparsedCommands)

    def test_check_orientation(self):
        self.parser.coordinateSystem = ""

        self.parser._checkOrientationLine(["1", "1", "1"])
        self.assertEqual(self.parser.coordinateSystem, "xyz")

        self.parser.coordinateSystem = ""
        self.parser._checkOrientationLine(["1", "1", "1", "1"])
        self.assertEqual(self.parser.coordinateSystem, "xyza")

        self.parser.coordinateSystem = ""
        self.parser._checkOrientationLine(["1", "1", "1", "1", "1"])
        self.assertEqual(self.parser.coordinateSystem, "xyzab")

        self.parser.coordinateSystem = ""
        self.parser._checkOrientationLine(["1", "0", "1"])
        self.assertEqual(self.parser.coordinateSystem, "xz")

        self.parser.coordinateSystem = ""
        self.parser._checkOrientationLine(["0", "1", "0", "0", "1"])
        self.assertEqual(self.parser.coordinateSystem, "yb")

        self.parser.coordinateSystem = ""
        self.parser._checkOrientationLine([])
        self.assertEqual(self.parser.coordinateSystem, "")

        self.parser.coordinateSystem = ""
        self.parser._checkOrientationLine(["0", "0", "0", "0", "0"])
        self.assertEqual(self.parser.coordinateSystem, "")


    def test_str_representation(self):
        self.parser.conversion()
        output = str(self.parser)
        self.assertTrue(len(output) == 508)

    def test_save_output(self):
        output_file = "output.txt"
        self.parser.conversion()
        self.parser.save(output_file)

        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)

    def test_parse_commands(self):
        parsed_commands = self.parser.parse_commands()
        self.assertGreater(len(parsed_commands), 0)

if __name__ == "__main__":
    unittest.main()