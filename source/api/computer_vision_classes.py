import cv2
import cv2.aruco as aruco
import os


class ParseImage:
    def __init__(self, source="webcam"):
        # Create aruco markers if necessary
        if os.path.exists("markers/"):
            "Markers already exist in markers/"
        else:
            "Generating markers; creating and adding to folder markers/"
            os.system("mkdir markers")
            for marker_num in range(10):
                # create 10 unique markers
                aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
                img = aruco.drawMarker(aruco_dict, marker_num, 700)
                cv2.imwrite("markers/marker_{}.jpg".format(str(marker_num)), img)

        # Set up the aruco detection
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters_create()

        # Set up OpenCV
        if source == "webcam":
            self.cap = cv2.VideoCapture(0)
        elif source == "Img":
            pass
            # TODO
            # Add functionality for reading from an image instead of the webcam

    def get_frame(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        gray = aruco.drawDetectedMarkers(gray, corners)
        frame = aruco.drawDetectedMarkers(frame, corners)
        # TODO: add capability for corner information to inform the placement of an image on top of the frame
        return frame, gray


if __name__ == "__main__":
    image_parser = ParseImage()
    while True:
        frame, gray = image_parser.get_frame()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
