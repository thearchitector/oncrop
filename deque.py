"""
This is a custom deque-like class that enhances the stability of the positioning of
the rectangles for the trackers.

@author: Duncan Mazza
@revision: v1.0
"""
class MyDeque:
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
        
        self.latest_rect = ((int(x1 / self.smooth_level), int(y1 / self.smooth_level)), (int(x2 / self.smooth_level), int(y2 / self.smooth_level)))
        return self.latest_rect


    def get_rect(self):
        """ Returns the average rectangle of all rectangles in rect_list. """
        return self.latest_rect
