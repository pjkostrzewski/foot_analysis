from Color import Color
import cv2

class Point:
    def __init__(self, xy):
        self.x, self.y = xy

    def __call__(self):
        return self.x, self.y

    def draw(self, image):
        cv2.circle(image, (self.x, self.y), 8, Color("GREEN").get(), -1)

    def get(self):
        return self.x, self.y

