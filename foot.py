from part import *


def paint_gray(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (9, 9), 7)
    return gray


def paint_median(gray):
    return cv.medianBlur(gray, 9)


def paint_edged(median):
    edged = cv.Canny(median, 50, 50)
    edged = cv.dilate(edged, None, iterations=3)
    edged = cv.erode(edged, None, iterations=1)
    return edged


def do_some_painting_shit(image):
    gray = paint_gray(image)
    median = paint_median(gray)
    edged = paint_edged(median)
    return edged


def get_foot_parts_from_cnts(cnts):
    sorted_parts = sorted(cnts, key=cv.contourArea, reverse=True)
    return [Part(x, number) for number, x in list(enumerate(sorted_parts, 1))]


def right_or_left(big_toe_center, small_toe_center):
    return "RIGHT" if big_toe_center[0] < small_toe_center[0] else "LEFT"


class Foot:
    def __init__(self, path_to_file):
        self.path = path_to_file
        self.image = cv.imread(self.path)
        self.height_img = np.size(self.image, 0)
        self.width_image = np.size(self.image, 1)
        height_a4 = 297
        width_a4 = 210
        self._pixel_ratio = round(height_a4/width_a4, 4)
        self.edged = do_some_painting_shit(self.image)
        self.all_cnts = self.set_cnts_from_edges()
        self._detected_parts = str(len(self.all_cnts))
        self._foot_parts = get_foot_parts_from_cnts(self.all_cnts)
        self._foot_contour = self.all_cnts
        self.side = right_or_left(self.foot_parts[0].center, self.foot_parts[-1].center)

    @property
    def pixel_ratio(self) -> float:
        return self._pixel_ratio
    #
    # @property
    # def detected_parts(self) -> int:
    #     return self._detected_parts

    def set_cnts_from_edges(self):
        cnts = cv.findContours(self.edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return imutils.grab_contours(cnts)


    @property
    def foot_contour(self):
        return self._foot_contour

    @foot_contour.setter
    def foot_contour(self, cnts):
        '''
        :param cnts: all contours detected
        :return: foot contour
        '''
        c = cnts[0]
        for x in range(1, len(cnts)-1):
            self._foot_contour = np.append(c, cnts[x], axis=0)

    @property
    def foot_parts(self):
        return self._foot_parts

    @foot_parts.setter
    def foot_parts(self, cnts):
        self._foot_parts = get_foot_parts_from_cnts(cnts)


f = Foot('src/two.png')
# print(f.foot_parts)
# print(type(f.foot_contour))
for part in f.foot_parts:
    print(part)
    print(part.center)
    cv.circle(f.image, part.center, 11, (255, 255, 0), -1)
    cv.circle(f.image, part.outside_points["left"], 8, (0, 50, 255), -1)
    cv.circle(f.image, part.outside_points["right"], 8, (0, 255, 255), -1)
    cv.circle(f.image, part.outside_points["top"], 8, (255, 50, 0), -1)
    cv.circle(f.image, part.outside_points["bottom"], 8, (255, 255, 0), -1)
print(f.side)

### DRAWING

# cv.line(f.image, top, bottom, (0, 255, 0), thickness=3, lineType=8)
# cv.line(f.image, left, right, (0, 255, 0), thickness=3, lineType=8)
cv.imshow("image", f.image)
cv.imwrite("src/two_result.png", img=f.image)
# cv.imshow("edged", edged)
# cv.imshow("gray", gray)
# cv.waitKey(0)
# cv.destroyAllWindows()