# paramClass.py

This file contains 4 classes: a parameter class for nscrypt and optomec separately, as well as a gui class form optomec and nscrypt separately.

# NscryptParameters class

This holds a simple array of float parameters for conversions to an nScrypt output. The first parameter represents whether spherical coordinates[0] or vector coordinates[1] are being used for the print. The other parameters are all technically placeholders, and are not set to anything meaningful at the moment. This is simply done to easily allow future parameters to be added.

In the nScrypt parameter GUI, you will be unable to save your selected parameter values unless the coordinates parameter is set to eitehr 1 or 0.

# OptomecParameters class

This holds a simple array of float parameters for conversions to an Optomec output. The first 2 parameters are open-delay and close-delay respectively. These are measured in milliseconds. The other parameters are all technically placeholders, and are not set to anything meaningful at the moment. This is simply done to easily allow future parameters to be added.

In the Optomec parameter GUI, you will be unable to save your selected parameter values unless the the open-delay and close-delay parameters both have values between 0 and 1000.

# NscryptParameterGui and OptomecParameterGui class

Both of the gui classes have a set of 3 existing parameter controls, a display of all the current parameter values, an OK button, and a cancel button. The 3 parameter controls are text boxes that allow the user to enter a value for the respective first 3 parameters. More buttons can easily be added, but as all but the first couple parameters are currently placeholders, this has not been done for current ease of use of the software. Each text box can be filled with float numbers only.

The two buttons at the bottom of both parameter GUIs are the OK and cancel button. Upon clicking either, the parameter GUI window will close. The difference is that the OK button saves your currently entered parameter values before closing, and the cancel button does not, keeping your previously saved values instead.

For both the NscryptParameterGui and the OptomecParameterGui, clicking the OK button will only save your parameters if all the parameters have valid values that are within acceptable ranges. These exist as safeguards against the user setting unreasonable or meaningless values for the parameters. These bounds can be changed in the paramClass.py code.

# parameters.json

Whenever a file is imported into the software, after the user selects either the Optomec or nScrypt printer, a blank parameter profile is created for that imported file. The set of parameters as well as the name of the imported file are stored as a dictionary in a .json file called parameters.json. Whenever that same file is loaded up in the future, if it has an existing parameter profile, this will be used instead of having a blank parameter profile. This json file will only be updated when the user presses OK in the parameter GUI window. Manually tampering with the parameters.json file can lead to corruption of that file, and if corruption is detected, the parameter file will be overwritten, losing any and all saved parameter profiles.
