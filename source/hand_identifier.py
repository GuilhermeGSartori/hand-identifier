import cv2
#import cvlib as cv
import imutils
import numpy as np
from support.constants import *
from support.output import *
from support.calculations import *


video = cv2.VideoCapture(0)
images = []
points = []

while True:

    check, frame = video.read()

    # It is necessary to process only a specific area of the screen (where
    # the user will put his hand). In the future, the face recognition
    # will define the ROI
    roi = frame[Y:deltaY, X:deltaX]

    # draw ROI on original frame
    # ROI is still connected to the frame (modification on ROI change the frame)
    cv2.rectangle(frame, (X,Y), (deltaX,deltaY), BGR_GREEN, 2)

    # threshholding and dilate to better find the countours
    gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    (thresh, blackAndWhiteImage) = cv2.threshold(blur, 156, 255, cv2.THRESH_BINARY)
    processed_img = cv2.dilate(blackAndWhiteImage, None, iterations=2)
    processed_img = cv2.erode(processed_img, None, iterations=2)
    img = {'name': "filtered", 'img': processed_img}
    images.append(img)

    # Find edgemap
    edges = cv2.Canny(img_dilate, 150, 75, apertureSize = 3)
    img = {'name': "edges", 'img': edges}
    images.append(img)

    # Find the contours of the edgemap
    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)


    # If a countour was found
    if cnts:
        # Get the countour with the biggest area (presumed to be hand)
        cntsSorted = sorted(cnts, key=lambda x: cv2.arcLength(x, 0))
        c1 = cntsSorted[-1]
        cv2.drawContours(frame, [c1 + (X, Y)], -1, BGR_RED)

        # Find extreme points and draw them.
        left = {'P': tuple(c1[c1[:, :, 0].argmin()][0]), 'BGR': BGR_RED}
        right = {'P': tuple(c1[c1[:, :, 0].argmax()][0]), 'BGR': BGR_GREEN}
        top = {'P': tuple(c1[c1[:, :, 1].argmin()][0]), 'BGR': BGR_BLUE}
        bot = {'P': tuple(c1[c1[:, :, 1].argmax()][0]), 'BGR': BGR_CYAN}
        points.extend([left, right, top, bot])

        # If there is second biggest contour, consider it (most of times hand is
        # segmented in capture)
        if len(cntsSorted) > 1:
            c2 = cntsSorted[-2]
            new_P = check_contour2(c1, c2)
            # If second biggest contour is close to the first
            if new_P is not None:
                i = 0
                cv2.drawContours(frame, [c2 + (X, Y)], -1, BGR_BLUE)
                # Update points if one or more points of c2 are more extreme
                for i in range(4):
                    if new_P[i]: points[i]['P'] = new_P[i]

        draw_points(points, roi)

    img = {'name': "frame", 'img': frame}
    images.append(img)

    show_images(images)

    del images[:]
    del points[:]

    key = cv2.waitKey(1) # Wait 1 clock for user input
    if key == ESC:
        break

video.release
