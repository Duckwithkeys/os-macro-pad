import os 
import time 
import threading 
import serial 
import serial.tools.list_ports

VENDOR_ID = 0x239A 
PRODUCT_ID = 0x80F8

def find_data_port(): 
    ports = serial.tools.list_ports.comports() 
    target_ports = [p.device for p in ports if p.vid == VENDOR_ID and p.pid == PRODUCT_ID] 
    if target_ports: 
        target_ports.sort() 
        return target_ports[1] if len(target_ports) >= 2 else target_ports[0] 
    return None

def heartbeat_sender(ser): 
    while ser.is_open: 
        try: 
            ser.write(b"HELLO:LINUX\n") 
            ser.flush() 
            time.sleep(1.5) 
        except Exception: 
            break

def main(): 
    print("Searching for QT Py Macro Pad...") 
    while True: 
        port = find_data_port() 
        if not port: 
            time.sleep(2) 
            continue

        print(f"Target found! Connecting to data stream on: {port}")
        try:
            with serial.Serial(port, 115200, timeout=0.1) as ser:
                ser.dtr = True
                time.sleep(0.1)
                
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
                                    os.system("/usr/bin/boot-windows")
                                elif line == "CMD:LINUX":
                                    print("Already running Linux!")
                                elif line == "CMD:REBOOT":
                                    os.system("reboot")
                            buffer = ""
                        else:
                            buffer += char
        except (serial.SerialException, OSError) as e:
            print(f"Connection dropped ({e}). Re-scanning in 2 seconds...")
            time.sleep(2)

if __name__ == "__main__": 
    main()
