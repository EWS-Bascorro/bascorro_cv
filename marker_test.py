import cv2 as cv
import imutils
from settings import *

cv.namedWindow("trackbars", cv.WINDOW_NORMAL)
cv.resizeWindow("trackbars", 600, 600)

windows_name = "trackbars"
cv.namedWindow(windows_name, cv.WINDOW_NORMAL)
cv.resizeWindow(windows_name, 300, 500)

f = lambda x: print(x)

cv.createTrackbar("t1", windows_name, 100, 200, f)
cv.createTrackbar("t2", windows_name, 100, 200, f)
cv.createTrackbar("t3", windows_name, 100, 200, f)
cv.createTrackbar("t4", windows_name, 100, 200, f)
cv.createTrackbar("t5", windows_name, 100, 200, f)
cv.createTrackbar("t6", windows_name, 100, 200, f)

cap = cv.VideoCapture(0)
while True:
    _, image = cap.read()
    # convert the image to grayscale, blur it, and detect edges
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, (10, 10, 10), (10, 10, 10))

    # gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(mask, (5, 5), 0)
    edged = cv.Canny(gray, 35, 125)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    try:
        c = max(cnts, key=cv.contourArea)
    except Exception:
        pass
    # compute the bounding box of the of the paper region and return it
    # cv.imshow("image", image)
    cv.imshow("image", edged)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
