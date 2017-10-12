import microbit
import radio

radio.on()

def send_message(message):
    radio.send(message)

row_count = 4
column_count = 0
message_structure = "00%s%s000000000000000000"

while True:
    if microbit.button_b.was_pressed():
        microbit.display.clear()
        message_to_send = message_structure % ( "%02x" % (column_count), "%02x"% (1* 2 **row_count))
        microbit.display.set_pixel(column_count, abs(row_count-4), 9)
        send_message(message_to_send)
        column_count = (column_count+1)%5
        if column_count == 0:
            row_count = (row_count-1)%5
