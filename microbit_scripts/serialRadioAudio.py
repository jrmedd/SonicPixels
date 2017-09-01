import microbit
import radio

this_device = (0, 0) #row and column
device_state = 0 #lit or not
state_display = [" ", "#"] #what to display for being lit or not

radio.on()

def to_bits(hex_input):
    converted = int(hex_input, 16)
    bits = [int(i) for i in '{0:05b}'.format(converted)]
    return bits

def hex_rows(hexstring):
    return [hexstring[i:i+2] for i in range(0,len(hexstring), 2)]

def parse_grid(hex_received):
    row_values = [to_bits(hex_row) for hex_row in hex_rows(hex_received)]
    return row_values

while True:
    if microbit.button_a.is_pressed():
        microbit.display.set_pixel(this_device[1], this_device[0], 9)
    else:
        microbit.display.show(state_display[device_state])
    hex_radio = radio.receive()
    if hex_radio:
        device_state = parse_grid(hex_radio)[this_device[0]][this_device[1]]
