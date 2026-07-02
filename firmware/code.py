import time, board, bitbangio, usb_cdc, gc, usb_hid
from adafruit_neokey.neokey1x4 import NeoKey1x4
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
gc.collect()
i2c = bitbangio.I2C(board.A3, board.A2)
neokey = NeoKey1x4(i2c, addr=0x30)
kbd = Keyboard(usb_hid.devices)
C_OFF = (0, 0, 0)
LAYOUT = [(120, 0, 0), (0, 0, 40), (0, 40, 0), (30, 30, 30)]
CMDS = [None, "CMD:WIN", "CMD:LINUX", "CMD:REBOOT"]
prev = [False] * 4
last_p = [0] * 4
f_until = [0] * 4
ser = usb_cdc.data if usb_cdc.data else usb_cdc.console
def send(c):
    if ser and c:
        try: ser.write((c + "\n").encode("utf-8"))
        except: pass
while True:
    now = time.monotonic_ns() // 1_000_000
    for i in range(4):
        p = neokey[i]
        if p and not prev[i] and (now - last_p[i]) > 150:
            last_p[i] = now
            f_until[i] = now + 150
            neokey.pixels[i] = C_OFF
            if i == 0: kbd.send(Keycode.ALT, Keycode.F4)
            else: send(CMDS[i])
            neokey.pixels.show()
            time.sleep(0.15)
        if f_until[i]:
            if now >= f_until[i]:
                f_until[i] = 0
                neokey.pixels[i] = LAYOUT[i]
            else: neokey.pixels[i] = C_OFF
        else: neokey.pixels[i] = LAYOUT[i]
        prev[i] = p
    neokey.pixels.show()
    time.sleep(0.01)
