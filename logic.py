import math
from matplotlib import pyplot as plt
import cv2
import imutils
import numpy as np

from Point import Point
from Color import Color


WIDTH_A4 = 210
HEIGHT_A4 = 297

decrease = 0.6

def load_and_resize(path, decrease):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    image = cv2.resize(image, None, fx=decrease, fy=decrease)
    return image

def get_extreme_points(cnts):
    c = cnts
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    return extLeft, extRight, extTop, extBot

def get_distance_two_outside_points(one: Point, two: Point, mode="horizontal"):
    return abs(one()[1] - two()[1]) if mode == "vertical" else abs(one()[0] - two()[0])


def get_distance(a: Point, b: Point):
    return math.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)


def draw_line(image, a: Point, b: Point):
    cv2.line(image, a(), b(), Color().get(), thickness=1, lineType=8)

def add_all_contours_together(_contours):
    all = _contours[0]
    for x in range(1, len(_contours)):
        all = np.append(all, _contours[x], axis=0)
    return all

def right_or_left(foot_center, big_toe):
    if foot_center[0] > big_toe[0]:
        return "RIGHT"
    else:
        return "LEFT"


def do_magic_bro(part):
    ret, thresh_part = cv2.threshold(part, 245, 255, 0)
    thresh_part = cv2.bitwise_not(thresh_part)
    contours_part, hierarchy = cv2.findContours(thresh_part, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_part = [x for x in contours_part if len(x) > 10]
    return add_all_contours_together(contours_part)

def move(FOOT, point: Point, move: int):
    x = FOOT.left()[0]+point()[0]
    y = point()[1]+FOOT.top()[1] + move
    return Point((x, y))

def get_triangle_height(a: Point, b: Point, top: Point):
    a_b = get_distance(a, b)
    a_top = get_distance(a, top)
    b_top = get_distance(b, top)
    p = (a_b + a_top + b_top)/2
    area = math.sqrt(p*(p-a_b)*(p-a_top)*(p-b_top))
    return 2*area/a_b 

def sztriter_godunov(a: Point, b: Point, top_1: Point, top_2: Point):
    height_1 = get_triangle_height(a, b, top_1)
    height_2 = get_triangle_height(a, b, top_2)
    return (height_2-height_1)/height_2



def angle_between_points(p0: Point, p1: Point, p2: Point):
    a = (p1.x-p0.x)**2 + (p1.y-p0.y)**2
    b = (p1.x-p2.x)**2 + (p1.y-p2.y)**2
    c = (p2.x-p0.x)**2 + (p2.y-p0.y)**2
    return 180 - math.acos((a+b-c) / math.sqrt(4*a*b)) * 180/math.pi

def angle_from_sin(p0: Point, p1: Point):
    c = get_distance(p0, p1)
    b = get_distance_two_outside_points(p0, p1)
    return math.degrees(math.sin(b/c))