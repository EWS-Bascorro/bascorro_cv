# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 17:51:29 2019

@author: Binatang Kesusahan
"""
import cv2 as cv
import numpy as np
import imutils
import settings as rw
import serial_rw as srw
from imutils.video import WebcamVideoStream
import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-c", "--camera", type=int, default=0, help="change camera")
ap.add_argument("-d", "--display", type=int, default=1, help="Whether or not frame should be displayed")

args = ap.parse_args()

if args.display > 0:
    cv.namedWindow("trackbars", cv.WINDOW_NORMAL)
    cv.resizeWindow("trackbars", 300, 500)
    cv.createTrackbar("L - H", "trackbars", int(rw.read("setting/LH.txt")), 179, lambda x: rw.write(x, "setting/LH.txt"))
    cv.createTrackbar("L - S", "trackbars", int(rw.read("setting/LS.txt")), 255, lambda x : rw.write(x, "setting/LS.txt"))
    cv.createTrackbar("L - V", "trackbars", int(rw.read("setting/LV.txt")), 255, lambda x : rw.write(x, "setting/LV.txt"))
    cv.createTrackbar("U - H", "trackbars", int(rw.read("setting/UH.txt")), 179, lambda x: rw.write(x, "setting/UH.txt"))
    cv.createTrackbar("U - S", "trackbars", int(rw.read("setting/US.txt")), 255, lambda x: rw.write(x, "setting/US.txt"))
    cv.createTrackbar("U - V", "trackbars", int(rw.read("setting/UV.txt")), 255, lambda x : rw.write(x, "setting/UV.txt"))

    cv.createTrackbar("dilation", "trackbars", int(rw.read("setting/dilation_bola.txt")), 50, lambda x : rw.write(x, "setting/dilation_bola.txt"))
    cv.createTrackbar("Dilation iterations", "trackbars", int(rw.read("setting/dilation_iteration_bola.txt")), 10, lambda x : rw.write(x, "setting/dilation_iteration_bola.txt"))
    cv.createTrackbar("erosion", "trackbars", int(rw.read("setting/erosion_bola.txt")), 50, lambda x : rw.write(x, "setting/erosion_bola.txt"))
    cv.createTrackbar("Erosion iterations", "trackbars", int(rw.read("setting/erosion_iteration_bola.txt")), 10, lambda x : rw.write(x, "setting/erosion_iteration_bola.txt"))
    cv.createTrackbar("gaussian", "trackbars", int(rw.read("setting/gaussian_bola.txt")), 20, lambda x : rw.write(x, "setting/gaussian_bola.txt"))
    cv.createTrackbar("radius", "trackbars", int(rw.read("setting/radius_bola.txt")), 50, lambda x : rw.write(x, "setting/radius_bola.txt"))

cap = WebcamVideoStream(args.camera).start()
while True:
    frame = cap.read()
    frame =  imutils.resize(frame, width=300)
    tinggi, panjang, _ = frame.shape

    gaussian_kernel = int(rw.read("setting/gaussian_bola.txt"))
    gaussian_kernel = rw.odd(gaussian_kernel)

    frame = cv.GaussianBlur(frame, (gaussian_kernel,gaussian_kernel), 0)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    l_h = int(rw.read("setting/LH.txt"))
    l_s = int(rw.read("setting/LS.txt"))
    l_v = int(rw.read("setting/LV.txt"))
    u_h = int(rw.read("setting/UH.txt"))
    u_s = int(rw.read("setting/US.txt"))
    u_v = int(rw.read("setting/UV.txt"))


    lower_white = np.array([l_h,l_s,l_v])
    upper_white = np.array([u_h,u_s,u_v])

    mask = cv.inRange(hsv, lower_white, upper_white)

    erosion = int(rw.read("setting/erosion_bola.txt"))
    erosion = rw.odd(erosion)

    dilation= int(rw.read("setting/dilation_bola.txt"))
    dilation= rw.odd(dilation)

    erosion_iterations = int(rw.read("setting/erosion_iteration_bola.txt"))
    dilation_iterations = int(rw.read("setting/dilation_iteration_bola.txt"))

    erosion_kernel = cv.getStructuringElement(cv.MORPH_RECT, (erosion, erosion))
    dilation_kernel = cv.getStructuringElement(cv.MORPH_RECT, (dilation, dilation))

    mask = cv.erode(mask, erosion_kernel, iterations = erosion_iterations)
    mask = cv.dilate(mask, dilation_kernel, iterations = dilation_iterations)

    result = cv.bitwise_and(frame, frame, mask = mask)

    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    x = 0
    y = 0
    radius = 0

    if len(contours) > 0:
        c = max(contours, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)

        if int(M["m00"]) > 0:

            rads = int(rw.read("setting/radius_bola.txt"))
            if radius > rads :
#                srw.serialWrite(x,y)
                cv.circle(result, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv.circle(result, (int(x), int(y)), 5, (0,0,255), -1)
                cv.putText(result, "Cx : {}  Cy : {}".format(int(x), int(y)), (10, tinggi-25), cv.FONT_HERSHEY_COMPLEX_SMALL,0.8, (10,255,10))
        #else:
 #           srw.serialWrite(0,0)

    #cv.line(result, (int(panjang/3), tinggi), (int(panjang/3),0), (0,255,0), 2) #kiri
    #cv.line(result, (int(2*panjang/3), tinggi), (int(2*panjang/3),0), (0,255,0), 2) # kanan
    #cv.line(result, (0, int(2*tinggi/3)), (panjang, int(2*tinggi/3) ), (123,10,32), 2) #bawah
    if args.display > 0:
        cv.imshow("result", result)
        cv.imshow("mask", mask)
        cv.imshow("frame", frame)

    key = cv.waitKey(1)
    if key == 27:
        break

cap.stop()
cv.destroyAllWindows()
