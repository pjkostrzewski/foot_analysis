# from corners import *
# from variables import *
# from random import randint
# from matplotlib import pyplot as plt
# import os
# from pprint import pprint


# def get_center_of_contours(cnts):
#     M = cv2.moments(cnts)
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
#     return cX, cY


# def get_extreme_points(cnts):
#     c = cnts
#     extLeft = tuple(c[c[:, :, 0].argmin()][0])
#     extRight = tuple(c[c[:, :, 0].argmax()][0])
#     extTop = tuple(c[c[:, :, 1].argmin()][0])
#     extBot = tuple(c[c[:, :, 1].argmax()][0])
#     return extLeft, extRight, extTop, extBot


# def get_distance_two_outside_points(one, two, mode="horizontal"):
#     return abs(one[1] - two[1]) if mode == "vertical" else abs(one[0] - two[0])


# def add_all_contours_together(_contours):
#     all = _contours[0]
#     for x in range(1, len(_contours)):
#         all = np.append(all, _contours[x], axis=0)
#     return all


# def right_or_left(foot_center, big_toe):
#     if foot_center[0] > big_toe[0]:
#         return "RIGHT"
#     else:
#         return "LEFT"


# def do_magic_bro(part):
#     ret, thresh_part = cv2.threshold(part, 245, 255, 0)
#     thresh_part = cv2.bitwise_not(thresh_part)
#     contours_part, hierarchy = cv2.findContours(thresh_part, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours_part = [x for x in contours_part if len(x) > 10]
#     return add_all_contours_together(contours_part)


# def draw_circles(*args):
#     for draw in args:
#         cv2.circle(image, draw, 8, (0, 0, 255), -1)

# path = "C:\\Users\\pkostrze\\Desktop\\odbitki stop"
# files = [x for x in os.listdir(path) if x.endswith(".png") and "Scan" in x]
# sizes = {}
# for file in files:
#     image = load_and_resize("{}\\{}".format(path, file), decrease)
#     image_black = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#     img = cv2.GaussianBlur(image_black, (7, 7), 3)
#     img = cv2.medianBlur(img, 7)
#     ret, thresh = cv2.threshold(img, 245, 255, 0)
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = [x for x in contours if cv2.contourArea(x) > 100]
#     sizes.update({file: len(contours)})
# pprint(sizes)
# # image = load_and_resize(path, decrease)
# # image_black = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)