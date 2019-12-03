import cv2

def show_images(windows):
  for img in windows:
    cv2.imshow(img['name'], img['img'])

def draw_points(points, img):
  for point in points:
    cv2.circle(img, point['P'], 4, point['BGR'], -1)
