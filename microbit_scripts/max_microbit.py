import microbit
import radio

radio.on()

def send_message(message):
    radio.send(message)
