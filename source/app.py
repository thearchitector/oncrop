"""
A web app interface for dynamic, live facial image insertion.

@author: Elias Gabriel
@revision: v1.3
"""
from flask import render_template, Response, request, session, redirect, jsonify
from api.web_classes import WebApplication
from api.cv_classes import ProcessingEngine
import tempfile
from random import randint
import os


app = WebApplication("cropmeon")


@app.route('/', methods=['GET'])
def index(error=False):
	""" Renders the index HTML page. """
	# Render the index page, showing the error message if something went wrong
	return render_template('index.html', visibility=("visible" if error else "hidden"))


@app.errorhandler(404)
def unknown_page(error):
	""" Defines the response when a 404 HTTP status code is thrown. """
	return index(error=True), 404


@app.route('/upload', methods=['POST'])
def upload():
	""" Handles image file uploads to the server. """
	images = request.files.getlist('images[]') if 'images[]' in request.files else None
	if not images: return index(error=True)

	# Save the uploaded images temporarily server-side, to be used when the  ProcessingEngine
	# is constructed later
	session['images'] = []

	# Generate temporary files to store the uploaded images
	for f in images:
		# Create a temp file
		_, tpath = tempfile.mkstemp()
		# Save the file and path
		session['images'].append(tpath)
		f.save(tpath)

	# Mark the session as modified, as sessioned mutable objects can be buggy
	session.modified = True

	# Return a JSON object indicating a successful request
	return jsonify(number_uploads=len(images), status="success")


@app.route('/marker', methods=['GET'])
def marker():
	""" Renders a random pre-generated AURCO marker. """
	if not ('images' in session): return index()

	# Render the marker template and randomly select a marker file, set to randmarker variable
	return render_template('marker.html', randmarker="markers/marker_" + str(randint(0, 9)) + ".jpg")


@app.route('/capture', methods=['GET'])
def capture():
	""" Renders the camera viewpoint. """
	if not ('images' in session): return index(error=True)

	return render_template('capture.html')


@app.route('/eye', methods=['GET'])
def eye():
	""" Returns a mixed multipart HTTP response containing streamed MJPEG data, pulled from
	the OpenCV image processor. """
	# Create a processing engine and register the uploaded face
	engine = ProcessingEngine(source="local")
	engine.set_face(session['images'][0])
	# Clear and delete the cached session images
	for fpath in session['images']: os.remove(fpath)
	session.clear()

	# Create and return a mutlipart HTTP response, with the separate parts defined by '--frame'
	try: return Response(feed(engine), mimetype='multipart/x-mixed-replace; boundary=frame')
	except: return index(error=True)


def feed(engine):
	""" Opens a camera reader, gets a processed frame, encodes it to JPEG, and returns it as a
	snippet of a multipart response body. """

	# In a loop, get the current frame of the camera as a byte sequence and yield it to the calling process.
	# This lets us send a HTTP response back to the client, but keeps it open to allow for continious
	# updates. In effect, this streams image data from the server to the client's computer through a
	# Motion JPEG.
	# Wrap the encoded frame in a multipart image section, to be inserted into the multipart HTTP response
	while True: yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + engine.get_frame() + b'\r\n')


@app.route('/snapshot', methods=['POST'])
def snapshot():
	""" Passes the exported image data to `show`. """
	URI = request.form.get('URI', None)
	if not URI: return index()
	session['uri'] = URI

	return jsonify(status="success")


@app.route('/show', methods=['GET'])
def show():
	""" Displays the captured photo, and prompts the user to either take another photo or start again. """
	if not ('uri' in session): return index(error=True)
	uri = session['uri']
	session.clear()

	return render_template('show.html', captured_img=uri)


if __name__ == "__main__":
	app.listen(port=8080, env="development")
