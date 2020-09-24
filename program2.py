import settings as rw
import cv2 as cv
import imutils
from imutils.video import WebcamVideoStream
import numpy as np
import argparse

# LOAD CONFIGURATION ###
l_h_gawang = int(rw.read("setting/LH_gawang.txt"))
l_s_gawang = int(rw.read("setting/LS_gawang.txt"))
l_v_gawang = int(rw.read("setting/LV_gawang.txt"))
u_h_gawang = int(rw.read("setting/UH_gawang.txt"))
u_s_gawang = int(rw.read("setting/US_gawang.txt"))
u_v_gawang = int(rw.read("setting/UV_gawang.txt"))

lower_white = np.array([l_h_gawang, l_s_gawang, l_v_gawang])
upper_white = np.array([u_h_gawang, u_s_gawang, u_v_gawang])

dilation_gawang = rw.odd(int(rw.read("setting/dilation_gawang.txt")))
dilation_iteration_gawang = int(rw.read("setting/dilation_iteration_gawang.txt"))
erosion_gawang = rw.odd(int(rw.read("setting/erosion_gawang.txt")))
erosion_iteration_gawang = int(rw.read("setting/erosion_iteration_gawang.txt"))
gaussian_gawang = rw.odd(int(rw.read("setting/gaussian_gawang.txt")))
radius_gawang = int(rw.read("setting/radius_gawang.txt"))

erosion_kernel = cv.getStructuringElement(cv.MORPH_RECT, (erosion_gawang, erosion_gawang))
dilation_kernel = cv.getStructuringElement(cv.MORPH_RECT, (dilation_gawang, dilation_gawang))


def color_filter(frame):
    frame = cv.GaussianBlur(frame, (gaussian_gawang, gaussian_gawang), 0)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_white, upper_white)
    mask = cv.erode(mask, erosion_kernel, iterations=erosion_iteration_gawang)
    mask = cv.dilate(mask, dilation_kernel, iterations=dilation_iteration_gawang)
    result = cv.bitwise_and(frame, frame, mask=mask)
    return result


img = cv.imread("gambar/original_image.jpg", cv.COLOR_RGB2HSV)

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", type=int, default=0, help="change camera")
ap.add_argument("-d", "--display", type=int, default=1, help="Whether or not frame should be displayed")
args = ap.parse_args()

cv.namedWindow("trackbars", cv.WINDOW_NORMAL)
cv.resizeWindow("trackbars", 300, 500)
cv.createTrackbar("t1", "trackbars", int(rw.read("setting/canny_1.txt")), 2000,
                  lambda x: rw.write(x, "setting/canny_1.txt"))
cv.createTrackbar("t2", "trackbars", int(rw.read("setting/canny_2.txt")), 2000,
                  lambda x: rw.write(x, "setting/canny_2.txt"))

# cap = WebcamVideoStream(0).start()
cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        cap = cv.VideoCapture("gambar/reg3.mp4")
        continue
    frame = imutils.resize(frame, width=600)

    tinggi, panjang, _ = frame.shape

    filtered = color_filter(frame)

    t1 = int(rw.read("setting/canny_1.txt"))
    t2 = int(rw.read("setting/canny_2.txt"))
    edges = cv.Canny(filtered, t1, t2, apertureSize=5)

    lines = cv.HoughLines(edges, 12, np.pi / 180, 10)
    if lines is not None:
        '''for line in lines:
            x1,y1,x2,y2 = line[0]
            cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)'''
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    if args.display > 0:
        cv.imshow("result", frame)
        cv.imshow("edge", edges)
        cv.imshow("frame", filtered)

    key = cv.waitKey(25)
    if key == 27:
        break

cv.destroyAllWindows()
