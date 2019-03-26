"""
This is a custom deque-like class that enhances the stability of the positioning of
the rectangles for the trackers.

@author: Duncan Mazza
@revision: v1.0
"""

import cv2
import math

# Parameters for 
lower_dict = {0: (0, 0, 240), 1: (0, 240, 0), 2: (240, 0, 0)}
upper_dict = {0: (230, 230, 255), 1: (230, 255, 230), 2: (255, 230, 230)}
colors_dict = {2: (255, 0, 0), 1: (0, 255, 0), 0: (0, 0, 255)}
SCL = 2

class SmoothRect:
    def __init__(self, smooth_level=5):
        """ Initializes the deque with smooth_level empty rectangles.

        :param smooth_level: The number of rectangle information tuples that will be averaged. The
                             higher this number the greater the smoothing of the rectangle, but
                             the more it will lag behind the face.
        """
        self.smooth_level = smooth_level
        self.rect_list = []
        self.latest_rect = ((0, 0), (0, 0))

        for i in range(smooth_level): self.rect_list.append(((0, 0), (0, 0)))

    def add(self, rect):
        """ This method takes in the latest rectangle and returns the average of it and the
        previous 4 rectangles.

        :param rect: a tuple of coordinates, where each coordinate is a tuple
        :return latest_rect: the average rectangle of all rectangles in rect_list
        """
        self.rect_list.pop(0)
        self.rect_list.append(rect)

        x1 = y1 = x2 = y2 = 0
        for i in range(self.smooth_level):
            x1 += self.rect_list[i][0][0]
            y1 += self.rect_list[i][0][1]
            x2 += self.rect_list[i][1][0]
            y2 += self.rect_list[i][1][1]

        self.latest_rect = ((int(x1 / self.smooth_level), int(y1 / self.smooth_level)),
                            (int(x2 / self.smooth_level), int(y2 / self.smooth_level)))
        return self.latest_rect

    def get_rect(self):
        """ Returns the average rectangle of all rectangles in rect_list. """
        return self.latest_rect


class CamReader:
    def __init__(self, filterByArea=True, minArea=5, filterByCircularity=True, minCircularity=0.4,
                 filterByConvexity=True, minConvexity=0.7, filterByInertia=False, minInertiaRatio=0.5):
        self.cap = cv2.VideoCapture(0)

        ###########################
        # Set up the blob detector:
        params = cv2.SimpleBlobDetector_Params()

        # Filter by Area
        self.filterByArea = filterByArea
        params.filterByArea = self.filterByArea
        self.minArea = minArea
        params.minArea = self.minArea

        # Filter by Circularity
        self.filterByCircularity = filterByCircularity
        params.filterByCircularity = self.filterByCircularity
        self.minCircularity = minCircularity
        params.minCircularity = self.minCircularity

        # Filter by Convexity
        self.filterByConvexity = filterByConvexity
        params.filterByConvexity = self.filterByConvexity
        self.minConvexity = minConvexity
        params.minConvexity = self.minConvexity

        # Filter by Inertia
        self.filterByInertia = filterByInertia
        params.filterByInertia = self.filterByInertia
        self.minInertiaRatio = minInertiaRatio
        params.minInertiaRatio = self.minInertiaRatio

        self.blob_detector = cv2.SimpleBlobDetector_create(params)

        self.deque_dict = {0: SmoothRect(10), 1: SmoothRect(10), 2: SmoothRect(10)}

    def parse_markers(self, frame, keypoints, i):
        """
        Interpret and display (using rectangles) the information from the blob detection's outputs.
        :param frame: frame on which the rectangles will be drawn
        :param keypoints: the output from the blob detection
        :param i: the color of marker that is being looked for
        :return None:
        """
        coords = []
        # parse marker into coordinates
        for marker in keypoints:
            coords.append(tuple(int(i) for i in marker.pt))
        # reject the coordinates if there is anything other than a pair; increase the timer

        if len(coords) != 2:
            rect = self.deque_dict[i].get_rect()
            cv2.rectangle(frame, rect[0], rect[1], colors_dict[i], -1)
            return None
        else:
            # put bottommost coord in first spot, topmost coord in the second spot
            coords.sort(key=lambda x: x[1])
            dist_btw = math.sqrt((coords[0][0] - coords[1][0]) ** 2 + (coords[0][1] - coords[1][1]) ** 2)
            # find the center between the coordinates; head vector is the lower coord
            direc_vec = (int(((coords[0][0] - coords[1][0]) * (dist_btw / 2)) / dist_btw),
                         int(((coords[0][1] - coords[1][1]) * (dist_btw / 2)) / dist_btw))
            center = [sum(x) for x in zip(direc_vec, coords[1])]
            # calculate square params:
            rect = self.deque_dict[i].add(((int(center[0] - SCL * dist_btw / 3), int(center[1] - SCL * dist_btw / 2)),
                                      (int(center[0] + SCL * dist_btw / 3), int(center[1] + SCL * dist_btw / 2))))
            # draw square:
            cv2.rectangle(frame, rect[0], rect[1], colors_dict[i], -1)
            return None

    def get_frame(self):
        """
        Looks for markers and overlays them with rectangles.
        :return frame: a OpenCV-readable numpy array of the frame to display
        """
        # Capture frame-by-frame
        ret, frame = self.cap.read()
        blur = cv2.GaussianBlur(frame, (11, 11), 0)

        for i in range(3):
            mask = cv2.inRange(blur, lower_dict[i], upper_dict[i])
            mask = cv2.erode(mask, None, iterations=2)
            mask = 255 - mask

            keypoints = self.blob_detector.detect(mask)
            # for marker in keypoints:
            #     print(tuple(int(i) for i in marker.pt))
            #     frame = cv2.drawMarker(frame, tuple(int(i) for i in marker.pt), (255, 255, 255))

            self.parse_markers(frame, keypoints, i)

        # frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        return frame
