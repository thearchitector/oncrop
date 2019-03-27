"""
Contains all the classes used for computer vision and backend processing.

@author: Duncan Mazza, Elias Gabriel
@revision: v1.1
"""
import cv2
import cv2.aruco as aruco
import os



class ByteCapture:
    """
    Serves as a wrapper for a given byte sequence. This class forms a bridge between raw data and
    an abstracted processing engine.
    """


    def write(byte_seq):
        """ Stores the given byte sequence within an instance attribute. Returns the instance for
        easy instantiation. """
        self.bytes = byte_seq
        return self


    def read():
        """ Returns the stored byte sequence. """
        return None, self.bytes



class ProcessingEngine:
    """
    The main backend class for image per-processing, appending given images to tracked positional
    ARCUO markers in a media feed.
    """


    def __init__(self, source="webcam", filename=None):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

        # Create aruco markers if necessary
        if os.path.exists("markers/"): print("Markers already exist!")
        else:
            print("Generating markers...")
            os.system("mkdir markers")

            # Create 10 unique markers
            for marker_num in range(10):   
                img = aruco.drawMarker(self.aruco_dict, marker_num, 700)
                cv2.imwrite("markers/marker_{}.jpg".format(str(marker_num)), img)

        # Create detection parameters
        self.parameters = aruco.DetectorParameters_create()

        # Set up OpenCV. If the source is local, open a webcam feed. If the source is a file, read the file,
        # verify that it is a valid image, and write it to a byte feed. If it is a remote source, create
        # an empty byte feed.
        if source == "local": self.cap = cv2.VideoCapture(0)
        elif source == "file":
            # Read the image data
            imdata = cv2.imread(filename)
            # Verify that it exists
            if imdata.size == 0: raise("Source expected as a file, but no valid filename was given!")
            # Create a ByteCapture object and write the image data
            self.cap = ByteCapture().write(imdata)
        elif source == "remote": self.cap = ByteCapture()
        # Throw an error if something isn't write
        else: raise("Unknown source type! Must be `local`, `file`, or `remote`.")


    def get_frame(self):
        """ Reads a frame from the given capture device, identifies the markers and inserts the desired
        faces. The processed frame is encoded as a JPEG and returned as a byte sequence. """
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, _, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        frame = aruco.drawDetectedMarkers(frame, corners)

        # TODO: add capability for corner information to inform the placement of an image on top of the frame
       
        # Encode the final frame as a JPEG and return its byte sequence
        return cv2.imencode('.jpg', frame)[1].tobytes()


# Artifact of incremental testing
if __name__ == "__main__":
    engine = ProcessingEngine(source="local")

    while True:
        cv2.imshow('image', engine.get_frame())
        if cv2.waitKey(1) & 0xFF == ord('q'): break
