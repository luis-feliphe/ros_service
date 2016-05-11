# main.py

from flask import Flask, render_template, Response, redirect
from camera import VideoCamera

app = Flask(__name__)

############################
############################
import freenect 
import cv2
import numpy as np
import Image
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    ret, jpeg = cv2.imencode('.jpeg', array)
    return jpeg.tostring()
############################




@app.route('/')
def index():
#    return render_template('map.html')
    return render_template('index.html')


@app.route('/<path:path>')
def catch_all(path):
    if (path=="map.html"):
        return render_template('map.html') 
    elif(path=="monitor.html"):
        return render_template('monitor.html') 
    else:
        return 'You want path: %s' % path



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
#    app.run(host='10.13.100.1', port=8080, debug=True)
#    app.run(host='192.168.1.111', port=8080, debug=True)
#    app.run(host='25.70.63.170', port=8080, debug=True)
#    app.run(host='150.165.205.53', port=8080, debug=True)

