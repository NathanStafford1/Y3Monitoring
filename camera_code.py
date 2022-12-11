from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
global grey
grey = 0
# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

# instatiate flask app
app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)
def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:
            if (grey):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass
@app.route('/')
def index():
    return render_template('working_cam.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=False)

camera.release()
cv2.destroyAllWindows()
