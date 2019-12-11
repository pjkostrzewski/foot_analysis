from corners import *
from variables import *
from random import randint
from matplotlib import pyplot as plt


def get_center_of_contours(cnts):
    M = cv2.moments(cnts)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return cX, cY


def get_extreme_points(cnts):
    c = cnts
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    return extLeft, extRight, extTop, extBot

path = "/home/spodek/Pulpit/odbitki stop/Scan14.png"
image = load_and_resize(path, decrease)
image_black = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

img = cv2.GaussianBlur(image_black, (7, 7), 3)
img = cv2.medianBlur(img, 7)

ret, thresh = cv2.threshold(img, 245, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours[1:], key=len)
for c in [x for x in contours if cv2.contourArea(x) > 300]:
    cv2.drawContours(image, c, -1, (randint(0, 255), randint(0,255), randint(0,255)), 3)

ALL_CONTOURS = contours[0]
for x in range(1, len(contours)):
    ALL_CONTOURS = np.append(ALL_CONTOURS, contours[x], axis=0)

FOOT_CENTER = get_center_of_contours(ALL_CONTOURS)
cv2.circle(image, FOOT_CENTER, 7, (0, 255, 0), -1)
big_toe_center = get_center_of_contours(contours[-2])
cv2.circle(image, big_toe_center, 7, (0, 255, 0), -1)
if FOOT_CENTER[0] > big_toe_center[0]:
    print("right")
else:
    print("left")
# c = max(all_contours, key=cv2.contourArea)
extLeft, extRight, extTop, extBot = get_extreme_points(ALL_CONTOURS)

cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)

cv2.rectangle(image, (extLeft[0], extTop[1]), (extRight[0],extBot[1]), (255, 0, 0), 2)
cv2.imshow("image", image)

# low = np.array([0, 0, 0])
# medium = np.array([100, 100, 100])
# high = np.array([150, 150, 150])
# ultra_high = np.array([200, 200, 200])
# # Mask image to only select browns
# mask = cv2.inRange(img, low, medium)
# mask2 = cv2.inRange(img, medium, high)
# mask3 = cv2.inRange(img, high, ultra_high)
# # Change image to red where we found brown
# img[mask > 0] = (0, 0, 255)
# img[mask2 > 0] = (0, 153, 255)
# img[mask3 > 0] = (129, 255, 255)
# cv2.imshow("image", img)
# cv2.imshow("threshold", img)



cv2.waitKey(0)
cv2.destroyAllWindows()
