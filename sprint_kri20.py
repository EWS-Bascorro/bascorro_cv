import argparse

import cv2 as cv

from program import Program


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-d', action='store_true')
    arg = parser.parse_args()

    program = Program()
    cap = program.init_cap()

    if arg.t:
        program.show_trackbars()

    ret = True
    cnt = 0
    while ret:
        ret, img = cap.read()
        if cnt > 10000:
            break
        cnt += 1
        yellow_mask, x_yellow, y_yellow = program.filter_color(img, 'YELLOW')
        print(cnt, x_yellow, y_yellow)


        if arg.d:
            cv.circle(img, (x_yellow, y_yellow), 5, (0, 255, 0), -1)
            cv.putText(img, f"x : {int(x_yellow)} y : {int(y_yellow)}", (10, 100 - 25),
                       cv.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (10, 255, 10))
            cv.imshow("image", img)
            cv.imshow("mask", yellow_mask)

        k = cv.waitKey(1) & 0xFF
        if k == 27:
            program._setting.write()
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
