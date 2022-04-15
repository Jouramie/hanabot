from dataclasses import dataclass

import cv2
import numpy as np

image = cv2.imread("../resources/screenshots/smollur-first-turn.png")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# filtered = cv2.fastNlMeansDenoising(hsv, h=10, templateWindowSize=7, searchWindowSize=21)
# cv2.imwrite("../target/imread/1-filtered.png", filtered)


@dataclass(frozen=True)
class ColorBoundary:
    lower_bound: np.array
    upper_bound: np.array


play_mat = ColorBoundary(np.array([65, 100, 0]), np.array([70, 160, 255]))

mask = cv2.inRange(hsv, play_mat.lower_bound, play_mat.upper_bound)
cv2.imwrite("../../target/imread/2-mask.png", mask)
inv = cv2.bitwise_not(mask)
cv2.imwrite("../../target/imread/2-1-inv.png", inv)

contours = cv2.findContours(inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

min_area = 100000
image_number = 0
contour = sorted([contour for contour in contours if cv2.contourArea(contour) > min_area], key=lambda x: cv2.contourArea(x), reverse=True)[1]
x, y, w, h = cv2.boundingRect(contour)
card = image[y : y + h, x : x + w]
cv2.imwrite(f"../../target/imread/4-{image_number}.png", card)
cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)
image_number += 1

cv2.imwrite("../../target/imread/3-contour.png", image)
