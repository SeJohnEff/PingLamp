# This code is licensed under the Creative Commons CC0 1.0 Universal License.

import subprocess
import time

# Function to find the device path
def find_device_path():
    # Run the usb-devices command to get information about USB devices
    usb_info = subprocess.check_output(["usb-devices"]).decode("utf-8")
    # Split the output by lines
    lines = usb_info.split('\n')
    # Initialize variables to store Vendor and Product IDs
    vendor_id = None
    product_id = None
    # Loop through each line
    for line in lines:
        # Check if the line contains Vendor and Product IDs
        if "Vendor=" in line and "ProdID=" in line:
            # Extract Vendor and Product IDs
            vendor_id = line.split("Vendor=")[1].split()[0]
            product_id = line.split("ProdID=")[1].split()[0]
            # Check if the Vendor and Product IDs match the expected values
            if vendor_id == "1a86" and product_id == "7523":
                # If match found, extract the device path
                for line in lines:
                    if "T:" in line and "Dev#=" in line:
                        return line.split(" ")[1]

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
