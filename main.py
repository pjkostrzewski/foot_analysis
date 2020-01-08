from FootPart import *
from Index import (
    WejsflogIndex, GammaIndex, 
    SztriterGodunowIndex, BalakirewIndex, 
    AlfaIndex, BetaIndex
)
from logic import draw_line

# INPUT  

path = "C:\\Users\\pkostrze\\Desktop\\odbitki stop\\Scan17.png"
image = load_and_resize(path, decrease)
image_black = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
H_IMG = np.size(image, 0)
H_A4 = 297
W_IMG = np.size(image, 1)
W_A4 = 210
ratio = round(H_IMG/H_A4, 4)/10

# MODIFY
img = cv2.GaussianBlur(image_black, (7, 7), 3)
img = cv2.medianBlur(img, 7)
ret, thresh = cv2.threshold(img, 245, 255, 0)

# AREAS
low = np.array([0, 0, 0])
medium = np.array([200, 200, 200])
high = np.array([220, 220, 220])
img_help = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
mask_1 = cv2.inRange(img_help, low, medium)
mask_2 = cv2.inRange(img_help, medium, high)
image[mask_1 > 0] = (140, 88, 253)
image[mask_2 > 0] = (140, 253, 255)

#CONTOURS
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours[1:], key=len)[-6:]
print(len(contours), "contours!")

# FOOT MANAGER
FOOT = FootManager(contours)

# DRAW
FOOT.draw(image)
FOOT.top.draw(image)
FOOT.left.draw(image)
FOOT.right.draw(image)
FOOT.bottom.draw(image)


wejsflog = WejsflogIndex(FOOT)
print(wejsflog())

CROPPED_FOOT = img[FOOT.top()[1]: FOOT.bottom()[1], FOOT.left()[0]: FOOT.right()[0]]
height, width = CROPPED_FOOT.shape
heel_cropped = CROPPED_FOOT[3*height//4:, :]

ALL_HEEL_CONTOURS = do_magic_bro(heel_cropped)
HEEL = FootPart(ALL_HEEL_CONTOURS)

arch_cropped= CROPPED_FOOT[(3*height//4) - (1*height//4): 2*height//3, :]
ALL_ARCH_CONTOURS = do_magic_bro(arch_cropped)
ARCH = FootPart(np.sort(ALL_ARCH_CONTOURS, axis=1))

idx_1_4 = len(ARCH.contours)//4
ARCH.left = Point(ARCH.contours[idx_1_4][0])
ARCH.right = Point(tuple(ARCH.contours[-idx_1_4][0]))



HEEL.left =move(FOOT, HEEL.left, 3*height//4)
HEEL.right =move(FOOT, HEEL.right, 3*height//4)
HEEL.left.draw(image)
HEEL.right.draw(image)


ARCH.left = move(FOOT, ARCH.left, (3*height//4)-(1*height//4))
ARCH.right = move(FOOT, ARCH.right, (3*height//4)-(1*height//4))
ARCH.left.draw(image)
ARCH.right.draw(image)

gamma = GammaIndex(FOOT, HEEL)
print(gamma())


sztriter_godunov = SztriterGodunowIndex(FOOT, HEEL, ARCH)
print(sztriter_godunov())

balakirew = BalakirewIndex(FOOT, HEEL)
print(balakirew())
balakirew.point_top.draw(image)
balakirew.point_bottom.draw(image)

alfa = AlfaIndex(FOOT, HEEL)
print(alfa())

beta = BetaIndex(FOOT, HEEL)
print(beta())
FOOT.big_toe.right.draw(image)
to_draw = [
    (balakirew.point_top, balakirew.point_bottom),
    (FOOT.left, HEEL.left),
    (FOOT.right, HEEL.right),
    (FOOT.left, FOOT.right),
    (FOOT.top, FOOT.bottom),
    (ARCH.left, ARCH.right),
    (HEEL.right, ARCH.left),
    (HEEL.right, ARCH.right),
    (FOOT.right, ARCH.left),
    (FOOT.right, ARCH.right),
    (FOOT.big_toe.right, FOOT.right)
]

for points in to_draw:
    draw_line(image, *points)
    


cv2.imshow("cropped", image)
cv2.waitKey(0)
cv2.destroyAllWindows()