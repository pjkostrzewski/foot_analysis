from part import *
from paint import Paint
from singleton_decorator import singleton
import exceptions


def get_foot_parts_from_cnts(cnts):
    sorted_parts = sorted(cnts, key=cv.contourArea, reverse=True)
    return [Part(x, number) for number, x in list(enumerate(sorted_parts, 1))]


def right_or_left(big_toe_center, small_toe_center):
    return "RIGHT" if big_toe_center[0] < small_toe_center[0] else "LEFT"


@singleton
class Foot:
    def __init__(self, path_to_file):
        self.path = path_to_file
        self.image = cv.imread(self.path)
        self.height_img = np.size(self.image, 0)
        self.width_image = np.size(self.image, 1)
        height_a4 = 297
        width_a4 = 210
        self._pixel_ratio = round(self.height_img/height_a4, 4)
        self.painter = Paint(self.image)
        self.edged = self.painter.get_edged()
        self.all_cnts = self.set_cnts_from_edges()
        self._detected_parts = str(len(self.all_cnts))
        self._foot_parts = get_foot_parts_from_cnts(self.all_cnts)
        self._foot_contour = self.all_cnts
        self.side = right_or_left(self.foot_parts[0].center, self.foot_parts[-1].center)
        #POINTS
        self.outside_points = self.set_foot_outside_points()
        self.top = self.outside_points["top"]
        self.bottom = self.outside_points["bottom"]
        self.left = self.foot_parts[0].outside_points["left"]
        self.right = self.foot_parts[0].outside_points["right"]
        #LENGTH
        self.foot_length = get_distance_two_outside_points(self.top, self.bottom, self.pixel_ratio, mode='vertical')
        self.foot_width = get_distance_two_outside_points(self.left, self.right, self.pixel_ratio, mode='horizontal')

    def __repr__(self):
        return "{} from {} -> ratio: {}, length: {}cm, width: {}cm, parts: {}".format(
            self.__class__.__name__, self.path, self.pixel_ratio, self.foot_length, self.foot_width, self._detected_parts)

    @property
    def pixel_ratio(self) -> float:
        return self._pixel_ratio
    #
    # @property
    # def detected_parts(self) -> int:
    #     return self._detected_parts

    def set_cnts_from_edges(self):
        cnts = cv.findContours(self.edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # if len(cnts) < 3 or len(cnts) > 7:
        #     raise exceptions.NotEnoughPartsToAnalysis
        # else:
        #     return cnts
        return cnts


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

    def show_image(self):
        cv.imshow("image", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def write_image(self, path):
        cv.imwrite(path, img=self.image)

    def set_foot_outside_points(self):
        c = self.all_cnts[0]
        for x in range(1, len(self.all_cnts)):
            c = np.append(c, self.all_cnts[x], axis=0)
        return set_outside_points(c)


f = Foot('src/gosia_4.png')
print(f)
# for part in f.foot_parts:
#     print(part)
#     print(part.center)
#     f.painter.draw_point(part.center, (255, 255, 0))
    # f.painter.draw_point(part.outside_points["left"], (0, 50, 255))
    # f.painter.draw_point(part.outside_points["right"], (0, 255, 255))
    # f.painter.draw_point(part.outside_points["top"], (255, 255, 0))
    # f.painter.draw_point(part.outside_points["bottom"], (255, 255, 0))
temp = f.foot_parts[1].outside_points["left"]
f.painter.draw_line(f.left, temp, (102, 222, 59))
f.painter.draw_line(f.left, (f.left[0], temp[1]), (0, 222, 159))
print(f.left, temp)
f.painter.draw_point(temp, (127, 127, 0))
f.painter.draw_point(f.top, (0, 50, 255))
f.painter.draw_point(f.bottom, (0, 50, 255))
f.painter.draw_point(f.left, (0, 50, 255))
f.painter.draw_point(f.right, (0, 50, 255))


print(f.side)

f.painter.draw_line(f.foot_parts[1].outside_points["top"], f.foot_parts[0].outside_points["bottom"], (0, 255, 0))
f.painter.draw_line(f.foot_parts[0].outside_points["left"], f.foot_parts[0].outside_points["right"], (0, 255, 0))
f.write_image("src/gosia_4_result.png")

