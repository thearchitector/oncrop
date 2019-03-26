"""
A web app interface for dynamic, live facial image insertion.

@author: Elias Gabriel
@revision: v1.0
"""
from flask import render_template, Response

class WebApp():
    """ A class object for instantiating and launching a web server. """


    def __init__(self, app_name=__name__, debug=False):
        self.app = Flask(__name__)
        self.app.debug = debug

    def listen(ip=):
    

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
