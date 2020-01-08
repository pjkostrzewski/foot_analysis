from logic import *

class FootPart(object):

    def __init__(self, contours):
        self.contours = contours
        self.left, self.right, self.top, self.bottom = self._get_extreme_points()
        self.center = self._get_center()

    def _get_extreme_points(self):
        c = self.contours
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        return Point(extLeft), Point(extRight), Point(extTop), Point(extBot)

    def _get_center(self):
        M = cv2.moments(self.contours)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return Point((cX, cY))

    def draw(self, image, color=None):
        if color is None:
            color = Color("BLUE")
        cv2.drawContours(image, self.contours, -1, color.get(), 3)


class FootManager(object):

    def __init__(self, contours):
        self.foot_parts = []
        self.set_foot_parts(contours)
        self.big_toe = self.foot_parts[-2]
        self.foot = self.foot_parts[-1]
        
        self.top = self.big_toe.top
        self.left = self.foot.left
        self.bottom = self.foot.bottom
        self.right = self.foot.right
        self.side = self.get_side()

        self.top_bottom = get_distance(self.top, self.bottom)
        self.left_right = get_distance(self.left, self.right)
        
        
    def add_part(self, part):
        self.foot_parts.append(part)

    def set_foot_parts(self, contours):
        for c in [x for x in contours if cv2.contourArea(x) > 100]:
            new_part = FootPart(c)
            self.add_part(new_part)
    
    def draw(self, image):
        for part in self.foot_parts:
            part.draw(image)
    
    def get_side(self):
        return "RIGHT" if self.foot.center.get()[0] > self.top()[0] else "LEFT"
    

    