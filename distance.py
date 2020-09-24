# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2 as cv


def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    # hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, (36, 25, 25), (70, 255, 255))

    # gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(mask, (5, 5), 0)
    edged = cv.Canny(gray, 35, 125)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv.contourArea)
    # compute the bounding box of the of the paper region and return it
    return cv.minAreaRect(c)


def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 50
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 12.5
# load the first image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
cap = cv.VideoCapture(0)

image = cv.imread("test.jpg")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH


while True:
    _, image = cap.read()
    if image is None:
        print("none")
        continue

    # loop over the images
        # load the image, find the marker in the image, then compute the
        # distance to the marker from the camera
    # image = cv.imread(image)
    marker = find_marker(image)
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    # draw a bounding box around the image and display it
    box = cv.boxPoints(marker)
    box = np.int0(box)
    cv.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv.putText(image, "%.2fft" % (inches / 12),
                (image.shape[1] - 200, image.shape[0] - 20), cv.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)
    cv.imshow("image", image)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
