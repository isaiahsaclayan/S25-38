# Purpose
This directory contains unit and integration tests to verify the functionality of our system and its components.

# How to Execute All Tests
1. Open a terminal and navigate to the project root.
2. Navigate to the test directory: `cd tests`
3. Execute the command: `python -m unittest discover -v`  
*`-v` can be omitted for a less verbose report.*

# How to Execute an Individual Test File
1. Open a terminal and navigate to the project root.
2. Navigate to the test directory: `cd tests`
3. Execute the command: `python -m unittest <name_of_test_file> -v`  
*`-v` can be omitted for a less verbose report.*

# Developer Notes

### Naming Convention
- Test files should be named `test_<module_name>.py`
- Test classes should be named `Test<module_name>`
- Test methods should be named `test_<method_name>`