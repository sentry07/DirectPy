DirectPy
========

A python library for interacting with DirecTV receivers. For more information on the protocol, please see:
https://www.satinstalltraining.com/homeautomation/DTV-MD-0359-DIRECTV_SHEF_Command_Set-V1.3.C.pdf

This class import provides basic functions for controlling a DirecTV receiver, either by setting its
channel directly or emulating remote button presses, as well as the ability to retrieve information
from the receiver about its status, current channel, and program information.

Example use:

from DirectPy import directv

dtv = directv('192.168.1.10')   # Initiates a new object using the IP address of the receiver
dtv.get_tuned()                 # Gets the currently tuned channel
dtv.set_channel('249')          # Sets the channel to 249
dtv.get_channel('264')          # Gets information on the program that is on channel 264 currently
dtv.key_press('poweroff')       # Emulates pressing the power off button
dtv.key_press('poweron')        # Emulates pressing the power on button
