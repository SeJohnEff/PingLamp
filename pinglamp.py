import subprocess
import time
import ping3
import serial.tools.list_ports

# Define the device path
DEVICE = "/dev/cu.usbserial-1240"

# Function to turn the lamp on
def turn_lamp_on():
    # Switch the relay on and off twice to turn the lamp on
    with open(DEVICE, "w") as dev:
        dev.write(b"\xA0\x01\x01\xA2")
        time.sleep(0.1)
        dev.write(b"\xA0\x01\x00\xA1")

# Function to turn the lamp off
def turn_lamp_off():
    # Switch the relay on and off once to turn the lamp off
    with open(DEVICE, "w") as dev:
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
        # If ping times out and lamp is on, turn it off
        if lamp_state == "on":
            turn_lamp_off()
            lamp_state = "off"
    # Wait for 0.1 second before next iteration
    time.sleep(0.1)
