import microbit
import radio

this_device = {'row':0 , 'column':0} #row and column

message_types = {"00":"playback", "01": "volume_change"}

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

def process_message(message):
    message_type = message_types.get(message[0:2])
    if message_type == "playback":
        message_pieces = (int(message[2:4]), message[4:22])
        rows = [to_bits(row) for row in hex_rows(message_pieces[1])]
        return {"message_type":message_type,"column":message_pieces[0],"rows":rows}
    elif message_type == "volume_change":
        return {"message_type":message_type, "row":int(message[2]),"column":int(message[3]), "volume":int(message[5:7],16)}

while True:
    if microbit.button_a.is_pressed():
        microbit.display.set_pixel(this_device.get('row'), this_device.get('column'), 9)
    else:
        microbit.display.show(" ")
    incoming_message = radio.receive()
    if incoming_message:
        processed_message = process_message(incoming_message)
        if processed_message:
            if processed_message.get('column') == this_device.get('column'):
                if processed_message.get('message_type') == "playback":
                    for row in range(len(processed_message.get('rows'))):
                        if processed_message.get('rows')[row][this_device.get('row')]:
                            microbit.display.show("P "+str(row))
                elif processed_message.get('message_type') == "volume_change":
                    microbit.display.show("V "+ str(processed_message.get('volume')))
