from microbit import *
import neopixel

uart.init(baudrate=9600, bits=8, parity=None, stop=1, tx=pin14, rx=pin15)

np = neopixel.NeoPixel(pin13, 2)

Start_Byte = 0x7E
Version_Byte = 0xFF
CMD_Length = 0x06
Acknowledge = 0x00
End_Byte = 0xEF
HighByte = 0x00
LowByte = 0x00


def split(num):
    return num >> 8, num & 0xFF


def command(CMD, Par1, Par2):
    Checksum = -(Version_Byte + CMD_Length + CMD + Acknowledge + Par1 + Par2)
    HighByte, LowByte = split(Checksum)
    CommandLine = bytes([b & 0xFF for b in [
        Start_Byte, Version_Byte, CMD_Length, CMD, Acknowledge,
        Par1, Par2, HighByte, LowByte, End_Byte
    ]])
    uart.write(CommandLine)


while True:
    if button_a.is_pressed():
        display.show(Image.SQUARE)
        # Start_Byte, Version_Byte, CMD_Length, CMD, Acknowledge,Par1, Par2, HighByte, LowByte, End_Byte
        # uart.write(bytes([0x7E, 0xFF, 0x06, 0x01, 0x00, 0x00, 0x00, 0xFE, 0xFA, 0xEF]))
        command(0x01, 0x00, 0x00)
        # uart.write(bytes([Start_Byte, Version_Byte, CMD_Length, 0x01, Acknowledge, 0x00, 0x00, HighByte, LowByte, End_Byte]))
        for pixel_id in range(0, len(np)):
            np[pixel_id] = (255, 0, 0)
            np.show()
    elif button_b.is_pressed():
        display.show(Image.DIAMOND)
        command(0x16, 0x00, 0x00)
        # uart.write(bytes([Start_Byte, Version_Byte, CMD_Length, 0x16, Acknowledge, 0x00, 0x00, HighByte, LowByte, End_Byte]))
        for pixel_id in range(0, len(np)):
            np[pixel_id] = (0, 0, 255)
            np.show()
    else:
        display.clear()
        for pixel_id in range(0, len(np)):
            np[pixel_id] = (0, 0, 0)
            np.show()
