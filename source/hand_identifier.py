import cv2
#import cvlib as cv
import imutils
import numpy as np
from support.constants import *
from support.output import *


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
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    img_dilate = cv2.dilate(blackAndWhiteImage, None, iterations=2)
    img_dilate = cv2.erode(img_dilate, None, iterations=2)
    img = {'name': "filtered", 'img': img_dilate}
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
        c = max(cnts, key=cv2.contourArea)
        cv2.drawContours(frame, [c + (X, Y)], -1, (0, 0, 255))
        # Find extreme points and draw them.
        left = {'point': tuple(c[c[:, :, 0].argmin()][0]), 'color': BGR_RED}
        right = {'point': tuple(c[c[:, :, 0].argmax()][0]), 'color': BGR_GREEN}
        top = {'point': tuple(c[c[:, :, 1].argmin()][0]), 'color': BGR_BLUE}
        bot = {'point': tuple(c[c[:, :, 1].argmax()][0]), 'color': BGR_CYAN}
        points.extend([left, right, top, bot])
        draw_points(points, roi)

        # necessary to get only countours with SIMILAR area
        # only if repeat a lot change the countour
        # sum of biggest and close contours?
        # hand should be alingned with the head (YZ)
        # hand should fill up the processing space

    img = {'name': "frame", 'img': frame}
    images.append(img)

    show_images(images)

    del images[:]
    del points[:]

    key = cv2.waitKey(1)
    if key == ESC: # exit on ESC
        break

video.release(0)
