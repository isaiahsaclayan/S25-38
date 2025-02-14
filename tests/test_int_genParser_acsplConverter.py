import unittest
import sys
sys.path.append("../source/transpiler/")
from acsplConverter import AcsplConverter
from parser import GenericParser

class TestIntegrationParserToACSPL(unittest.TestCase):
    def setUp(self):
        self.acsplConverter = AcsplConverter()
        self.genericParser = GenericParser("../tests/resources/op010.ncl.1")

    def test_conversion_to_translate_noException(self):
        # Arrange
        parsed_commands = self.genericParser.parse_commands() # Parse the file and get the parsed commands

        # Act & Assert
        try:
            self.acsplConverter.translate(parsed_commands)
        except Exception as e:
            self.fail(f"Exception raised during translation: {e}")

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
