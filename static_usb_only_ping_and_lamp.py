import subprocess
import time

# Define the device path
DEVICE = "/dev/ttyUSB0"  # Modify this to fit your machine and your device path

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
