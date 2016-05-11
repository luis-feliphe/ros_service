# -*- coding: utf-8 -*-


from flask import Flask, render_template, Response, redirect

import socket
import sys

HOST, PORT = "localhost", 9999



LEFT, RIGHT, UP, DOWN, RESET = "left", "right", "up", "down", "reset"
AVAILABLE_COMMANDS = {
	'Left': LEFT,
	'Right': RIGHT,
	'Up': UP,
	'Down': DOWN,
	'Reset': RESET
}

			
			

app = Flask(__name__)



@app.route('/')
def index():
	return render_template('control.html', commands=AVAILABLE_COMMANDS)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/<cmd>')
def command(cmd=None):
	if cmd == RESET:
		camera_command = "X"
		response = "Resetting ..."
	else:
		print str (cmd)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((HOST, PORT))
			sock.sendall(cmd + "\n")
			received = sock.recv(1024)
		finally:
			sock.close()

	response = "Moving {}".format(cmd.capitalize())
	return "", 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
	app.run(host="localhost", port=8000, debug=True)
#	app.run(host="10.13.100.1", port=8000, debug=True)
#	app.run(host="25.70.63.170", port=8000, debug=True)
#	app.run(host="192.168.1.111", port=8000, debug=True)
#	app.run(host="150.165.205.53", port=8000, debug=True)


