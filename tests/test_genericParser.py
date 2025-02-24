import pytest
import os
import sys

sys.path.append("../source/transpiler/")

from parser import genericParser

def test_verify_file(tmp_path):
    filename = tmp_path / "test.txt"
    filename.write_text("invalid content")
    
    parser = genericParser(str(filename))
    with pytest.raises(SystemExit):  # Assuming logger.error leads to exit
        parser.verify_file()

def test_parse_file(tmp_path):
    filename = tmp_path / "test.ncl.1"
    filename.write_text("$$* TITLE 1.0\nGOTO 1,2,3")
    
    parser = genericParser(str(filename))
    assert parser.creoCommands == ["$$* TITLE 1.0", "GOTO 1,2,3"]

def test_conversion(tmp_path):
    filename = tmp_path / "test.ncl.1"
    filename.write_text("$$* TITLE 1.0\nGOTO 1,2,3\nSPINDL ON 500\nCOOLNT ON\nFINI")

    parser = genericParser(str(filename))
    parser.conversion()
    
    assert {"title": {"type": "TITLE", "version": "1.0"}} in parser.parsedCommands
    assert {"move": {}} in parser.parsedCommands  # Coordinate system not set
    assert {"spindle_speed": {"control": "ON", "speed": 500.0}} in parser.parsedCommands
    assert {"coolant": {"bool": True}} in parser.parsedCommands
    assert {"finish_file": {"bool": True}} in parser.parsedCommands

def test_movement_command():
    parser = genericParser("dummy_file.ncl")
    parser.coordinateSystem = ["X", "Y", "Z"]
    command = ["GOTO", "", "1.0,", "2.0,", "3.0"]
    parsed = parser._movementCommand(command)
    assert parsed == {"move": {"X": 1.0, "Y": 2.0, "Z": 3.0}}

def test_spindle_speed():
    parser = genericParser("dummy_file.ncl")
    command = ["SPINDL", "", "ON", "1000"]
    parsed = parser._spindleSpeed(command)
    assert parsed == {"spindle_speed": {"control": "ON", "speed": 1000.0}}

def test_coolant_command():
    parser = genericParser("dummy_file.ncl")
    assert parser._coolantCommand(["COOLNT", "", "ON"]) == {"coolant": {"bool": True}}
    assert parser._coolantCommand(["COOLNT", "", "OFF"]) == {"coolant": {"bool": False}}

def test_save(tmp_path):
    filename = tmp_path / "output_test.txt"
    parser = genericParser("dummy_file.ncl")
    parser.parsedCommands = [{"example": "test"}]
    parser.save(str(filename))
    
    assert filename.read_text().strip() == "{'example': 'test'}"

if __name__ == "__main__":
    pytest.main()
