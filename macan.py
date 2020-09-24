import cv2
import numpy as np
import math
import os
import time
import serial
import io
import RPi.GPIO as GPIO
import socket
import settings as rw

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(15, GPIO.OUT, initial=0)
GPIO.setup(20, GPIO.IN)

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1.0)
flag = chr(0xFF)


def kirim(data1, data2):
    m_byte1 = int(data1 / 2)
    byte1 = chr(m_byte1)
    byte2 = chr(data2)
    ser.write(flag)
    ser.write(byte1)
    ser.write(byte2)


kernel = np.ones((5, 5), np.uint8)

os.system('sudo modprobe bcm2835-v4l2')

w = 160
h = 160

cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('closing')
cv2.namedWindow('mask')
cv2.namedWindow('tracking')

cv2.createTrackbar('hmin', 'HueComp', int(rw.read("setting/LH.txt")), 179, lambda x: rw.write(x, "setting/LH.txt"))
cv2.createTrackbar('hmax', 'HueComp', int(rw.read("setting/UH.txt")), 179, lambda x: rw.write(x, "setting/UH.txt"))

cv2.createTrackbar('smin', 'SatComp', int(rw.read("setting/LS.txt")), 255, lambda x: rw.write(x, "setting/LS.txt"))
cv2.createTrackbar('smax', 'SatComp', int(rw.read("setting/US.txt")), 255, lambda x: rw.write(x, "setting/US.txt"))

cv2.createTrackbar('vmin', 'ValComp', int(rw.read("setting/LV.txt")), 255, lambda x: rw.write(x, "setting/LV.txt"))
cv2.createTrackbar('vmax', 'ValComp', int(rw.read("setting/UV.txt")), 255, lambda x: rw.write(x, "setting/UV.txt"))

while (1):

    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv)

    if (GPIO.input(20) == False):
        hmn = int(rw.read("setting/UH.txt"))
        hmx = int(rw.read("setting/UH.txt"))
        smn = int(rw.read("setting/LS.txt"))  ##---=== BOLA ===---##
        smx = int(rw.read("setting/US.txt"))
        vmn = int(rw.read("setting/LV.txt"))
        vmx = int(rw.read("setting/UV.txt"))

        lower_white = np.array([hmn, smn, vmn])
        upper_white = np.array([hmx, smx, vmx])

        cv2.putText(frame, "BOLA", (2, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        hthresh = cv2.inRange(np.array(hue), np.array(hmn), np.array(hmx))
        sthresh = cv2.inRange(np.array(sat), np.array(smn), np.array(smx))
        vthresh = cv2.inRange(np.array(val), np.array(vmn), np.array(vmx))

        mask = cv2.inRange(hsv, lower_white, upper_white)

        tracking = cv2.bitwise_and(hthresh, cv2.bitwise_and(sthresh, vthresh))

        dilation = cv2.dilate(tracking, kernel, iterations=1)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
        closing = cv2.GaussianBlur(closing, (25, 25), 0)

        coordinates = cv2.moments(closing)
        area = coordinates['m00']

        if (area > 20):
            if (area < 2000000):
                x = int(coordinates['m10'] / coordinates['m00'])
                y = int(coordinates['m01'] / coordinates['m00'])
                GPIO.output(15, True)
                print('1')

                cv2.circle(frame, (x, y), 5, (0, 255, 0), 4)

                kirim(x, y)
                cv2.putText(frame, str(x), (2, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, str(y), (120, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            kirim(0, 0)


    else:
        hmn = 32
        hmx = 36
        smn = 154  ##---=== GAWANG ===---##
        smx = 255
        vmn = 137
        vmx = 190

        cv2.putText(frame, "GAWANG", (2, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        hthresh = cv2.inRange(np.array(hue), np.array(hmn), np.array(hmx))
        sthresh = cv2.inRange(np.array(sat), np.array(smn), np.array(smx))
        vthresh = cv2.inRange(np.array(val), np.array(vmn), np.array(vmx))

        tracking = cv2.bitwise_and(hthresh, cv2.bitwise_and(sthresh, vthresh))

        dilation = cv2.dilate(tracking, kernel, iterations=1)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
        closing = cv2.GaussianBlur(closing, (25, 25), 0)

        coordinates = cv2.moments(closing)
        area = coordinates['m00']

        if (area > 100):
            if (area < 2000000):
                x = int(coordinates['m10'] / coordinates['m00'])
                y = int(coordinates['m01'] / coordinates['m00'])
                GPIO.output(15, True)
                kirim(x, y)

                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 255, 0), 2)
                cv2.putText(frame, str(x), (2, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, str(y), (120, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    GPIO.output(15, False)
    print('0')
    cv2.imshow('HueComp', hthresh)
    cv2.imshow('SatComp', sthresh)
    cv2.imshow('ValComp', vthresh)
    cv2.imshow('closing', closing)
    cv2.imshow('mask', mask)
    cv2.imshow('tracking', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
