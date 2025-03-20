# GUI Manual Testing
## Overview
Unlike some other GUI frameworks, tkinter does not have its own testing framework. Although some automated testing is possible with existing testing frameworks like Python's unittest, it can only perform relatively simple tests via some work arounds. Some core functionality of the GUI requires the GUI to actually be running with its internal loop, which makes it difficult to test with traditional testing scripts. Since the GUI is fairly simple, manual testing should be sufficient to verify that the GUI functions properly.

## Procedure
Follow the following procedure to manually test GUI functionality. The steps are meant to test a range of cases to ensure the GUI has been implemented properly to prevent or handle invalid interactions by the user. If there is a contradiction discovered, ensure that the procedure has been written correctly and/or that the GUI implementation is correct. Does not test for loading/saving of parameter subsystem. 
1. Launch the program.
2. Check the following:
    - Select Import File Button is INTERACTABLE
    - Conversion Settings Button is NOT INTERACTABLE
    - Printer Parameters Button is NOT INTERACTABLE
    - Set Export Destination Button is NOT INTERACTABLE
    - Start Conversion Button is NOT INTERACTABLE
3. Click Select Import File Button.
4. Cancel File Selection.
5. Check that a status message appears: "Select File Import: Cancelled"
6. Click Select Import File Button.
7. Open a file from the /tests/resources directory
8. Check that a status message appears: "Select File Import: Successful"
9. Check that the Import Filepath is accurately reflected on the main menu.
10. Click on the Conversion Settings Button.
11. Select Printer Type.
12. Close the Conversion Settings Window WITHOUT SAVING.
13. Check the following:
    - Select Import File Button is INTERACTABLE
    - Conversion Settings Button is NOT INTERACTABLE
    - Printer Parameters Button is NOT INTERACTABLE
    - Set Export Destination Button is NOT INTERACTABLE
    - Start Conversion Button is NOT INTERACTABLE
14. Click on the Conversion Settings Button.
15. Select Printer Type.
16. Click Save.
17. Check that a status message appears: "Conversion Settings Saved" with the corresponding settings that were set. 
18. Close the Conversion Settings Window.
19. Check the following:
    - Conversion Settings Button is INTERACTABLE
    - Printer Parameters Button is INTERACTABLE
    - Select Import File Button is INTERACTABLE
    - Set Export Destination Button is INTERACTABLE
    - Start Conversion Button is NOT INTERACTABLE
20. Click on the Printer Parameters Button. (Possibly more thorough testing steps needed.)
21. Select and Save Applicable Printer Parameters.
22. Close Printer Parameters Window.
23. Check the following:
    - Conversion Settings Button is INTERACTABLE
    - Printer Parameters Button is INTERACTABLE
    - Select Import File Button is INTERACTABLE
    - Set Export Destination Button is INTERACTABLE
    - Start Conversion Button is NOT INTERACTABLE
24. Click Set Export Destination Button.
25. Cancel Folder Selection.
26. Check that a status message appears: "Set Export Destination: Cancelled"
27. Check the following:
    - Conversion Settings Button is INTERACTABLE
    - Printer Parameters Button is INTERACTABLE
    - Select Import File Button is INTERACTABLE
    - Set Export Destination Button is INTERACTABLE
    - Start Conversion Button is NOT INTERACTABLE
28. Click Set Export Destination Button.
29. Select Destination Folder.
30. Check that a status message appears: "Set Export Destination: Successful"
31. Check the following:
    - Conversion Settings Button is INTERACTABLE
    - Printer Parameters Button is INTERACTABLE
    - Select Import File Button is INTERACTABLE
    - Set Export Destination Button is INTERACTABLE
    - Start Conversion Button is INTERACTABLE
32. Check that the Export Filepath is accurately reflected on the main menu.
33. Click Start Conversion Button.
34. Check that the Conversion Process is executed with appropriate status messages.