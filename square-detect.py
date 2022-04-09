import cv2
import numpy as np

# Load image, grayscale, median blur, sharpen image
image = cv2.imread("test/resources/first-turn-3-players.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
denoise = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)
blur = cv2.medianBlur(denoise, 5)
sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

# Threshold and morph close
# thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
thresh = cv2.adaptiveThreshold(sharpen, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours and filter using threshold area
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 100
max_area = 1500
image_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if True or area > min_area and area < max_area:
        x, y, w, h = cv2.boundingRect(c)
        ROI = image[y : y + h, x : x + w]
        cv2.imwrite("target/result/ROI_{}.png".format(image_number), ROI)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        image_number += 1

cv2.imwrite("target/1-sharpen.png", sharpen)
cv2.imwrite("target/2-thresh.png", thresh)
cv2.imwrite("target/3-close.png", close)
cv2.imwrite("target/4-image.png", image)
cv2.waitKey()
