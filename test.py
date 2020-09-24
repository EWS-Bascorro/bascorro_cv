import argparse
import logging

import cv2
import numpy as np

from settings import Settings

logger = logging.getLogger()
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(15, GPIO.OUT, initial=0)
# GPIO.setup(20, GPIO.IN)
s = Settings()

# ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1.0)
flag = chr(0xFF)


def kirim(data1, data2):
    pass
    # m_byte1 = int(data1 / 2)
    # byte1 = chr(m_byte1)
    # byte2 = chr(data2)
    # ser.write(flag)
    # ser.write(byte1)
    # ser.write(byte2)


kernel = np.ones((5, 5), np.uint8)


# os.system('sudo modprobe bcm2835-v4l2')


def show_trackbars(window_name="trackbars_windows"):
    cv2.namedWindow(window_name, cv2.WINDOW_FULLSCREEN)
    cv2.createTrackbar("LH", window_name, s.read("LH"), 255, (lambda x: (s.update_or_insert("LH", x))))
    cv2.createTrackbar("LS", window_name, s.read("LS"), 255, (lambda x: (s.update_or_insert("LS", x))))
    cv2.createTrackbar("LV", window_name, s.read("LV"), 255, (lambda x: (s.update_or_insert("LV", x))))
    cv2.createTrackbar("UH", window_name, s.read("UH"), 255, (lambda x: (s.update_or_insert("UH", x))))
    cv2.createTrackbar("US", window_name, s.read("US"), 255, (lambda x: (s.update_or_insert("US", x))))
    cv2.createTrackbar("UV", window_name, s.read("UV"), 255, (lambda x: (s.update_or_insert("UV", x))))
    cv2.createTrackbar("RAD", window_name, s.read("RAD"), 255, (lambda x: (s.update_or_insert("RAD", x))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-d', action='store_true')
    arg = parser.parse_args()

    if arg.d:
        cv2.namedWindow('HueComp')
        cv2.namedWindow('SatComp')
        cv2.namedWindow('ValComp')
        cv2.namedWindow('closing')
        cv2.namedWindow('mask')
    if arg.t:
        show_trackbars()
        cv2.namedWindow('tracking')

    w = 360
    h = 330

    try:
        cap = cv2.VideoCapture(2)
    except Exception:
        cap = cv2.VideoCapture(-1)

    cap.set(3, w)
    cap.set(4, h)

    while True:
        _, frame = cap.read()
        if frame is None:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hue, sat, val = cv2.split(hsv)

        # if (GPIO.input(20) == False):
        if True:

            hmn = s.read("LH")
            hmx = s.read("UH")
            smn = s.read("LS")
            smx = s.read("US")
            vmn = s.read("LV")
            vmx = s.read("UV")
            rad = s.read("RAD")

            lower_white = np.array([hmn, smn, vmn])
            upper_white = np.array([hmx, smx, vmx])

            # cv2.putText(frame, "BOLA", (2, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

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

            KIRI = int(w * (1 / 3))
            KANAN = int(w * (2 / 3))

            cv2.line(frame, (KIRI,0), (KIRI, h), (255, 0, 0), thickness=1)
            cv2.line(frame, (KANAN, 0), (KANAN, h), (0, 255, 0), thickness=1)

            if rad > 20:
                if area < 2000000:
                    try:
                        x = int(coordinates['m10'] / coordinates['m00'])
                        y = int(coordinates['m01'] / coordinates['m00'])
                    except:
                        pass
                    # GPIO.output(15, True)
                    # print('1')
                    if KANAN < x < KIRI:
                        kirim(x, y)

                    cv2.circle(frame, (x, y), 5, (0, 255, 0), 4)

                    cv2.putText(frame, str(x), (2, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, str(y), (120, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                kirim(0, 0)

        if arg.d:
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
    s.write()


if __name__ == '__main__':
    main()
