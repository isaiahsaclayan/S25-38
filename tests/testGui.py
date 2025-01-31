import unittest
from unittest import mock
import sys

sys.path.append("../source/transpiler/")
from guiRoot import GuiRoot

class TestGuiButtons(unittest.TestCase):
    def setUp(self):
        self.guiRootObj = GuiRoot()

    def testImport(self):
        importMock = mock.Mock()

        self.guiRootObj.importFileButton.configure(command = importMock)
        self.guiRootObj.importFileButton.invoke()
        
        importMock.assert_called()

if __name__ == "__main__":
    unittest.main()