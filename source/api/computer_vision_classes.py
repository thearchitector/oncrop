import cv2
import cv2.aruco as aruco
import os


class ParseImage:
    def __init__(self):
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

        # Set up the aruco-specific code
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters_create()
        
    def


if __name__ == "__main__":
    write_aruco_code()
