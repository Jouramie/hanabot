import os
from dataclasses import dataclass

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


@dataclass(frozen=True)
class ColorBoundary:
    color: str
    lower_bound: np.array
    upper_bound: np.array


color_boundaries = [
    ColorBoundary("red", np.array([0, 20, 100]), np.array([20, 255, 255])),
    ColorBoundary("blue", np.array([105, 20, 100]), np.array([110, 255, 255])),
    ColorBoundary("purple", np.array([120, 40, 100]), np.array([140, 255, 255])),
    ColorBoundary("yellow", np.array([30, 120, 100]), np.array([50, 200, 200])),
    ColorBoundary("green", np.array([50, 0, 0]), np.array([60, 255, 220]))
]

total_card = 0


def find_cards(color_boundary: ColorBoundary):
    global total_card
    print(f"Finding card of the {color_boundary.color} suit.")

    mask = cv2.inRange(filtered, color_boundary.lower_bound, color_boundary.upper_bound)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = 1500
    image_number = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(c)
            card = image[y : y + h, x : x + w]
            cv2.imwrite(f"target/{color_boundary.color}-{image_number}.png", card)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
            image_number += 1

    cv2.imwrite(f"target/1-{color_boundary.color}-color-mask.png", mask)
    print(f"Found {image_number - 1} {color_boundary.color} cards.")

    total_card += image_number - 1


for color in color_boundaries:
    find_cards(color)

print(f"Found {total_card} cards in total.")

