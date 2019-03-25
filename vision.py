"""
A web app interface for dynamic, live facial image insertion.

@author: Elias Gabriel, Duncan Mazza
@revision: v1.0
"""
from flask import Flask, render_template, Response
import blob_test

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eye')
def eye():
    return Response(feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def feed():
    camera = Camera()

    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
