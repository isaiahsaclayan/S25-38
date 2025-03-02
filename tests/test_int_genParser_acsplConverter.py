import unittest
import sys
sys.path.append("../source/transpiler/")
from acsplConverter import AcsplConverter
from parser import GenericParser

class TestIntegrationParserToACSPL(unittest.TestCase):
    def setUp(self):
        """ Set up the test environment. """
        self.acsplConverter = AcsplConverter()
        self.genericParser = GenericParser("../tests/resources/op010.ncl.1")

    def test_conversion_to_translate_noException(self):
        """ Ensure parsing and conversion do not raise any exceptions. """
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
