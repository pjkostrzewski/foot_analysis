from part import *
from singleton_decorator import singleton


class Paint:
    def __init__(self, image):
        self.image = image
        self.gray = None
        self.median = None
        self.edged = None
        self.paint_gray()
        self.paint_median()
        self.paint_edged()

    def paint_gray(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (9, 9), 7)
        self.gray = gray

    def paint_median(self):
        self.median = cv.medianBlur(self.gray, 9)

    def paint_edged(self):
        edged = cv.Canny(self.median, 50, 50)
        edged = cv.dilate(edged, None, iterations=3)
        edged = cv.erode(edged, None, iterations=1)
        self.edged = edged

    def get_edged(self):
        return self.edged

    def draw_point(self, cnts, color: tuple):
        cv.circle(self.image, cnts, 11, color, -1)

    def draw_line(self, point1, point2, color: tuple):
        cv.line(self.image, point1, point2, color, thickness=1, lineType=8)
