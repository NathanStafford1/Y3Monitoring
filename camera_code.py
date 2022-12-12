import RPi.GPIO as GPIO
import time, threading
from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from threading import Thread

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-6ed21369-a5b3-4a8b-b9a6-3a225ce51275'
pnconfig.publish_key = 'pub-c-0abc1efe-4b78-4cdc-a195-fc1ebc33eaac'
pnconfig.user_id = "david"
pubnub = PubNub(pnconfig)

my_channel = 'davidmccabe'
sensors_list=["camera"]
data={}

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
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(my_channel).message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)
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


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='5000', debug=False)
if __name__ == '__main__':
    sensors_thread = threading.Thread(target=video_feed)
    sensors_thread.start()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()
camera.release()
cv2.destroyAllWindows()





# PIR_pin = 23
# Buzzer_pin = 24
#
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
#
# GPIO.setup(PIR_pin, GPIO.IN)
# GPIO.setup(Buzzer_pin, GPIO.OUT)
#
# def beep(repeat):
#     for i in range(0, repeat):
#         for pulse in range(60):
#             GPIO.output(Buzzer_pin, True)
#             time.sleep(0.001)
#             GPIO.output(Buzzer_pin, False)
#             time.sleep(0.001)
#         time.sleep(0.02)
#
#
# def motion_detection():
#     while(True):
#         if GPIO.input(PIR_pin):
#             print("Motion detected")
#             beep(4)
#         time.sleep(1)
#
# if __name__ == '__main__':
#     sensors_thread = threading.Thread(target=motion_detection)
#     sensors_thread.start()
#     pubnub.add_listener(MySubscribeCallback())
#     pubnub.subscribe().channels(my_channel).execute()