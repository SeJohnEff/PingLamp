# PingLamp
A design that turns on a lamp (Hazard Flash Lamp) when ping is successful

The design idea is to have a visual confirmation when a devive moving into a wireless network gets internet access.
Ping to 8.8.8.8 is done from the device
A USB relay is activated if ping is successful and deactivated at timeout.
A strobe light is connected via the relay


Please make sure to install the ping3 library if you haven't already by running:


pip install ping3
Additionally, ensure that you have the appropriate serial communication libraries installed, such as pyserial, which can be installed via:

pip install pyserial

## Hardware:
- A NUC running Ubuntu (or any harware at your choice)
- Warning Flashing Light: [amazon.se](https://www.amazon.se/-/en/dp/B07FP3WT89?ref=ppx_yo2ov_dt_b_product_details&th=1). Built in battery and a button. Press 1=flash 2=steady light 3=off and back to flash if you press again. The button will be replaced by the relay
- USB relay card: [amazon.se](https://www.amazon.se/dp/B07DJ549LX?psc=1&ref=ppx_yo2ov_dt_b_product_details). An USB to serial design with an MCU. The MCU receives the serial communication, decodes it and controls the relay. You send a string to it and relay goes on or off
## Software
#### on_off_by_ping.zsh
This might be sufficient for your purpose and is a stand alone shell script. I prefere the service implementation below. It has a hard-coded path to the USB Relay, checks for successful ping and turns on the lamp (Relay on/off/on/off) and if ping timeout it turns off the lamp (Relay on/off)
#### Service
The service makes sure main.py starts at boot
#### main
## Circuit Diagram
The USB relay did not fit with USB cable attached so I decided to solder the cable directly on the PCB
NOTE! If you decide to drill a hole in the lamp, don't forget to pull it through BEFORE you solder
![](/assets/diagram.jpg)
## Images
![USB Relay board](/assets/usb_relay.jpg)
![USB cables soldered](/assets/usb_cables_soldered.jpg)
![Lamp](/assets/lamp_pcb_button.jpg)
![Lamp PCB](/assets/lamp_pcb.jpg)
![Lamp,disassembled](/assets/lamp_disassembled.jpg)
