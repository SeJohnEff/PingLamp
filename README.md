# PingLamp
A design that turns on a lamp (Hazard Flash Lamp) when ping is successful

The design idea is to have a visual confirmation when a devive moving into a wireless network gets internet access.
Ping to 1.1.1.1 is done from the device
A USB relay is activated if ping is successful and deactivated at timeout.
A strobe light is connected via the realy and a 12V battery


Please make sure to install the ping3 library if you haven't already by running:


pip install ping3
Additionally, ensure that you have the appropriate serial communication libraries installed, such as pyserial, which can be installed via:

pip install pyserial
