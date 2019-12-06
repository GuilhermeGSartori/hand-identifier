import cv2
import os

def show_images(windows):
  for img in windows:
    cv2.imshow(img['name'], img['img'])

def draw_points(points, img):
  for point in points:
    cv2.circle(img, point['P'], 4, point['BGR'], -1)

def write_file(data):
  pathname = os.path.join("support\\skin_data", "color.txt")
  file = open(pathname, "w")
  file.write(data)
  file.close()

def read_file():
  pathname = os.path.join("support\\skin_data", "color.txt")
  file = open(pathname, "r")
  string = file.readline()
  file.close()
  return string
