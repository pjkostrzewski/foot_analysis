from corners import *
from variables import *


path = 'src/skalowane1.png'
# path = 'src/gosia6.jpg'
image = load_and_resize(path, decrease)

coords = get_corners_of_card(image)
cv2.drawContours(image, coords, -1, (0,255,0), 3)

warped = four_point_transform(image, coords)

# cv2.imshow("before", image)
# cv2.imshow("after", warped)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img = cv2.GaussianBlur(warped, (9, 9), 7)
img = cv2.medianBlur(img, 9)
kernel_sharpening = np.array([[-1,-1,-1],
                              [-1, 9,-1],
                              [-1,-1,-1]])# applying the sharpening kernel to the input image & displaying it.
img = cv2.filter2D(img, -1, kernel_sharpening)

# laplacian = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)


edged = cv2.Canny(img, 70, 40)
edged = cv2.dilate(edged, None, iterations=5)
edged = cv2.erode(edged, None, iterations=1)
# cv2.imshow("threshold", edged)
cv2.imshow("image", edged)
# final = cv2.hconcat([edged, img])
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(cnts)
# cv2.imshow("image", thresh1)
cv2.drawContours(img, cnts, -1, (0, 255, 0), 3)
# ret, threshold = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
low=np.array([0,0,0])
medium=np.array([100,100,100])
high = np.array([150,150,150])
ultra_high = np.array([200,200,200])

# Mask image to only select browns
mask=cv2.inRange(img, low, medium)
mask2=cv2.inRange(img, medium, high)
mask3=cv2.inRange(img, high, ultra_high)
# Change image to red where we found brown
img[mask>0]=(0,0,255)
img[mask2>0]=(0,153,255)
img[mask3>0]=(129,255,255)
cv2.imshow("image", img)
cv2.imshow("threshold", img)
cv2.waitKey(0)
cv2.destroyAllWindows()