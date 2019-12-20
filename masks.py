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

path = "/home/spodek/Pulpit/odbitki stop/Scan21.png"
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
footLeft, footRight, footTop, footBot = get_extreme_points(contours[-1])
toeLeft, toeRight, toeTop, toeBot = get_extreme_points(contours[-2])

cv2.circle(image, footLeft, 8, (0, 0, 255), -1)
cv2.circle(image, footRight, 8, (0, 255, 0), -1)
cv2.circle(image, toeTop, 8, (255, 0, 0), -1)
cv2.circle(image, footBot, 8, (255, 255, 0), -1)

# cv2.rectangle(image, (footLeft[0], toeTop[1]), (footRight[0], footBot[1]), (255, 0, 0), 2)  ### PROSTOKĄT
# cv2.imshow("image", image)

CROPPED_FOOT = img[toeTop[1]:footBot[1], footLeft[0]:footRight[0]]
height, width = CROPPED_FOOT.shape
HEEL = CROPPED_FOOT[3*height//4:, :]
ARCH = CROPPED_FOOT[(3*height//4)-(1*height//4):2*height//3, :]

ret, thresh_heel = cv2.threshold(HEEL, 245, 255, 0)
ret, thresh_arch = cv2.threshold(ARCH, 245, 255, 0)

thresh_heel = cv2.bitwise_not(thresh_heel)
thresh_arch = cv2.bitwise_not(thresh_arch)

contours_heel, hierarchy = cv2.findContours(thresh_heel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_arch, hierarchy = cv2.findContours(thresh_arch, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours_heel = [x for x in contours_heel if len(x) > 10]
contours_arch = [x for x in contours_arch if len(x) > 10]

ALL_HEEL_CONTOURS = contours_heel[0]
ALL_ARCH_CONTOURS = contours_arch[0]

for x in range(1, len(contours_heel)):
    ALL_HEEL_CONTOURS = np.append(ALL_HEEL_CONTOURS, contours_heel[x], axis=0)
heelLeft, heelRight, _, _ = get_extreme_points(ALL_HEEL_CONTOURS)

for x in range(1, len(contours_arch)):
    ALL_ARCH_CONTOURS = np.append(ALL_ARCH_CONTOURS, contours_heel[x], axis=0)
archLeft, archRight, _, _ = get_extreme_points(ALL_ARCH_CONTOURS)

cv2.circle(image, (footLeft[0]+heelLeft[0], heelLeft[1]+toeTop[1] + 3*height//4), 8, (0, 0, 255), -1)
cv2.circle(image, (footLeft[0]+heelRight[0], heelRight[1]+toeTop[1] + 3*height//4), 8, (0, 255, 0), -1)

cv2.circle(image, (footLeft[0]+archLeft[0], archLeft[1]+toeTop[1]+ (3*height//4)-(1*height//4)), 8, (0, 0, 255), -1)
cv2.circle(image, (footLeft[0]+archRight[0], archRight[1]+toeTop[1]+ (3*height//4)-(1*height//4)), 8, (0, 255, 0), -1)

cv2.imshow("cropped", image)

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


def get_distance_two_outside_points(one, two, mode="horizontal"):
    return abs(one[1] - two[1]) if mode == "vertical" else abs(one[0] - two[0])

H_IMG = np.size(image, 0)
H_A4 = 297
W_IMG = np.size(image, 1)
W_A4 = 210
ratio = round(H_IMG/H_A4, 4)
### GET FOOT HEIGHT
foot_length = get_distance_two_outside_points(toeTop, footBot, "vertical")/ratio/10
foot_width = get_distance_two_outside_points(footLeft, footRight, "horizontal")/ratio/10
print("length: {}cm".format(round(foot_length, 2)))
print("width: {}cm".format(round(foot_width, 2)))
print("wspolczynnik: {}".format(foot_length/foot_width))
cv2.waitKey(0)
cv2.destroyAllWindows()
