# packages
import argparse
import cv2
#import cvlib as cv
import imutils
import numpy as np
import sys

# files
from support.constants import *
from support.output import *
from support.auxiliar import *
from support.player_ctrl.control import *
from support.gestures import GestureType


# Script Start:
# Contract:

# 'set' to save your skin color hsv in the "color.txt" file
# 'get' to get the skin color hsv in the "color.txt" file
parser = argparse.ArgumentParser(description='Receive mode')
parser.add_argument('-s', '--skin', required=True, type=str, help='get skin color?')
args = parser.parse_args()

if 'set' in args.skin:
    minHsv, maxHsv = get_skin_color()
    set_skin_color(minHsv, maxHsv)
elif 'get' in args.skin:
    minHsv, maxHsv = read_skin_color()
    if minHsv is None or maxHsv is None:
        print("Skin color not defined! Color necessary to track hand!")
        sys.exit()
else:
    sys.exit()

video = cv2.VideoCapture(0)
images = []
points = []
gesture = 0
commandReady = False

while True:

    check, frame = video.read()

    # Get only a specific area of the screen (user will put his hand) to process
    # In the future, the face recognition will define the ROI
    roi = frame[Y:deltaY, X:deltaX]

    # Draw ROI on original frame (changes on ROI changes the frame)
    cv2.rectangle(frame, (X,Y), (deltaX,deltaY), BGR_GREEN, 2)

    # Get mask using skin hsv, dilate, erode, blur and apply mask
    HSVframe = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(HSVframe, minHsv, maxHsv)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    mask = cv2.dilate(mask, kernel, iterations = 2)
    mask = cv2.erode(mask, kernel, iterations = 2)
    blur = cv2.GaussianBlur(mask, (7, 7), 0)
    blur = cv2.bilateralFilter(blur,9,75,75)
    skin = cv2.bitwise_and(roi, roi, mask = blur)
    img = {'name': "skin", 'img': np.hstack([roi, skin])}
    images.append(img)

    # Get V value of image with mask (greyscale)
    h, s, v = cv2.split(skin)
    img = {'name': "filtered", 'img': skin}
    images.append(img)

    # Threshold and Dilate image with mask applied to better find the countours
    (thresh, blackAndWhiteImage) = cv2.threshold(v, 100, 255, cv2.THRESH_BINARY)
    processed_img = cv2.dilate(blackAndWhiteImage, None, iterations=2)
    processed_img = cv2.erode(processed_img, None, iterations=2)
    img = {'name': "filtered", 'img': processed_img}
    images.append(img)

    # Find edgemap
    edges = cv2.Canny(processed_img, 150, 150, apertureSize = 3)
    img = {'name': "edges", 'img': edges}
    images.append(img)

    # Find the contours of the edgemap
    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    # Mask to mill small contours
    mask_small_c = np.ones(edges.shape[:2], dtype="uint8") * 255
    # If a countour was found
    if cnts:
        for x in cnts:
            # If contour does not have the necessary size
            if cv2.arcLength(x, True) < edgeLimitSize:
                # Draw contour on mask
                cv2.drawContours(mask_small_c, [x], -1, 0, -1)
        # Applies mask
        edges = cv2.bitwise_and(edges, edges, mask=mask_small_c)

        contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(contours)
        img = {'name': "edges_filter", 'img': edges}
        images.append(img)

    # If a countour was still found
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

        frameGesture = check_gesture(points)
        if frameGesture != gesture:
            gesture = frameGesture
            gestureCounter = 0
        else:
            gestureCounter += 1
            if gestureCounter == 30 and frameGesture != GestureType.NONE:
                gestureCounter = 0
                if frameGesture == GestureType.OPEN:
                    commandReady = True
                    print("ready for new gesture!")
                elif commandReady:
                    control = send_gesture(frameGesture)
                    control()
                    commandReady = False

    img = {'name': "frame", 'img': frame}
    images.append(img)

    show_images(images)

    del images[:]
    del points[:]

    key = cv2.waitKey(1) # Wait 1 clock for user input
    if key == ESC:
        break

video.release
