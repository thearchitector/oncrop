"""
A web app interface for dynamic, live facial image insertion.

@author: Elias Gabriel, Duncan Mazza
@revision: v1.0
"""
from flask import render_template, Response
from api.web_classes import WebApplication
# from api.computer_vision_classes import CamReader
from api import __past__


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
    camera = archive.CamReader()
    
    while True:
        frame = camera.get_frame()
        
        # TODO: Parse numpy array into a JPEG image bytestream
        
        yield('--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + '\r\n')


if __name__ == "__main__":
    # Create a new web application
    app = WebApplication("cropmeon")

    # Define the application routes
    app.route({
        '/': index,
        '/eye': eye
    })

    # Beginning listening on `localhost`, port 3000
    app.listen(port=3000)
