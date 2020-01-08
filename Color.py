from random import randint


palette = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255)
}

class Color(object):
    
    def __init__(self, rgb=(randint(0,255), randint(0,255), randint(0,255))):
        self.b, self.r, self.g  = self.set(rgb)

    def __call__(self, rgb):
        self.set(rgb)
        
    def get(self):
        return (self.r, self.g, self.b)

    def set(self, rgb):
        if isinstance(rgb, str):
            return palette[rgb]
        elif isinstance(rgb, tuple) and len(rgb) == 3:
            return rgb
        else:
            raise KeyError("Wrong value. {}".format(rgb))
