# This work is licensed under a Creative Commons Attribution 4.0 International License. http://creativecommons.org/licenses/by/4.0/

import os
import time
import subprocess

# Function to find the device path dynamically
def find_device_path():
    # Iterate through the devices under /sys/class/tty
    for device in os.listdir("/sys/class/tty"):
        # Check if the device directory contains a symlink named "device"
        device_path = os.path.join("/sys/class/tty", device, "device")
        if os.path.islink(device_path):
            # If symlink exists, get the symlink target
            symlink_target = os.readlink(device_path)
            # Extract the device name from the symlink target
            device_name = os.path.basename(symlink_target)
            # Construct the device path
            device_path = f"/dev/{device_name}"
            # Check if the device path is valid
            if os.path.exists(device_path):
                return device_path
    # If no valid device path is found, return None
    return None

# Define the initial device path as None
DEVICE = None

# Function to turn the lamp on
def turn_lamp_on():
    if DEVICE:
        # Switch the relay on and off twice to turn the lamp on
        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x01\xA2")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")
            time.sleep(0.1)

        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x00\xA1")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")

# Function to turn the lamp off
def turn_lamp_off():
    if DEVICE:
        # Switch the relay on and off once to turn the lamp off
        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x01\xA2")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")
            time.sleep(0.1)

        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x00\xA1")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")
            time.sleep(0.1)

        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x01\xA2")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")
            time.sleep(0.1)

        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x00\xA1")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")

# Function to check internet connectivity
def check_internet():
    try:
        # Use ping to check internet connectivity
        subprocess.run(["ping", "-c", "1", "-W", "0.1", "8.8.8.8"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Initial state: Lamp is off
lamp_state = "off"

# Continuous monitoring loop
while True:
    # Find the device path if not already found
    if not DEVICE:
        DEVICE = find_device_path()
        print(DEVICE)
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
