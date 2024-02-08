import time
import ping3
import serial.tools.list_ports

# Configure the target IP address
target_ip = "8.8.8.8"

# Function to detect active USB serial port
def detect_active_port():
    active_port = None
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description:
            active_port = port.device
            break
    return active_port

# Function to send data via USB serial communication
def send_data_via_serial(data, port):
    try:
        ser = serial.Serial(port, 9600, timeout=1)  # Adjust baud rate and timeout as needed
        ser.write(data.encode())
        ser.close()
    except Exception as e:
        print(f"Error occurred while sending data via serial port: {str(e)}")

def main():
    active_port = detect_active_port()
    if active_port:
        while True:
            try:
                # Perform ping
                result = ping3.ping(target_ip, timeout=1)

                # Handle ping result
                if result is not None:
                    print("Ping successful. Relay on.")
                    send_data_via_serial("relay on", active_port)
                else:
                    print("Ping timeout. Relay off.")
                    send_data_via_serial("relay off", active_port)

                # Wait for 1 second before the next ping
                time.sleep(1)
            except KeyboardInterrupt:
                print("Exiting program.")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    else:
        print("No active USB serial port found.")

if __name__ == "__main__":
    main()
