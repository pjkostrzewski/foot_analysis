from FootPart import FootManager, FootPart
import math
from logic import (
    get_triangle_height, 
    get_distance_two_outside_points, 
    angle_between_points,
    angle_from_sin
)
from Point import Point


class IndexBase(object):
    
    def __init__(self, FOOT: FootManager):
        self.FOOT = FOOT
        self.diagnose = None
        self.value = None

    def __call__(self):
        return self.get()
        
    def get(self):
        return self.diagnose
        
    def set_diagnose(self, state: tuple):
        self.diagnose = state

    def calculate(self):
        pass
   
   
class AlfaIndex(IndexBase):
    
    def __init__(self, FOOT: FootManager, HEEL: FootPart):
        super().__init__(FOOT)
        self.HEEL = HEEL
        self.calculate()
        self.set_diagnose()
        
    def calculate(self):
        self.value = angle_between_points(self.FOOT.big_toe.right, self.FOOT.right, self.HEEL.right)
     
    def set_diagnose(self):
        if self.value < 9:
            self.diagnose = 0, self.value, "stopa normalna"
        else:
            self.diagnose = 1, self.value, "Niepoprawny kąt alfa"
            
            
class BetaIndex(IndexBase):
      
    def __init__(self, FOOT: FootManager, HEEL: FootPart):
        super().__init__(FOOT)
        self.HEEL = HEEL
        self.calculate()
        self.set_diagnose()
    
    def calculate(self):
        self.value = angle_from_sin(self.FOOT.left, self.HEEL.left)
    
    def set_diagnose(self):
        if self.value < 6:
            self.diagnose = 0, self.value, "stopa normalna"
        else:
            self.diagnose = 1, self.value, "Niepoprawny kąt beta"
          
              
class GammaIndex(IndexBase):
    
    def __init__(self, FOOT: FootManager, HEEL: FootPart):
        super().__init__(FOOT)
        self.HEEL = HEEL
        self.calculate()
        self.set_diagnose()
    
    def calculate(self):
        alfa_0 = math.atan2(self.FOOT.right.y - self.HEEL.right.y,
                            self.FOOT.right.x - self.HEEL.right.x)
        alfa_1 = math.atan2(self.FOOT.left.y - self.HEEL.left.y, 
                            self.FOOT.left.x - self.HEEL.left.x)
        self.value = abs(math.degrees(alfa_1 - alfa_0))
        
    def set_diagnose(self):
        if 15 < self.value < 19:
            self.diagnose = 0, self.value, "{} OK".format(self.__class__.__name__)
        else:
            self.diagnose = 1,  self.value, "Kąt gamma nieprawidłowy: {} stopni". format(self.value)
     
class SztriterGodunowIndex(IndexBase):    
    
    def __init__(self, FOOT: FootManager, HEEL: FootPart, ARCH: FootPart):
        super().__init__(FOOT)
        self.HEEL = HEEL
        self.ARCH = ARCH
        self.calculate()
        self.set_diagnose()
        
    def calculate(self):
        height_1 = get_triangle_height(self.HEEL.right, self.FOOT.big_toe.right, self.ARCH.right)
        height_2 = get_triangle_height(self.HEEL.right, self.FOOT.big_toe.right, self.ARCH.left)
        self.value =  height_2-height_1, height_2   
    
    def set_diagnose(self):
        ratio = self.value[0]/self.value[1]
        if 0.0 < ratio < 0.25:
            self.diagnose =  1, ratio, "stopa wydrążona"
        elif 0.26 < ratio < 0.45:
            self.diagnose =  0, ratio, "stopa normalna" 
        if 0.46 < ratio < 0.7:
            self.diagnose =  2, ratio, "stopa obniżona" 
        elif 0.71 < ratio < 1:
            self.diagnose =  3, ratio, "stopa płaska" 
      
         
class BalakirewIndex(IndexBase):
    
    def __init__(self, FOOT: FootManager, HEEL: FootPart):
        super().__init__(FOOT)   
        self.HEEL = HEEL
        self.point_top = self.calculate_top()
        self.point_bottom = self.calculate_bottom()
        self.calculate()
        self.set_diagnose()

    
    def calculate_top(self):
        dis_hor_1 = get_distance_two_outside_points(self.FOOT.left, self.FOOT.right, mode="horizontal")//3
        dis_ver_1 = get_distance_two_outside_points(self.FOOT.left, self.FOOT.right, mode="vertical")//3
        return Point((self.FOOT.right.x-dis_hor_1, self.FOOT.right.y+dis_ver_1))
    
    def calculate_bottom(self):
        dis_hor_2 = get_distance_two_outside_points(self.point_top, self.FOOT.bottom, mode="horizontal")*2//3
        dis_ver_2 = get_distance_two_outside_points(self.point_top, self.FOOT.bottom, mode="vertical")*2//3
        return Point((self.point_top.x-dis_hor_2, self.point_top.y+dis_ver_2))
    
    def calculate(self):
        a = get_distance_two_outside_points(self.point_bottom, self.HEEL.left)
        b = get_distance_two_outside_points(self.point_top, self.FOOT.right)
        self.value = a/b 
        
    def set_diagnose(self):
        """
        więcej niż 1 to stopa jest płaska  
        -mniej niż 1 to stopa jest wydrążona
        - równy 1 to stopa jest normalna
        """
        if self.value >= 1.08:
            self.diagnose = 2, self.value, "stopa płaska"
        if  0.95 < self.value < 1.08:
            self.diagnose = 0, self.value, "stopa normalna"
        if self.value <= 0.95:
            self.diagnose = 1, self.value, "stopa wydrążona"
   
            
class WejsflogIndex(IndexBase):
      
    def __init__(self, FOOT: FootManager):
        super().__init__(FOOT)   
        self.calculate()
        self.set_diagnose()
        
    def calculate(self):
        self.value = self.FOOT.top_bottom/self.FOOT.left_right
        
    def set_diagnose(self):
        if self.value < 2.5:
            diagnose = 1, self.value ,"Płaskostopie poprzeczne"
            self.diagnose =  diagnose
        else:
            self.diagnose = 0, self.value, "{} OK".format(self.__class__.__name__)