import microbit
import radio

radio.on()

def to_bits(hex_input):
    converted = int(hex_input, 16)
    bits = [int(i) for i in '{0:05b}'.format(converted)]
    return bits

def hex_rows(hexstring):
    return [hexstring[i:i+2] for i in range(0,len(hexstring), 2)]

def show_grid(hex_received):
    radio.send(hex_received)
    row_values = [to_bits(hex_row) for hex_row in hex_rows(hex_received)]
    for row in range(len(row_values)):
        for column in range(len(row_values[row])):
            microbit.display.set_pixel(column, row, row_values[row][column]*9)
