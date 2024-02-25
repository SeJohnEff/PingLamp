# This code is licensed under the Creative Commons CC0 1.0 Universal License.

import subprocess
import time

# Function to find the device path
def find_device_path():
    # Run the lsusb command to list connected USB devices
    lsusb_info = subprocess.check_output(["lsusb"]).decode("utf-8")
    # Check if our USB device is present
    if "1a86:7523" in lsusb_info:
        # Run the command to find the device path
        usb_device_info = subprocess.check_output(["udevadm", "info", "--query=path", "--name=/dev/ttyUSB0"]).decode("utf-8")
        # Extract the device path
        for line in usb_device_info.split('\n'):
            if "E: DEVNAME" in line:
                return line.split('=')[1]
    else:
        # If not found, return None
        return None

# Function to reset the USB device
def reset_device(device_path):
    # Run the usbreset command to reset the USB device
    subprocess.run(["usbreset", device_path], shell=True)

# Function to check if the USB device is busy
def is_device_busy(device_path):
    # Try to open the device in write mode
    try:
        with open(device_path, 'wb'):
            return False
    except IOError:
        return True

# Define the device path
DEVICE = find_device_path()

# Function to turn the lamp on
def turn_lamp_on():
    # Switch the relay on and off twice to turn the lamp on
    with open(DEVICE, 'wb') as f:
        f.write(b"\xA0\x01\x01\xA2\r\n")
        time.sleep(0.1)
        f.write(b"\xA0\x01\x00\xA1\r\n")

# Function to turn the lamp off
def turn_lamp_off():
    # Switch the relay on and off once to turn the lamp off
    with open(DEVICE, 'wb') as f:
        f.write(b"\xA0\x01\x01\xA2\r\n")
        time.sleep(0.1)
        f.write(b"\xA0\x01\x00\xA1\r\n")
        time.sleep(0.1)
        f.write(b"\xA0\x01\x01\xA2\r\n")
        time.sleep(0.1)
        f.write(b"\xA0\x01\x00\xA1\r\n")

# Function to check internet connectivity
def check_internet():
    try:
        subprocess.run(["ping", "-c", "1", "-W", "0.1", "8.8.8.8"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Initial state: Lamp is off
lamp_state = "off"

# Continuous monitoring loop
while True:
    # Check if the device path is None
    if DEVICE is None:
        # If so, try finding the device path again
        DEVICE = find_device_path()
    else:
        # Check if the device is busy
        if is_device_busy(DEVICE):
            # If busy, reset the device
            reset_device(DEVICE)
        else:
            # Check internet connectivity
            if check_internet():
                # If internet is available and lamp is off, turn it on
                if lamp_state == "off":
                    turn_lamp_on()
                    lamp_state = "on"
            else:
                # If internet is not available and lamp is on, turn it off
                if lamp_state == "on":
                    turn_lamp_off()
                    lamp_state = "off"
    # Wait for 0.1 second before next iteration
    time.sleep(0.1)
