# Utility Imports
import unittest
from unittest.mock import patch, mock_open # For mocking the file
import sys

# Transpiler Imports
sys.path.append("../source/transpiler/")
from acsplConverter import AcsplConverter
from parser import GenericParser

class TestIntegrationParserToACSPL(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.acsplConverter = AcsplConverter()
        self.genericParser = GenericParser("../tests/resources/op010.ncl.1")

    def test_conversion_to_translate_noException(self):
        """
        Ensure parsing and conversion do not raise any exceptions.
        """
        # Arrange
        parsed_commands = self.genericParser.parse_commands() # Parse the file and get the parsed commands

        # Act & Assert
        try:
            self.acsplConverter.translate(parsed_commands)
        except Exception as e:
            self.fail(f"Exception raised during translation: {e}")

    def test_conversion_to_translation_noInvalidCommands(self):
        """
        Ensure translated output does not contain invalid commands, as all in the current
        Creo file are supported.
        """
        # Arrange
        parsed_commands = self.genericParser.parse_commands()

        # Act
        translated_commands = self.acsplConverter.translate(parsed_commands)

        # Assert
        for command in translated_commands:
            self.assertNotIn("INVALID", command)

    def test_conversion_to_translation_typeCheck(self):
        """
        Ensure the translated output is a list of strings.
        """
        # Arrange
        parsed_commands = self.genericParser.parse_commands()

        # Act
        translated_commands = self.acsplConverter.translate(parsed_commands)

        # Assert
        self.assertIsInstance(translated_commands, list) # Ensure the output is a list
        self.assertGreater(len(translated_commands), 0) # Ensure there are commands
        # Ensure all commands are strings
        for command in translated_commands:
            self.assertIsInstance(command, str)


    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_input_file(self, mock_file):
        """
        Ensure an empty file does not raise any exceptions and does not get processed.
        """
        # Arrange, use the mock to simulate an empty file
        mock_parser = GenericParser("empty_file.ncl.1")

        # Act
        parsed_commands = mock_parser.parse_commands()
        translated_command = self.acsplConverter.translate(parsed_commands)

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
        translated_command = self.acsplConverter.translate(parsed_commands)

        # Assert
        self.assertEqual(len(parsed_commands), 0) # Ensure the command was not processed by parser
        self.assertEqual(len(translated_command), 0) # Ensure the command was not translated by converter
        self.assertIn("INVALIDCOMMAND", mock_parser.unparsedCommands[0]) # Ensure the invalid command is in the unparsed list

    # TODO remove this test before delivery
    def test_print(self):
        # Arrange
        parsed_commands = self.genericParser.parse_commands()
        # Act
        translated_commands = self.acsplConverter.translate(parsed_commands)
        # Assert
        for command in translated_commands:
            print(command)

if __name__ == "__main__":
    unittest.main()
