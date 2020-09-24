import logging
import sys

import cv2 as cv
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store_true')

arg = parser.parse_args()

from settings import Settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
s = Settings()


def show_trackbars(window_name="trackbars_windows"):
    cv.namedWindow(window_name, cv.WINDOW_FULLSCREEN)
    for key, v in s.setting.items():
        cv.createTrackbar(key, window_name, v, 255, (lambda x: (s.update_or_insert(key, x))))
        logger.info(f"Created trackbars for {key}")


# cap = cv.VideoCapture('video/test1.webm')
camera = 0
cap = cv.VideoCapture(camera)
retry = 0

while cap.read()[1] is None:
    if retry <= 100:
        cap.release()
        cap = cv.VideoCapture(camera)
        retry += 1
    else:
        pass

frame_counter = 0
if arg.t:
    show_trackbars()

kalman = cv.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.03

while True:
    _, img = cap.read()

    # frame_counter += 1
    # if frame_counter == int(cap.get(cv.CAP_PROP_FRAME_COUNT)) - 70:
    #     frame_counter = 0
    #     cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    uh = s.read("UH")
    us = s.read("US")
    uv = s.read("UV")

    lh = s.read("LH")
    ls = s.read("LS")
    lv = s.read("LV")
    RAD = s.read("RADIUS")

    img = cv.medianBlur(img, 5)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)

    mask = cv.inRange(hsv, lower_hsv, upper_hsv)
    img2, contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    x = 0
    y = 0
    center = None
    radius = None
    print(radius, RAD)
    print(len(contours))
    if len(contours) > 0:
        c = max(contours, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)

        if int(M["m00"]) > 0:
            cx = int(M["m10"]) / int(M["m00"])
            cy = int(M["m01"]) / int(M["m00"])
            center = (int(cx), int(cy))
            if radius > RAD:
                kalman.correct(np.array([[center[0]], [center[1]]], np.float32))
                tp = kalman.predict()

                cv.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv.circle(img, center, 5, (0, 0, 255), -1)
                cv.circle(img, (int(tp[0]), int(tp[1])), 5, (0, 255, 0), -1)
                cv.putText(img, "x : {} y : {}".format(int(x), int(y)), (10, 100 - 25),
                           cv.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (10, 255, 10))

    cv.imshow("image", img)

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        s.write()
        cv.destroyAllWindows()
        break
