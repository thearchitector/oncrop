"""
Detects AR markers within a single frame, and replaces them with given faces.

@author: Elias Gabriel and Duncan Mazza
@revision: v1.0
"""
import cv2
import numpy as np
import math

SCL = 2


class MyDeque:
    """
    This is a custom deque that is like a python deque but specifically for the purpose of averaging the face bounding
    box variables over the latest five frames (to reduce the *jiggly* nature of the bounding box.
    """

    def __init__(self, smooth_level=5):
        """
        Initializes the deque with 5 empty *bounding boxes*
        :param smooth_level: The number of bounding box information tuples that will be averaged; the higher this
        number, the greater the smoothing of the bounding box, but the more it will lag behind the face.
        """
        self.smooth_level = smooth_level
        self.rect_list = []
        for i in range(smooth_level):
            self.rect_list.append(((0, 0), (0, 0)))
        self.latest_rect = ((0, 0), (0, 0))

    def add(self, rect):
        """
        This method takes in the latest bounding box and returns the average of it and the previous 4 bounding boxes.
        :param rect: a tuple of coordinates, where each coordinate is a tuple
        :return x, y, w, h: the new parameters for a bounding box
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
        return self.latest_rect


lower_dict = {0: (0, 0, 240), 1: (0, 240, 0), 2: (240, 0, 0)}
upper_dict = {0: (230, 230, 255), 1: (230, 255, 230), 2: (255, 230, 230)}
colors_dict = {2: (255, 0, 0), 1: (0, 255, 0), 0: (0, 0, 255)}
deque_dict = {0: MyDeque(10), 1: MyDeque(10), 2: MyDeque(10)}


def parse_markers(frame, keypoints, i):
    coords = []
    # parse marker into coordinates
    for marker in keypoints:
        coords.append(tuple(int(i) for i in marker.pt))
    # reject the coordinates if there is anything other than a pair; increase the timer

    if len(coords) != 2:
        rect = deque_dict[i].get_rect()
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
        rect = deque_dict[i].add(((int(center[0] - SCL * dist_btw / 3), int(center[1] - SCL * dist_btw / 2)),
                                  (int(center[0] + SCL * dist_btw / 3), int(center[1] + SCL * dist_btw / 2))))
        # draw square:
        cv2.rectangle(frame, rect[0], rect[1], colors_dict[i], -1)
        return None


def look_for_markers(cap, num_people):
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 5

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.4

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.7

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.5

    t = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        blur = cv2.GaussianBlur(frame, (11, 11), 0)

        for i in range(3):
            mask = cv2.inRange(blur, lower_dict[i], upper_dict[i])
            mask = cv2.erode(mask, None, iterations=2)
            mask = 255 - mask

            d = cv2.SimpleBlobDetector_create(params)
            keypoints = d.detect(mask)
            # for marker in keypoints:
            #     print(tuple(int(i) for i in marker.pt))
            #     frame = cv2.drawMarker(frame, tuple(int(i) for i in marker.pt), (255, 255, 255))

            parse_markers(frame, keypoints, i)

        # frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    look_for_markers(cap, num_people=3)
