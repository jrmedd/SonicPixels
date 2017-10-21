import microbit
import radio

radio.config(power=7)

radio.on()


def send_message(message):
    radio.send(message)
