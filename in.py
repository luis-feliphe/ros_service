from flask import Flask, render_template, Response, redirect
from camera import VideoCamera

app = Flask(__name__)



LEFT, RIGHT, UP, DOWN, RESET = "left", "right", "up", "down", "reset"
AVAILABLE_COMMANDS = {
	'Left': LEFT,
	'Right': RIGHT,
	'Up': UP,
	'Down': DOWN,
	'Reset': RESET
}

@app.route('/')
def index():
	return render_template('index2.html', commands=AVAILABLE_COMMANDS)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/<cmd>')
def command(cmd=None):
	print "\n\n comand: " + str (cmd) + "\n\n\n"
	if cmd == RESET:
		camera_command = "X"
		response = "Resetting ..."
	elif cmd== "Left":
		print "\n\n\nLeft comand received\n\n\n"
	#    else:
	#        camera_command = cmd[0].upper()
	response = "Moving {}".format(cmd.capitalize())

	# ser.write(camera_command)
	return "", 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
	app.run(host="25.70.63.170", port=8080, debug=True)
