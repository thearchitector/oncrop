"""
Contains all the classes used for computer vision and backend processing.

@author: Duncan Mazza, Elias Gabriel
@revision: v1.1
"""
import cv2
import cv2.aruco as aruco
import os

FACE_SCL = 4  # coefficient to scale the size of the face relative to the width of the aruco code


class ByteCapture:
    """
    Serves as a wrapper for a given byte sequence. This class forms a bridge between raw data and
    an abstracted processing engine.
    """

    def write(self, byte_seq):
        """ Stores the given byte sequence within an instance attribute. Returns the instance for
        easy instantiation. """
        self.bytes = byte_seq
        return self

    def read(self):
        """ Returns the stored byte sequence. """
        return None, self.bytes


class ProcessingEngine:
    """
    The main backend class for image per-processing, appending given images to tracked positional
    ARCUO markers in a media feed.
    """

    def __init__(self, source="webcam", filename=None):
        # load the face image
        face = cv2.imread("{}".format(filename), -1)
        if face is not None:
            self.face = face
            print(face.shape)
            self.face_size_y, self.face_size_x, _ = face.shape
            self.file_type = filename[len(filename) - 3:len(filename)]
        else:  # image doesn't exist
            self.file_type = False

        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        # Create aruco markers if necessary
        if os.path.exists("markers/"):
            print("Markers already exist!")
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
        if source == "local":
            self.cap = cv2.VideoCapture(0)
        elif source == "file":
            # Read the image data
            imdata = cv2.imread(filename)
            # Verify that it exists
            if imdata.size == 0: raise ("Source expected as a file, but no valid filename was given!")
            # Create a ByteCapture object and write the image data
            self.cap = ByteCapture().write(imdata)
        elif source == "remote":
            self.cap = ByteCapture()
        # Throw an error if something isn't write
        else:
            raise ("Unknown source type! Must be `local`, `file`, or `remote`.")

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
        if len(corners) == 1:  # there must be only one aruco code at this point
            ####################################################################
            x_plus = y_plus = 0  # for calculating the center of the aruco code
            x_h_list = []  # for calculating the width of the aruco code
            for corner in corners[0][0]:
                x_h_list.append(int(corner[0]))
                x_plus += corner[0]
                y_plus += corner[1]
            x = int(x_plus / 4)  # x coordinate of aruco code center
            y = int(y_plus / 4)  # y coordinate of aruco code center
            min_x = min(x_h_list)
            max_x = max(x_h_list)
            w = max_x - min_x  # width of the aruco code

            # change x and y to be offsets instead of the center
            face = cv2.resize(self.face, (FACE_SCL * w, int(FACE_SCL * w * (self.face_size_y / self.face_size_x))))

            # log the dimensions of the resized face image
            face_x = face.shape[1]
            face_y = face.shape[0]

            # Calculate the parameters for cropping the face on top of the frame

            # find the bounds of the region of interest rectangle (roi)
            delta_x = int(face_x / 2)
            delta_y = int(face_y / 2)
            x1 = x - delta_x
            y1 = y - delta_y
            x2 = x1 + face_x
            y2 = y1 + face_y

            print(x1, y1, x2, y2)
            # handle clipping
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

            # if the face is too big:
            if x2 - x1 >= frame_x or y2 - y1 >= frame_y:
                cv2.putText(frame, "You are too close to the frame", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (255, 255, 255), 2)
                return frame

            # pull out the region of interest:
            roi = frame[y1:y2, x1:x2]

            if self.file_type == "png":
                mask = face[:, :, 3]
                mask_inv = cv2.bitwise_not(mask)
                frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
                face_fg = cv2.bitwise_and(face, face, mask=mask)
                dst = cv2.add(frame_bg, face_fg[:, :, :3])
                frame[y1:y2, x1:x2] = dst
            elif self.file_type == "jpg":
                frame[y1:y2, x1:x2] = face
            else:
                return frame

            # Encode the final frame as a JPEG and return its byte sequence
            # return cv2.imencode('.jpg', frame)[1].tobytes()

            return frame
        else:
            # Encode the final frame as a JPEG and return its byte sequence
            # return cv2.imencode('.jpg', frame)[1].tobytes()

            return frame


# Artifact of incremental testing
if __name__ == "__main__":
    engine = ProcessingEngine(source="local", filename="tux-r.jpg")

    while True:
        cv2.imshow('res', engine.get_frame())
        if cv2.waitKey(1) & 0xFF == ord('q'): break
