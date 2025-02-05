import unittest
import sys
sys.path.append("../source/transpiler/")
from acsplConverter import AcsplConverter

MOVE_COMMAND = {
        "MOVE": {
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

if __name__ == "__main__":
    unittest.main()