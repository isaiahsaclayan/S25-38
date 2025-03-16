# GUI Manual Testing
## Overview
Unlike some other GUI frameworks, tkinter does not have its own testing framework. Although some automated testing is possible with existing testing frameworks like Python's unittest, it can only perform relatively simple tests via some work arounds. Some core functionality of the GUI requires the GUI to actually be running with its internal loop, which makes it difficult to test with traditional testing scripts. Since the GUI is fairly simple, manual testing should be sufficient to verify that the GUI functions properly.

## Procedure
Follow the following procedure to manually test GUI functionality. The steps are meant to test a range of cases to ensure the GUI has been implemented properly to prevent or handle invalid interactions by the user. If there is a contradiction discovered, ensure that the procedure has been written correctly and/or that the GUI implementation is correct.
1. Launch the program.
2. Check the following:
    - Conversion Settings Button is INTERACTABLE
    - Printer Parameters Button is NOT INTERACTABLE
    - Select Import File Button is NOT INTERACTABLE
    - Set Export Destination Button is NOT INTERACTABLE
3. Click on the Conversion Settings Button.
4. Select Printer Type.
5. Close the Conversion Settings Window WITHOUT SAVING.
6. Check the following (Repeat of Step 2):
    - Conversion Settings Button is INTERACTABLE
    - Printer Parameters Button is NOT INTERACTABLE
    - Select Import File Button is NOT INTERACTABLE
    - Set Export Destination Button is NOT INTERACTABLE
7. Click on the Conversion Settings Button.
8. Select Printer Type.
9. Click Save.
10. Check that a status message appears: "Conversion Settings Saved" with the corresponding settings that were set. 
11. Close the Conversion Settings Window.
12. Check the following (Repeat of Step 2):
    - Conversion Settings Button is INTERACTABLE
    - Printer Parameters Button is INTERACTABLE
    - Select Import File Button is INTERACTABLE
    - Set Export Destination Button is INTERACTABLE
13. Click on the Printer Parameters Button. (Possibly more thorough testing steps needed.)
14. Select and Save Applicable Printer Parameters.
15. Close Printer Parameters Window.
16. Click Start Conversion Button.
17. Check that status messages appear indicating that import/export paths were not set: 
    - "Cannot start conversion: Please select import file"
    - "Cannot start conversion: Please set export destination"

18. Click Select Import File Button.
19. Cancel File Selection.
20. Check that a status message appears: "Select File Import: Cancelled"
21. Click Select Import File Button.
22. Open a file from the /tests/resources directory
23. Check that a status message appears: "Select File Import: Successful"
24. Check that the Import Filepath is accurately reflected on the main menu.
25. Click Start Conversion Button.
26. Check that a status message appears: 
    - "Cannot start conversion: Please set export destination"
27. Click Set Export Destination Button.
28. Cancel Folder Selection.
29. Check that a status message appears: "Set Export Destination: Cancelled"
30. Click Set Export Destination Button.
31. Select Destination Folder.
32. Check that a status message appears: "Set Export Destination: Successful"
33. Check that the Export Filepath is accurately reflected on the main menu.
34. Click Start Conversion Button.
35. Check that the Conversion Process is executed with appropriate status messages.