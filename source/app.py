"""
A web app interface for dynamic, live facial image insertion.

@author: Elias Gabriel, Duncan Mazza
@revision: v1.0
"""
from flask import render_template, Response
from api.web_classes import WebApplication

# Import archived code for testing
from api import __past__
from apix.cam_classes import CamReader


def index():
    """ Renders the index HTML page. """
    # TODO: Create basic UI
    return render_template('index.html')


def eye():
    """ Returns a mixed multipart HTTP response containing streamed MJPEG data, pulled from
    the OpenCV image processor. """
    # Create and return a mutlipart HTTP response, with the separate parts defined by '--frame'
    return Response(feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


def feed():
    """ Opens a camera reader, gets a processed frame, encodes it to JPEG, and returns it as a
    snippet of a multipart response body. """
    # Creates a new camera reader
    camera = CamReader()

    # TODO: Implement ARCUO engine

    # In a loop, get the current frame of the camera as a byte sequence and yield it to the calling process.
    # This lets us send a HTTP response back to the client, but keeps it open to allow for continious
    # updates. In effect, this streams image data from the server to the client's computer through a
    # Motion JPEG.
    # Wrap the encoded frame in a multipart image section, to be inserted into the multipart HTTP response
    while True: yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + camera.get_frame() + b'\r\n')


# Only start the server if the script is run directly
if __name__ == "__main__":
    # Create a new web application
    app = WebApplication("cropmeon")
    # Define the application routes
    app.route({ '/': index, '/eye': eye })
    # Beginning listening on `localhost`, port 3000
    app.listen(port=8080, env="development")
