import microbit
import radio

message_types = {"00":'play_c', "01": 'vol_c'} #incoming hex messages are prepended by message types

radio.config(power=7) #radio full power

radio.on() #radio on

def send_message(message):
    radio.send(message) #send the message straight onto cells
    microbit.display.clear() #clear the display
    processed_message = process_message(message) #process the message
    if processed_message.get('msg_type') == 'play_c':
        pressed_col = processed_message.get('col')
        for row in processed_message.get('rows'):
            for idx, bit in enumerate(row):
                if bit == 1:
                    pressed_row = idx
                    microbit.display.set_pixel(pressed_col, pressed_row, 9)

def to_bits(hex_input):
    converted = int(hex_input, 16) #convert hex to int
    bits = [int(i) for i in '{0:05b}'.format(converted)] #convert int to list of bits
    return bits

def hex_rows(hexstring):
    return [hexstring[i:i+2] for i in range(0,len(hexstring), 2)]

def process_message(message):
    message_type = message_types.get(message[0:2])
    if message_type == 'play_c':
        message_pieces = (int(message[2:4]), message[4:22], int(message[22:24]))
        rows = [to_bits(row) for row in hex_rows(message_pieces[1])]
        return {'msg_type':message_type,'col':message_pieces[0],"rows":rows, 'bank':message_pieces[2]}
    elif message_type == 'vol_c':
        return {'msg_type':message_type, "row":int(message[2]),'col':int(message[3]), 'volume':int(message[5:7],16)}
