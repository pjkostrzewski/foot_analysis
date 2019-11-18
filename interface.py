import cv2 as cv
import numpy as np
import imutils



path = "src/five.png"
image = cv.imread(path)
img = cv.resize(image, None, fx=0.3,fy=0.3)
# img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.GaussianBlur(img, (9, 9), 7)
img = cv.medianBlur(img, 9)
kernel_sharpening = np.array([[-1,-1,-1],
                              [-1, 9,-1],
                              [-1,-1,-1]])# applying the sharpening kernel to the input image & displaying it.
img = cv.filter2D(img, -1, kernel_sharpening)

# laplacian = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)


edged = cv.Canny(img, 70, 40)
edged = cv.dilate(edged, None, iterations=5)
edged = cv.erode(edged, None, iterations=1)
# cv.imshow("image", edged)
# final = cv.hconcat([edged, img])
cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(cnts)
# cv.imshow("image", thresh1)
cv.drawContours(img, cnts, -1, (0, 255, 0), 3)
# ret, threshold = cv.threshold(img, 125, 255, cv.THRESH_BINARY)
low=np.array([0,0,0])
medium=np.array([100,100,100])
high = np.array([150,150,150])
ultra_high = np.array([200,200,200])

# Mask image to only select browns
mask=cv.inRange(img, low, medium)
mask2=cv.inRange(img, medium, high)
mask3=cv.inRange(img, high, ultra_high)
# Change image to red where we found brown
img[mask>0]=(0,0,255)
img[mask2>0]=(0,153,255)
img[mask3>0]=(129,255,255)
# cv.imshow("image", img)
cv.imshow("threshold", img)
cv.waitKey(0)
cv.destroyAllWindows()