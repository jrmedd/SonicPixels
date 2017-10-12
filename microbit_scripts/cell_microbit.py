import microbit
import radio

this_device = {'row':0 , 'column':0} #row and column

message_types = {"00":"playback", "01": "volume_change"}

radio.on()

#recommended to write pin16 low (this is the busy pin indicator)
microbit.pin16.read_digital()

microbit.uart.init(baudrate=9600, bits=8, parity=None, stop=1, tx=microbit.pin14, rx=microbit.pin15)

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
    microbit.uart.write(CommandLine)

#folders named "##", e.g. "00" to "99" with tracks named "###.mp3", e.g. "000.mp3" to "255.mp3"
def play_track(folder, track):
    stop_track()
    command(0x0F,int(folder),int(track))

#stops any track playing
def stop_track():
    command(0x16,0,0)

#volume should be int between 0 (silent) and 48 (loud)
def set_volume(volume):
    command(0x06,0,int(volume))

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
        message_pieces = (int(message[2:4]), message[4:22], int(message[22:24]))
        rows = [to_bits(row) for row in hex_rows(message_pieces[1])]
        return {"message_type":message_type,"column":message_pieces[0],"rows":rows, "sound_bank":message_pieces[2]}
    elif message_type == "volume_change":
        return {"message_type":message_type, "row":int(message[2]),"column":int(message[3]), "volume":int(message[5:7],16)}

while True:
    if microbit.button_a.is_pressed():
        microbit.display.set_pixel(this_device.get('column'), this_device.get('row'), 9)
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
                            microbit.display.show("P "+str(processed_message.get('sound_bank'))+str(row))
                            play_track(processed_message.get('sound_bank'), row)
                elif processed_message.get('message_type') == "volume_change":
                    microbit.display.show("V "+ str(processed_message.get('volume')))
                    set_volume(int((processed_message.get('volume')/255.)*48))
