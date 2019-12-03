#from constants import *
import math as m
import cv2

def  check_contour2(c1, c2):
    # close = False

    # M1 = cv2.moments(c1)
    # M2 = cv2.moments(c2)
    # try:
    #     c1X = int(M1['m10'] /M1['m00'])
    #     c1Y = int(M1['m01'] /M1['m00'])
    #     c2X = int(M2['m10'] /M2['m00'])
    #     c2Y = int(M2['m01'] /M2['m00'])
    # except:
    #     return None
    # diffX = abs(c1X - c2X)
    # diffY = abs(c1Y - c2Y)
    #
    # if diffX < 80 and diffY < 80:
    #     close = True

    close = True
    if close:
        points = []
        if c1[c1[:, :, 0].argmin()][0][0] > c2[c2[:, :, 0].argmin()][0][0]:
            points.append(tuple(c2[c2[:, :, 0].argmin()][0]))
        else:
            points.append(None)

        if c1[c1[:, :, 0].argmax()][0][0] < c2[c2[:, :, 0].argmax()][0][0]:
            points.append(tuple(c2[c2[:, :, 0].argmax()][0]))
        else:
            points.append(None)

        if c1[c1[:, :, 1].argmin()][0][1] > c2[c2[:, :, 1].argmin()][0][1]:
            points.append(tuple(c2[c2[:, :, 1].argmin()][0]))
        else:
            points.append(None)

        if c1[c1[:, :, 1].argmax()][0][1] < c2[c2[:, :, 1].argmax()][0][1]:
            points.append(tuple(c2[c2[:, :, 1].argmax()][0]))
        else:
            points.append(None)

    return points if close else None
