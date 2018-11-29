DirectPy
========

A Python 2.5+/3 library for interacting with DirecTV receivers. For more information on setting up your receiver to use the API, please see:
http://forums.solidsignal.com/docs/DTV-MD-0359-DIRECTV_SHEF_Command_Set-V1.3.C.pdf

This class import provides basic functions for controlling a DirecTV receiver, either by setting its
channel directly or emulating remote button presses, as well as the ability to retrieve information
from the receiver about its status, current channel, and program information.

Example use:
============
from DirectPy import DIRECTV

\# Initiate a new object using the IP address of the receiver
dtv = DIRECTV('192.168.1.10')

\# Emulate pressing the power on button
dtv.key_press('poweron')

\# Get the currently tuned channel
dtv.get_tuned()

\# Set the channel to 249
dtv.tune_channel('249')

\# Get information about the program that is on channel 264
dtv.get_channel('264')

\# Emulate pressing the power off button
dtv.key_press('poweroff')

\# Retrieve the different RVU's attached
dtv.get_locations()

\# Retrieve access card ID, receiver ID, STB software version, system time, and version of current implementation
dtv.get_version()

\# Retrieve serial number
dtv.get_serialnum()

