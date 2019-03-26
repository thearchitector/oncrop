"""
A web app interface for dynamic, live facial image insertion.

@author: Elias Gabriel, Duncan Mazza
@revision: v1.0
"""
from flask import render_template, Response
from api.web_classes import WebApplication
from api.cam_classes import CamReader


def index():
    """ Renders the index HTML page. """
    return render_template('index.html')


def eye():
    """ Returns a mixed multipart HTTP response containing streamed MJPEG data, pulled from
    the OpenCV image processor. """
    return Response(feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


def feed():
    """ Opens a camera reader, gets a processed frame, encodes it to JPEG, and returns it as a
    snippet of a multipart response body. """
    camera = CamReader()
    
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == "__main__":
    # Create a new web application
    app = WebApplication()

    # Define the application routes
    app.routes({
        '/': index,
        '/eye': eye
    })

    # Beginning listening on `localhost`, port 3000
    app.listen(port=3000)
