# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2 as cv
import pprint


def get_center_of_toe(toe):
    moments = cv.moments(toe)
    c_x = int(moments["m10"] / moments["m00"])
    c_y = int(moments["m01"] / moments["m00"])
    return c_x, c_y


def right_or_left(big_toe_center, small_toe_center):
    return "RIGHT" if big_toe_center[0] < small_toe_center[0] else "LEFT"


def get_distance_two_outside_points(one, two, mode="horizontal"):
    return abs(one[1] - two[1]) if mode == "vertical" else abs(one[0] - two[0])




# load the image, convert it to grayscale, and blur it slightly
image = cv.imread('src/two.png')
H_IMG = np.size(image, 0)
H_A4 = 297
W_IMG = np.size(image, 1)
W_A4 = 210
ratio = round(H_IMG/H_A4, 4)
print(str(ratio) + " pixels = 1mm.")
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (9, 9), 7)
median = cv.medianBlur(gray, 9)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv.Canny(median, 50, 50)
edged = cv.dilate(edged, None, iterations=3)
edged = cv.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print("PARTS DETECTED: " + str(len(cnts)))
#
foot_parts = sorted(cnts, key=cv.contourArea, reverse=True)
shank, big_toe, small_toe = foot_parts[0], foot_parts[1], foot_parts[-1]
cv.drawContours(image, shank, -1, (255, 0, 0), 3)
cv.drawContours(image, big_toe, -1, (0, 255, 0), 3)
cv.drawContours(image, small_toe, -1, (0, 0, 255), 3)
toes_centers = {
    "big_toe": get_center_of_toe(big_toe),
    "small_toe": get_center_of_toe(small_toe),
    "shank": get_center_of_toe(shank)
}
### OUTSIDE POINTS
c = cnts[0]
for x in range(1, len(cnts)):
    c = np.append(c, cnts[x], axis=0)
top = tuple(c[c[:, :, 1].argmin()][0])
c = sorted(cnts, key=cv.contourArea, reverse=True)[0]
left = tuple(c[c[:, :, 0].argmin()][0])
right = tuple(c[c[:, :, 0].argmax()][0])
bottom = tuple(c[c[:, :, 1].argmax()][0])

### GET FOOT HEIGHT
foot_length = get_distance_two_outside_points(top, bottom, "vertical")/ratio/10
foot_width = get_distance_two_outside_points(left, right, "horizontal")/ratio/10
print("length: {}cm".format(round(foot_length, 2)))
print("width: {}cm".format(round(foot_width, 2)))


### RESULTS
print(right_or_left(toes_centers["big_toe"], toes_centers["small_toe"]))
print("length/width ratio (Wejsflog ratio): {}, expected 3.0".format(round(foot_length/foot_width, 2)))
### DRAWING
cv.circle(image, toes_centers["big_toe"], 11, (255, 255, 0), -1)
cv.circle(image, toes_centers["small_toe"], 11, (255, 255, 0), -1)
cv.circle(image, toes_centers["shank"], 11, (69, 21, 127), -1)

cv.circle(image, left, 8, (0, 50, 255), -1)
cv.circle(image, right, 8, (0, 255, 255), -1)
cv.circle(image, top, 8, (255, 50, 0), -1)
cv.circle(image, bottom, 8, (255, 255, 0), -1)
cv.line(image, top, bottom, (0, 255, 0), thickness=3, lineType=8)
cv.line(image, left, right, (0, 255, 0), thickness=3, lineType=8)
cv.imshow("image", image)
cv.imwrite("src/one_result.png", img=image)
# cv.imshow("edged", edged)
# cv.imshow("gray", gray)
cv.waitKey(0)
cv.destroyAllWindows()

