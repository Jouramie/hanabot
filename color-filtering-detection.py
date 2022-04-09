import os

import cv2
import numpy as np

for filename in os.listdir("target"):
    file_path = f"target/{filename}"
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
    except Exception as e:
        print("Failed to delete %s. Reason: %s" % (file_path, e))


# Load image, grayscale, median blur, sharpen image
image = cv2.imread("test/resources/first-turn-3-players.png")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
filtered = cv2.fastNlMeansDenoising(hsv, h=10, templateWindowSize=7, searchWindowSize=21)

lower_red = np.array([0, 20, 100])
upper_red = np.array([20, 255, 255])
lower_blue = np.array([105, 20, 100])
upper_blue = np.array([110, 255, 255])
lower_purple = np.array([120, 20, 100])
upper_purple = np.array([140, 255, 255])
lower_yellow = np.array([30, 0, 0])
upper_yellow = np.array([50, 255, 255])
lower_green = np.array([50, 0, 0])
upper_green = np.array([60, 255, 255])


mask = cv2.inRange(filtered, lower_yellow, upper_yellow)

cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 1500
image_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > min_area:
        x, y, w, h = cv2.boundingRect(c)
        ROI = image[y : y + h, x : x + w]
        cv2.imwrite(f"target/result{image_number}.png", ROI)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        image_number += 1


cv2.imwrite("target/1-color-mask.png", mask)
