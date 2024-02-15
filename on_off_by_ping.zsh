#!/bin/zsh
#zsh script made for mac
#will work on Linux

# Define the device path
DEVICE="/dev/cu.usbserial-1240" # Modify this to fit your machine and your device path

# Function to turn the lamp on
turn_lamp_on() {
    # Switch the relay on and off twice to turn the lamp on
    echo -e "\xA0\x01\x01\xA2" > "$DEVICE"
    sleep 0.1
    echo -e "\xA0\x01\x00\xA1" > "$DEVICE"
}

# Function to turn the lamp off
turn_lamp_off() {
    # Switch the relay on and off once to turn the lamp off
    echo -e "\xA0\x01\x01\xA2" > "$DEVICE"
    sleep 0.1
    echo -e "\xA0\x01\x00\xA1" > "$DEVICE"
    sleep 0.1
    echo -e "\xA0\x01\x01\xA2" > "$DEVICE"
    sleep 0.1
    echo -e "\xA0\x01\x00\xA1" > "$DEVICE"

}

# Function to check internet connectivity
check_internet() {
#    echo "Checking internet connectivity..."
    ping -c 1 -W 0.1 8.8.8.8 > /dev/null 2>&1
#    ping -c 1 8.8.8.8 > /dev/null 2>&1
}

# Initial state: Lamp is off
lamp_state="off"

# Continuous monitoring loop
while true; do
    # Check internet connectivity
    if check_internet; then
        # If internet is available and lamp is off, turn it on
        if [ "$lamp_state" = "off" ]; then
            turn_lamp_on
            lamp_state="on"
        fi
    else
        # If ping times out and lamp is on, turn it off
        if [ "$lamp_state" = "on" ]; then
            turn_lamp_off
            lamp_state="off"
        fi
    fi
    # Wait for 0.1 second before next iteration
    sleep 0.1
done
