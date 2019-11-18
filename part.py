import imutils
import numpy as np
import cv2 as cv
import math


def set_outside_points(cnts) -> dict:
    return {
        "top": tuple(cnts[cnts[:, :, 1].argmin()][0]),
        "left": tuple(cnts[cnts[:, :, 0].argmin()][0]),
        "right": tuple(cnts[cnts[:, :, 0].argmax()][0]),
        "bottom": tuple(cnts[cnts[:, :, 1].argmax()][0])
    }


def get_distance_two_outside_points(point1, point2, ratio, mode="horizontal"):
    ratio = ratio * 10 # mm to cm
    if mode == "vertical":
        return round(abs(point1[1] - point2[1]) / ratio, 2)
    elif mode == "horizontal":
        return round(abs(point1[0] - point2[0])/ratio, 2)
    else:
        raise Exception


class Part:
    def __init__(self, cnts, name):
        self.name = name
        self.contours = cnts
        self._center = self.set_area_center(self.contours)
        self.area = cv.contourArea(self.contours)
        self.outside_points = set_outside_points(self.contours)

    def __repr__(self):
        return "Part{}, center: {}, area: {}".format(str(self.name), self.center, self.area)

    @property
    def center(self) -> tuple:
        return self._center

    @center.setter
    def center(self, cnts):
        self._center = self.set_area_center(cnts)

    @staticmethod
    def set_area_center(cnts) -> tuple:
        moments = cv.moments(cnts)
        try:
            c_x = int(moments["m10"] / moments["m00"])
            c_y = int(moments["m01"] / moments["m00"])
        except ZeroDivisionError:
            c_x = (0, 0)
            c_y = (0, 0)
        return c_x, c_y
