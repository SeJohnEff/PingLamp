import subprocess
import time
import ping3
import serial.tools.list_ports

# Function to turn the lamp on
def turn_lamp_on(device):
    # Switch the relay on and off twice to turn the lamp on
    with open(device, "w") as dev:
        dev.write(b"\xA0\x01\x01\xA2")
        time.sleep(0.1)
        dev.write(b"\xA0\x01\x00\xA1")

# Function to turn the lamp off
def turn_lamp_off(device):
    # Switch the relay on and off once to turn the lamp off
    with open(device, "w") as dev:
        dev.write(b"\xA0\x01\x01\xA2")
        time.sleep(0.1)
        dev.write(b"\xA0\x01\x00\xA1")
        time.sleep(0.1)
        dev.write(b"\xA0\x01\x01\xA2")
        time.sleep(0.1)
        dev.write(b"\xA0\x01\x00\xA1")

# Function to check internet connectivity
def check_internet():
    try:
        subprocess.check_call(["ping", "-c", "1", "-W", "0.1", "8.8.8.8"])
        return True
    except subprocess.CalledProcessError:
        return False

# Find the USB device path dynamically
def find_usb_device_path():
    usb_ports = list(serial.tools.list_ports.comports())
    for port, desc, hwid in usb_ports:
        if "usbserial" in hwid.lower():
            return port
    return None

# Initial state: Lamp is off
lamp_state = "off"

# Continuous monitoring loop
while True:
    # Find the USB device path
    usb_device = find_usb_device_path()
    if usb_device:
        # Check internet connectivity
        if check_internet():
            # If internet is available and lamp is off, turn it on
            if lamp_state == "off":
                turn_lamp_on(usb_device)
                lamp_state = "on"
        else:
            # If ping times out and lamp is on, turn it off
            if lamp_state == "on":
                turn_lamp_off(usb_device)
                lamp_state = "off"
    else:
        print("USB device not found. Please connect the device.")
        time.sleep(1)  # Wait for 1 second before checking again
