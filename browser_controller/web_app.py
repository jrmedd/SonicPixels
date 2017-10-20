from flask import Flask, flash, url_for, render_template, request, redirect, make_response, Response, jsonify
from flask_socketio import SocketIO
from OSC import OSCClient, OSCMessage

app = Flask(__name__)

app.secret_key = "secret"

socketio = SocketIO(app)


#my_ip = "127.0.0.1"
my_ip = "10.99.100.120"

client = OSCClient()
client.connect((my_ip, 8000))

@app.route('/')
def index():
    return render_template('index.html',ip=my_ip)

@socketio.on('grid_message')
def handle_grid_message(grid_message):
    column = grid_message.get('data').get('column')
    row = grid_message.get('data').get('row')
    state = int(grid_message.get('data').get('state'))
    grid_number = grid_message.get('grid')
    send_osc_message("/%s"%(grid_number), [column, row, state])

@socketio.on('control_message')
def handle_control_message(control_message):
    parameter = control_message.get('data').get('parameter')
    state = control_message.get('data').get('state')
    send_osc_message("/%s"%(parameter), [state])

def send_osc_message(address, message):
    oscmsg = OSCMessage()
    oscmsg.setAddress(address)
    oscmsg.append(message)
    try:
        client.send(oscmsg)
    except:
        print "Error sending messsage, reciever may not be available"

if __name__ == '__main__':
    socketio.run(app, host=my_ip, debug=True)
