# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 17:51:29 2019

@author: Binatang Kesusahan
"""
import cv2 as cv
import numpy as np
import imutils
import settings as rw
import argparse
from imutils.video import WebcamVideoStream

ap = argparse.ArgumentParser()

ap.add_argument("-c", "--camera", type=int, default=0, help="change camera")
ap.add_argument("-d", "--display", type=int, default=1, help="Whether or not frame should be displayed")

args = ap.parse_args()

cv.namedWindow("trackbars", cv.WINDOW_NORMAL)
cv.resizeWindow("trackbars", 300, 500)
cv.createTrackbar("L - H", "trackbars", int(rw.read("setting/LH_gawang.txt")), 179, lambda x: rw.write(x, "setting/LH_gawang.txt"))
cv.createTrackbar("L - S", "trackbars", int(rw.read("setting/LS_gawang.txt")), 255, lambda x : rw.write(x, "setting/LS_gawang.txt"))
cv.createTrackbar("L - V", "trackbars", int(rw.read("setting/LV_gawang.txt")), 255, lambda x : rw.write(x, "setting/LV_gawang.txt"))
cv.createTrackbar("U - H", "trackbars", int(rw.read("setting/UH_gawang.txt")), 179, lambda x: rw.write(x, "setting/UH_gawang.txt"))
cv.createTrackbar("U - S", "trackbars", int(rw.read("setting/US_gawang.txt")), 255, lambda x: rw.write(x, "setting/US_gawang.txt"))
cv.createTrackbar("U - V", "trackbars", int(rw.read("setting/UV_gawang.txt")), 255, lambda x : rw.write(x, "setting/UV_gawang.txt"))

cv.createTrackbar("dilation", "trackbars", int(rw.read("setting/dilation_gawang.txt")), 20, lambda x : rw.write(x, "setting/dilation_gawang.txt"))
cv.createTrackbar("Dilation iterations", "trackbars", int(rw.read("setting/dilation_iteration_gawang.txt")), 10, lambda x : rw.write(x, "setting/dilation_iteration_gawang.txt"))
cv.createTrackbar("erosion", "trackbars", int(rw.read("setting/erosion_gawang.txt")), 20, lambda x : rw.write(x, "setting/erosion_gawang.txt"))
cv.createTrackbar("Erosion iterations", "trackbars", int(rw.read("setting/erosion_iteration_gawang.txt")), 10, lambda x : rw.write(x, "setting/erosion_iteration_gawang.txt"))
cv.createTrackbar("gaussian", "trackbars", int(rw.read("setting/gaussian_gawang.txt")), 20, lambda x : rw.write(x, "setting/gaussian_gawang.txt"))
cv.createTrackbar("radius", "trackbars", int(rw.read("setting/radius_gawang.txt")), 20, lambda x : rw.write(x, "setting/radius_gawang.txt"))

#cap = WebcamVideoStream(args.camera).start()
cap = cv.VideoCapture("gambar/reg3.mp4")
while True:
    ret ,frame = cap.read()
    if not ret:
            cap = cv.VideoCapture("gambar/reg3.mp4")
            continue

    frame =  imutils.resize(frame, width=300)
    tinggi, panjang, _ = frame.shape

    gaussian_kernel = int(rw.read("setting/gaussian_gawang.txt"))
    gaussian_kernel = rw.odd(gaussian_kernel)

    frame = cv.GaussianBlur(frame, (gaussian_kernel,gaussian_kernel), 0)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    l_h = int(rw.read("setting/LH_gawang.txt"))
    l_s = int(rw.read("setting/LS_gawang.txt"))
    l_v = int(rw.read("setting/LV_gawang.txt"))
    u_h = int(rw.read("setting/UH_gawang.txt"))
    u_s = int(rw.read("setting/US_gawang.txt"))
    u_v = int(rw.read("setting/UV_gawang.txt"))


    lower_white = np.array([l_h,l_s,l_v])
    upper_white = np.array([u_h,u_s,u_v])

    mask = cv.inRange(hsv, lower_white, upper_white)

    erosion = int(rw.read("setting/erosion_gawang.txt"))
    erosion = rw.odd(erosion)

    dilation= int(rw.read("setting/dilation_gawang.txt"))
    dilation = rw.odd(dilation)

    erosion_iterations = int(rw.read("setting/erosion_iteration_gawang.txt"))
    dilation_iterations = int(rw.read("setting/dilation_iteration_gawang.txt"))

    erosion_kernel = cv.getStructuringElement(cv.MORPH_RECT, (erosion, erosion))
    dilation_kernel = cv.getStructuringElement(cv.MORPH_RECT, (dilation, dilation))

    mask = cv.erode(mask, erosion_kernel, iterations = erosion_iterations)
    mask = cv.dilate(mask, dilation_kernel, iterations = dilation_iterations)

    result = cv.bitwise_and(frame, frame, mask = mask)

    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    x = 0
    y = 0
    radius = 0
    ''''
        if len(contours) > 0:
            c = max(contours, key=cv.contourArea)
            ((x, y), radius) = cv.minEnclosingCircle(c)
            M = cv.moments(c)

            if int(M["m00"]) > 0:

                rads = int(rw.read("setting/radius_gawang.txt"))
                if radius > rads:

                    cv.circle(result, (int(x), int(y)), int(radius), (0,255,255), 2)
                    cv.circle(result, (int(x), int(y)), 5, (0,0,255), -1)
                    cv.putText(result, "x : {} y : {}".format(int(x), int(y)), (10, tinggi-25), cv.FONT_HERSHEY_COMPLEX_SMALL,0.8, (10,255,10))

        cv.line(result, (int(panjang/3), tinggi), (int(panjang/3),0), (0,255,0), 2) #kiri
        cv.line(result, (int(2*panjang/3), tinggi), (int(2*panjang/3),0), (0,255,0), 2) # kanan
        cv.line(result, (0, int(2*tinggi/3)), (panjang, int(2*tinggi/3) ), (123,10,32), 2) #bawah
    '''


    if args.display > 0:
        cv.imshow("result", result)
        cv.imshow("mask", mask)
        cv.imshow("frame", frame)



    key = cv.waitKey(25)
    if key == 27:
        break

cap.stop()
cv.destroyAllWindows()
