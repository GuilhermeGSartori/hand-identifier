import math as m
import cv2
import time
import numpy as np

from .constants import *
from .output import *

# Calibration
def find_frame_hsv(frame, everyX, everyY, size, square_matriz):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    minH = 179; minS = 255; minV = 255
    maxH = 0; maxS = 0; maxV = 0
    for i in range(square_matriz**2):
        colorH = 0; colorS = 0; colorV = 0
        for j in range(size-1):
            for k in range(size-1):
                minH = min(int(hsv_frame[everyX[i]+j+1][everyY[i]+k+1][0]), minH)
                maxH = max(int(hsv_frame[everyX[i]+j+1][everyY[i]+k+1][0]), maxH)

                minS = min(int(hsv_frame[everyX[i]+j+1][everyY[i]+k+1][1]), minS)
                maxS = max(int(hsv_frame[everyX[i]+j+1][everyY[i]+k+1][1]), maxS)

                minV = min(int(hsv_frame[everyX[i]+j+1][everyY[i]+k+1][2]), minV)
                maxV = max(int(hsv_frame[everyX[i]+j+1][everyY[i]+k+1][2]), maxV)

    return tuple([minH, minS, minV]), tuple([maxH, maxS, maxV])

def get_skin_color():

    calibration = cv2.VideoCapture(0)
    timer = time.time()
    square_matriz = 3 # Odd number
    middle = m.ceil(square_matriz/2)
    middle -= 1

    while time.time() - timer < calibrationTime:
        check, frame = calibration.read()
        cv2.rectangle(frame, (X,Y), (deltaX,deltaY), BGR_GREEN, 2)
        roi = frame[Y:deltaY, X:deltaX]
        rows, cols, _ = roi.shape
        size = int(min(rows, cols)/CaptureSquareToRoi)
        diff = size

        midX = int(rows/2)
        midY = int(cols/2)
        startX = Y + int(middle*-diff + midX - size/2)
        startY = X + int(middle*-diff + midY - size/2)

        squaresX = []; squaresY = []
        for i in range(square_matriz):
            pX = startX
            pY = startY
            for j in range(square_matriz):
                squaresX.append(pX)
                squaresY.append(pY)
                pX = pX + size + diff
            startY = pY + size + diff

        getAreaRight = np.array(squaresX, dtype=np.uint32)
        getAreaTop = np.array(squaresY, dtype=np.uint32)
        getAreaLeft = getAreaRight + size
        getAreaBot = getAreaTop + size

        for i in range(square_matriz**2):
            cv2.rectangle(frame, (getAreaTop[i], getAreaRight[i]),
                                 (getAreaBot[i], getAreaLeft[i]),
                          BGR_RED, 1)

        key = cv2.waitKey(1) # Necessary to generate frame to show
        cv2.imshow('Calibration', frame)
        if calibrationTime/2 < time.time() - timer < calibrationTime - 0.5:
            frame = cv2.medianBlur(frame,5)
            min_hsv, max_hsv = find_frame_hsv(frame, getAreaRight, getAreaTop, size, square_matriz)
    calibration.release
    cv2.destroyAllWindows()
    print(min_hsv)
    print(max_hsv)
    return min_hsv, max_hsv

def set_skin_color(min, max):
    string = str(min[0]) + " " + str(min[1]) + " " + str(min[2]) + " "
    string += str(max[0]) + " " + str(max[1]) + " " + str(max[2])
    write_file(string)

def read_skin_color():
    numbers = []
    hsvString = read_file()
    numbers = list(map(int, hsvString.split(" ")))
    minHsv = [numbers[0], numbers[1], numbers[2]]
    maxHsv = [numbers[3], numbers[4], numbers[5]]
    return tuple(minHsv), tuple(maxHsv)
# End of Calibration


# Calculations
def  check_contour2(c1, c2):
    close = False

    M1 = cv2.moments(c1)
    M2 = cv2.moments(c2)
    try:
        c1X = int(M1['m10'] /M1['m00'])
        c1Y = int(M1['m01'] /M1['m00'])
        c2X = int(M2['m10'] /M2['m00'])
        c2Y = int(M2['m01'] /M2['m00'])
    except:
        return None
    diffX = abs(c1X - c2X)
    diffY = abs(c1Y - c2Y)

    if diffX < 70 and diffY < 70:
        close = True

    #close = True
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
# End of Calculations
