# main.py

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
#    return render_template('index.html')
    return render_template('index.html', commands= AVAILABLE_COMMANDS)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/foo', methods=['GET', 'POST'])
def foo(x=None, y=None):
    # do something to send email
    print " OBAAAAAAAAA  \n\n\n "
#    return redirect ('http://25.70.63.170:8080/', code=302)
    return "oi"

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='25.70.63.170', port=8080, debug=True)




@app.route('/cmd')
def command(cmd=None):
    print "\n\n\n-----------------------\n" + str (cmd) + "\n\n\n---------------------------\n"
    if cmd == RESET:
       camera_command = "X"
       response = "Resetting ..."
    else:
        camera_command = cmd[0].upper()
        response = "Moving {}".format(cmd.capitalize())

    # ser.write(camera_command)
    return response, 200, {'Content-Type': 'text/plain'}
