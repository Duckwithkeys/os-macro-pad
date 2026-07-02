# OS-Switching NeoKey Macro Pad

A hardware-assisted dual-boot coordination system using an Adafruit NeoKey 1x4 (powered by a QT Py) to coordinate OS switching and control between Windows and Linux.

## Project Structure

```
os-macro-pad/
├── firmware/
│   └── code.py                  # CircuitPython firmware for QT Py + NeoKey 1x4
├── host_linux/
│   └── macropad_listener.py     # Background listener service for Linux
├── host_windows/
│   ├── macropad_listener.py     # Background listener service for Windows
│   └── launch_macropad.vbs      # VBS launcher to run the Windows listener silently
├── requirements.txt             # Python dependencies for host machines
└── README.md                    # Project documentation
```

---

## Hardware Configuration

- **Controller**: Adafruit QT Py (RP2040, SAMD21, etc. running CircuitPython 8+)
- **Keypad**: Adafruit NeoKey 1x4 (I2C address `0x30`)
- **Wiring**: Connected via I2C (SDA/SCL on Board pins A2/A3)

---

## Macro Pad Layout & Functions

The 4 keys are configured with specific colors and commands:

| Key | Color | LED Color (RGB) | Function / Command |
| :--- | :--- | :--- | :--- |
| **Key 0** | Red | `(120, 0, 0)` | **Alt + F4** (Close active window) |
| **Key 1** | Blue | `(0, 0, 40)` | **CMD:WIN** (Reboots host machine into Windows) |
| **Key 2** | Green | `(0, 40, 0)` | **CMD:LINUX** (Reboots host machine into Linux) |
| **Key 3** | White | `(30, 30, 30)` | **CMD:REBOOT** (Triggers a standard system restart) |

---

## Installation & Setup

### 1. Firmware Installation (Macro Pad)
1. Install **CircuitPython** on your QT Py board.
2. Copy the files/libraries from the Adafruit CircuitPython Bundle to your board's `lib/` directory:
   - `adafruit_neokey`
   - `adafruit_hid`
   - `adafruit_pixelbuf`
   - `neopixel.mpy`
3. Copy [firmware/code.py](file:///Users/oliver/Documents/Projects/Macro%20Pad/os-macro-pad/firmware/code.py) to the root of the board's storage as `code.py`.

### 2. Host Prerequisites (Linux & Windows)
Make sure Python 3 is installed on both machines, then install dependencies:
```bash
pip install -r requirements.txt
```

---

## Running the Host Services

### Linux Service Setup
The Linux host script listens for `CMD:WIN` and runs `/usr/bin/boot-windows` (which should set your EFI bootnext to Windows and trigger a reboot) or `CMD:REBOOT` to restart.

Run it manually or set it up as a systemd service:
```bash
python host_linux/macropad_listener.py
```

### Windows Service Setup
The Windows host script listens for `CMD:LINUX` or `CMD:REBOOT` to reboot the machine back into Linux or reboot immediately.

To run the listener in the background without showing a command window:
1. Move `macropad_listener.py` to your user folder (e.g., `C:\Users\Oliver\macropad_listener.py` as configured in the VBS script).
2. Double-click [host_windows/launch_macropad.vbs](file:///Users/oliver/Documents/Projects/Macro%20Pad/os-macro-pad/host_windows/launch_macropad.vbs) to start the daemon in the background.
