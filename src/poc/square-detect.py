from dataclasses import dataclass

import cv2
import numpy as np

# Load image, grayscale, median blur, sharpen image
image = cv2.imread("../../target/red-3.png")

border = 4
upper_crop = 24
cropped = image[border + upper_crop : -border - upper_crop, border:-border]

# Convert the image to gray scale
hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
filtered = cv2.fastNlMeansDenoising(hsv, h=10, templateWindowSize=7, searchWindowSize=21)
cv2.imwrite("../../target/imread/1-filtered.png", filtered)


@dataclass(frozen=True)
class ColorBoundary:
    color: str
    lower_bound: np.array
    upper_bound: np.array


red = ColorBoundary("red", np.array([0, 200, 100]), np.array([20, 255, 255]))
blue = ColorBoundary("blue", np.array([20, 200, 0]), np.array([200, 255, 255]))
purple = ColorBoundary("purple", np.array([120, 200, 100]), np.array([140, 255, 255]))
yellow = ColorBoundary("yellow", np.array([0, 0, 0]), np.array([255, 150, 255]))
green = ColorBoundary("green", np.array([50, 200, 0]), np.array([60, 255, 220]))

boundary = red

mask = cv2.inRange(filtered, boundary.lower_bound, boundary.upper_bound)
cv2.imwrite("../../target/imread/2-mask.png", mask)
inv = cv2.bitwise_not(mask)
cv2.imwrite("../../target/imread/2-1-inv.png", inv)

cnts = cv2.findContours(inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 100
max_area = 1000
image_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if min_area < area < max_area:
        x, y, w, h = cv2.boundingRect(c)
        card = image[y : y + h, x : x + w]
        cv2.rectangle(image, (x + border, y + border + upper_crop), (x + w + border, y + h + border + upper_crop), (0, 0, 0), 2)
        image_number += 1

cv2.imwrite("../../target/imread/3-contour.png", image)
print(f"This card is {boundary.color} {image_number}")
