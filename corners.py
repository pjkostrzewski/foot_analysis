


# def get_corners_of_card(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     edged = cv2.Canny(blurred, 50, 150)
#     cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#     assert len(cnts) >= 4, "not enough contours found. {}".format(len(cnts))
#     print("found: ", len(cnts))
#     # cv2.drawContours(img, cnts, -1, (111, 255,144), 3)
#     # cv2.imshow("before", edged)
#     if len(cnts) > 0:
#         cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
#         for c in cnts:
#             peri = cv2.arcLength(c, True)
#             approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#             if len(approx) == 4:
#                 return approx
#     return None


# def order_points(pts):
#     rect = np.zeros((4, 2), dtype="float32")
#     s = pts.sum(axis=1)
#     rect[0] = pts[np.argmin(s)]
#     rect[2] = pts[np.argmax(s)]
#     diff = np.diff(pts, axis=1)
#     rect[1] = pts[np.argmin(diff)]
#     rect[3] = pts[np.argmax(diff)]
#     return rect


# def four_point_transform(image, pts):
#     # print(pts)
#     pts = pts.astype("float32")
#     pts.shape = (4, 2)
#     rect = order_points(pts)
#     (tl, tr, br, bl) = rect
#     widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
#     widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
#     maxWidth = max(int(widthA), int(widthB))
#     heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
#     heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
#     maxHeight = max(int(heightA), int(heightB))
#     dst = np.array([
#         [0, 0],
#         [maxWidth - 1, 0],
#         [maxWidth - 1, maxHeight - 1],
#         [0, maxHeight - 1]], dtype="float32")
#     M = cv2.getPerspectiveTransform(rect, dst)
#     warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
#     return warped


# def load_and_resize(path, decrease):
#     image = cv2.imread(path, cv2.IMREAD_COLOR)
#     image = cv2.resize(image, None, fx=decrease, fy=decrease)
#     return image


# def left_or_right(image):
#     y, x, _ = image.shape
#     first = image[1:y, 1:int(x/2)]
#     second = image[1:y, int(x/2):x]
#     first_sum = 0
#     second_sum = 0
#     for x in first:
#         for r, g, b in x:
#             rgb_sum = int((r+g+b)/3)
#             if rgb_sum < 100:
#                 first_sum += rgb_sum
#     for x in second:
#         for r, g, b in x:
#             rgb_sum = int((r+g+b)/3)
#             if rgb_sum < 100:
#                 second_sum += rgb_sum
#     assert first_sum != second_sum
#     cv2.imshow("frst", first)
#     cv2.imshow("second", second)
#     print("first:", first_sum)
#     print("second:", second_sum)
#     return "LEFT" if first_sum < second_sum else "RIGHT"
