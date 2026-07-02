import os 
import time 
import threading 
import serial 
import serial.tools.list_ports

VENDOR_ID = 0x239A 
PRODUCT_ID = 0x80F8

def find_data_port(): 
    ports = serial.tools.list_ports.comports() 
    for p in ports: 
        if p.vid == VENDOR_ID and p.pid == PRODUCT_ID: 
            return p.device 
    return None

def heartbeat_sender(ser): 
    while ser.is_open: 
        try: 
            ser.write(b"HELLO:WINDOWS\n") 
            time.sleep(2) 
        except Exception: 
            break

def main(): 
    print("Searching for QT Py Macro Pad on Windows...") 
    while True: 
        port = find_data_port() 
        if not port: 
            time.sleep(2) 
            continue

        print(f"Target found! Connecting to data stream on: {port}")
        try:
            with serial.Serial(port, 115200, timeout=0.1) as ser:
                print("Successfully Connected!")
                
                t = threading.Thread(target=heartbeat_sender, args=(ser,), daemon=True)
                t.start()

                print("--- RAW DATA STREAM ACTIVE ---")
                buffer = ""
                while True:
                    char_byte = ser.read(1)
                    if char_byte:
                        char = char_byte.decode('utf-8', errors='ignore')
                        if char in ('\n', '\r'):
                            line = buffer.strip()
                            if line:
                                print(f"Processed Command: {line}")
                                
                                if line == "CMD:WIN":
                                    print("Already running Windows!")
                                elif line == "CMD:LINUX":
                                    print("Rebooting back to Linux...")
                                    os.system("shutdown /r /t 0")
                                elif line == "CMD:REBOOT":
                                    print("Triggering system restart...")
                                    os.system("shutdown /r /t 0")
                            buffer = ""
                        else:
                            buffer += char
        except (serial.SerialException, PermissionError) as e:
            print(f"Connection dropped ({e}). Re-scanning in 2 seconds...")
            time.sleep(2)

if __name__ == "__main__": 
    main()
