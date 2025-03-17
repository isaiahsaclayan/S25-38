import unittest
import sys
sys.path.append("../source/transpiler/")
from unittest.mock import patch, mock_open # For mocking the file
from nscryptConverter import NscryptConverter
from parser import GenericParser

def _print(results):
    for result in results:
        print(result)

class TestIntegrationParserTonScrypt(unittest.TestCase):
    def setUp(self):
        self.nScryptConverter = NscryptConverter()
        self.genericParser = GenericParser("../tests/resources/op010.ncl.1")

    def test_conversion_to_translate_noException(self):
        # Arrange
        parsed_commands = self.genericParser.parse_commands() # Parse the file and get the parsed commands

        # Act & Assert
        try:
            self.nScryptConverter.translate(parsed_commands)
        except Exception as e:
            self.fail(f"Exception raised during translation: {e}")

    def test_conversion_to_translation_noInvalidCommands(self):
        # Arrange
        parsed_commands = self.genericParser.parse_commands()

        # Act
        translated_commands = self.nScryptConverter.translate(parsed_commands)

        # Assert
        for command in translated_commands:
            self.assertNotIn("INVALID", command)
            
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_input_file(self, mock_file):
        """
        Ensure an empty file does not raise any exceptions and does not get processed.
        """
        # Arrange, use the mock to simulate an empty file
        mock_parser = GenericParser("empty_file.ncl.1")

        # Act
        parsed_commands = mock_parser.parse_commands()
        translated_command = self.nScryptConverter.translate(parsed_commands)

        # Assert
        self.assertEqual(len(parsed_commands), 0) # Ensure no commands were parsed
        self.assertEqual(len(translated_command), 0) # Ensure no commands were translated

    @patch("builtins.open", new_callable=mock_open, read_data="INVALIDCOMMAND / 1.0, 2.0, 3.0")
    def test_invalid_command(self, mock_file):
        """
        Ensure an invalid command does not raise any exceptions and does not get processed.
        """
        # Arrange, use the mock to simulate an invalid command
        mock_parser = GenericParser("invalid_command.ncl.1")

        # Act
        parsed_commands = mock_parser.parse_commands()
        translated_command = self.nScryptConverter.translate(parsed_commands)

        # Assert
        self.assertEqual(len(parsed_commands), 0) # Ensure the command was not processed by parser
        self.assertEqual(len(translated_command), 0) # Ensure the command was not translated by converter
        self.assertIn("INVALIDCOMMAND", mock_parser.unparsedCommands[0]) # Ensure the invalid command is in the unparsed list

    @patch("builtins.open", new_callable=mock_open, read_data="COOLNT / ON")
    def test_ignored_command(self, mock_file):
        """
        Ensures a command that is supported by parser, but not converter is processed correctly.
        Parser should process the command but the converter should not.
        """
        # Arrange, use the mock to simulate an ignored command
        mock_parser = GenericParser("ignored_command.ncl.1")

        # Act
        parsed_commands = mock_parser.parse_commands()
        translated_command = self.nScryptConverter.translate(parsed_commands)

        # Assert
        # Ensure the command was processed by the parser
        self.assertEqual(len(parsed_commands), 1)
        # Ensure the command was not translated by the converter, there should only be 3 lines appended
        # the machine setup code block, a start comment, and the stop code block
        self.assertEqual(len(translated_command), 2)
        
    @patch("builtins.open", new_callable=mock_open, read_data="UNITS / INCHES\nGOTO / 1, -1, 2")
    def test_unit_change_command(self, mock_file):
        """
        Ensures that units are changed according to what the parser takes in
        """
        # Arrange, use the mock to simulate an ignored command
        mock_parser = GenericParser("unit_change.ncl.1")

        # Act
        parsed_commands = mock_parser.parse_commands()
        translated_command = self.nScryptConverter.translate(parsed_commands)

        # Assert
        # Ensure the command was processed by the parser
        self.assertEqual(len(parsed_commands), 2)
        self.assertEqual(len(translated_command), 3)
        self.assertEqual(translated_command[2], "25.4 -25.4 50.8 0.0 0.0")
        
    def test_axis_command(self):
        """
        Ensures the proper axis are translated regardless of the order they are in
        """
        mock_parser = GenericParser("../tests/resources/op010-axis_change.ncl.1")

        # Act
        parsed_commands = mock_parser.parse_commands()
        translated_command = self.nScryptConverter.translate(parsed_commands)

        # Assert
        # Checking if axis translated correctly
        self.assertEqual(translated_command[3], f"{1.2250000000*25.4} {-0.3500000000*25.4} {5.0107142857*25.4} 0.0 0.0")

    # TODO remove this test before delivery
    def test_print(self):
        # Arrange
        parsed_commands = self.genericParser.parse_commands()
        # Act
        translated_commands = self.nScryptConverter.translate(parsed_commands)

        #_print(translated_commands)

if __name__ == "__main__":
    unittest.main()