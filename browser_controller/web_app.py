from flask import Flask, flash, url_for, render_template, request, redirect, make_response, Response, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from OSC import OSCClient, OSCMessage

app = Flask(__name__)

app.secret_key = "secret"

socketio = SocketIO(app)


my_ip = "127.0.0.1"
client = OSCClient()
client.connect((my_ip, 8000))

@app.route('/')
def index():
    return render_template('index.html',ip=my_ip)

@socketio.on('grid_message')
def handle_message(grid_message):
    column = grid_message.get('data').get('column')
    row = grid_message.get('data').get('row')
    state = int(grid_message.get('data').get('state'))
    grid_number = grid_message.get('grid')
    oscmsg = OSCMessage()
    oscmsg.setAddress("/%s" % (grid_number))
    oscmsg.append([column, row, state])
    client.send(oscmsg)


if __name__ == '__main__':
    socketio.run(app, host=my_ip, debug=True)
