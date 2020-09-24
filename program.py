from enum import Enum

import cv2 as cv
import numpy as np
import logging
from settings import Settings


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class Program:
    class State(Enum):
        STATE_BAR = 1
        STATE_TURNING = 2

    def __init__(self, camera=0):
        self._camera = camera
        self._setting = Settings()
        self._kalman = cv.KalmanFilter(4, 2)
        self._kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self._kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self._kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                                                np.float32) * 0.03
        self.init_cap()

    def init_cap(self):
        self._camera = 0
        cap = cv.VideoCapture(self._camera)
        retry = 0

        while cap.read()[1] is None:
            if retry <= 100:
                cap.release()
                cap = cv.VideoCapture(self._camera)
                retry += 1
            else:
                raise Exception("Cant connect to camera")

        return cap

    def filter_color(self, img, prefix="_", tpx=0, tpy=0):

        uh = self._setting.read(prefix + "UH")
        us = self._setting.read(prefix + "US")
        uv = self._setting.read(prefix + "UV")

        lh = self._setting.read(prefix + "LH")
        ls = self._setting.read(prefix + "LS")
        lv = self._setting.read(prefix + "LV")
        rad = self._setting.read(prefix + "RADIUS")

        img = cv.medianBlur(img, 5)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        lower_hsv = np.array([lh, ls, lv])
        upper_hsv = np.array([uh, us, uv])
        # greenLower = (29, 86, 6)
        # greenUpper = (64, 255, 255)

        mask = cv.inRange(hsv, lower_hsv, upper_hsv)
        img2, contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            c = max(contours, key=cv.contourArea)
            _, _, radius = cv.minEnclosingCircle(c)
            M = cv.moments(c)

            if int(M["m00"]) > 0:
                cx = int(M["m10"]) / int(M["m00"])
                cy = int(M["m01"]) / int(M["m00"])
                center = (int(cx), int(cy))
                if radius > rad:
                    self._kalman.correct(np.array([[center[0]], [center[1]]], np.float32))
                    tp = self._kalman.predict()
                    tpx = int(tp[0])
                    tpy = int(tp[1])

        return mask, tpx, tpy

        # frame_counter += 1
        # if frame_counter == int(cap.get(cv.CAP_PROP_FRAME_COUNT)) - 70:
        #     frame_counter = 0
        #     cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    def show_trackbars(self, window_name="trackbars_windows"):
        cv.namedWindow(window_name, cv.WINDOW_FULLSCREEN)
        for key, v in self._setting.setting.items():
            cv.createTrackbar(key, window_name, v, 255, (lambda x: (self._setting.update_or_insert(key, x))))
            logger.info(f"Created trackbars for {key}")