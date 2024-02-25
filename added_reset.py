import os
import time
import subprocess
import re

def get_usb_info(vendor_id, product_id):
    output = subprocess.check_output(["lsusb"]).decode("utf-8")
    pattern = r"Bus (\d+) Device (\d+): ID {0}:{1}".format(vendor_id, product_id)
    match = re.search(pattern, output)

    if match:
        bus = match.group(1)
        device = match.group(2)
        port = "0"  # Assuming it's connected directly to the root hub
        return bus, device, port
    else:
        print("USB device with Vendor ID {} and Product ID {} not found.".format(vendor_id, product_id))
        return None, None, None

def unbind_usb(bus, device, port):
    path = "/sys/bus/usb/drivers/usb/{0}-{1}:{2}/unbind".format(bus, device, port)
    with open(path, "w") as f:
        f.write("{0}-{1}:{2}".format(bus, device, port))

def bind_usb(bus, device, port):
    path = "/sys/bus/usb/drivers/usb/{0}-{1}:{2}/bind".format(bus, device, port)
    with open(path, "w") as f:
        f.write("{0}-{1}:{2}".format(bus, device, port))

def find_device_path():
    for device in os.listdir("/sys/class/tty"):
        device_path = os.path.join("/sys/class/tty", device, "device")
        if os.path.islink(device_path):
            symlink_target = os.readlink(device_path)
            device_name = os.path.basename(symlink_target)
            device_path = f"/dev/{device_name}"
            if os.path.exists(device_path):
                return device_path
    return None

DEVICE = None

def turn_lamp_on():
    if DEVICE:
        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x01\xA2")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")
            time.sleep(0.1)

        with open(DEVICE, 'wb') as f:
            f.write(b"\xA0\x01\x00\xA1")
        with open(DEVICE, 'wb') as f:
            f.write(b"\x0D\x0A")

def turn_lamp_off():
    if DEVICE:
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

def check_internet():
    try:
        subprocess.run(["ping", "-c", "1", "-W", "0.1", "8.8.8.8"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    vendor_id = "1d6b"
    product_id = "0003"

    bus, device, port = get_usb_info(vendor_id, product_id)
    if bus and device and port:
        unbind_usb(bus, device, port)
        time.sleep(1)  # Add a delay to ensure unbinding completes before rebinding
        bind_usb(bus, device, port)

    global DEVICE
    DEVICE = find_device_path()

    lamp_state = "off"

    while True:
        if not DEVICE:
            DEVICE = find_device_path()

        if check_internet():
            if lamp_state == "off":
                turn_lamp_on()
                lamp_state = "on"
        else:
            if lamp_state == "on":
                turn_lamp_off()
                lamp_state = "off"

        time.sleep(0.1)

if __name__ == "__main__":
    main()
