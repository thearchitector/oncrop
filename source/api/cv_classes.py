"""
Contains all the classes used for computer vision and backend processing.

@author: Duncan Mazza, Elias Gabriel
@revision: v1.1
"""
import cv2
import cv2.aruco as aruco
import os
import numpy as np


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

        face = cv2.imread("{}".format(filename), -1)
        if face is not None:
            self.face = face
            print(face.shape)
            self.face_size_y, self.face_size_x, _ = face.shape

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
        # height, width = frame.size
        frame_x = frame.shape[1]
        frame_y = frame.shape[0]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, _, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)



        # Find the x, y, w, and h of the aruco code (approx. since considering rotation and skew are not important)
        if len(corners) != 0:
            ####################################################################
            x_plus = y_plus = 0
            x_h_list = []
            y_h_list = []
            for corner in corners[0][0]:
                x_h_list.append(int(corner[0]))
                x_plus += corner[0]
                y_h_list.append(int(corner[1]))
                y_plus += corner[1]
            x = int(x_plus / 4)  # center x
            y = int(y_plus / 4)  # center y
            min_x = min(x_h_list)
            max_x = max(x_h_list)
            min_y = min(y_h_list)
            max_y = max(y_h_list)
            h = max_y - min_y
            w = max_x - min_x
            # change x and y to be offsets instead of the center
            face = cv2.resize(self.face, (3 * w, int(3 * w * (self.face_size_y / self.face_size_x))))
            face_x = face.shape[1]
            face_y = face.shape[0]
            delta_x = int(face_x / 2)
            delta_y = int(face_y / 2)
            x1 = x - delta_x
            y1 = y - delta_y
            x2 = x1 + face_x
            y2 = y1 + face_y

            if x1 < 0:
                x1 = 0
                x2 = face_x
            if y1 < 0:
                y1 = 0
                y2 = face_y
            if x2 > frame_x:
                x2 = frame_x
                x1 = frame_x - face_x
            if y2 > frame_y:
                y2 = frame_y
                y1 = frame_y - face_y

            roi = frame[y1:y2, x1:x2]

            mask = face[:,:,3]
            mask_inv = cv2.bitwise_not(mask)
            frame_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
            face_fg = cv2.bitwise_and(face, face, mask = mask)
            dst = cv2.add(frame_bg, face_fg[:,:,:3])
            frame[y1:y2, x1:x2] = dst

            # Encode the final frame as a JPEG and return its byte sequence
            # return cv2.imencode('.jpg', frame)[1].tobytes()
            return frame
        else:
            # Encode the final frame as a JPEG and return its byte sequence
            # return cv2.imencode('.jpg', frame)[1].tobytes()
            return frame


# Artifact of incremental testing
if __name__ == "__main__":
    engine = ProcessingEngine(source="local", filename = "will_smith.png")

    while True:
        cv2.imshow('res', engine.get_frame())
        if cv2.waitKey(1) & 0xFF == ord('q'): break
