# Import required packages
import cv2
import numpy as np
import pytesseract

# https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
# https://www.topcoder.com/thrive/articles/python-for-character-recognition-tesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Read image from which text needs to be extracted
image = cv2.imread("../../target/blue-0.png")


# Convert the image to gray scale
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
filtered = cv2.fastNlMeansDenoising(hsv, h=10, templateWindowSize=7, searchWindowSize=21)
cv2.imwrite("../../target/imread/1-filtered.png", filtered)

lower, upper = np.array([20, 200, 0]), np.array([200, 255, 255])

# ret, thresh1 = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY_INV)

mask = cv2.inRange(filtered, lower, upper)
cv2.imwrite("../../target/imread/2-mask.png", mask)
cv2.imwrite("../../target/imread/2-1-inv.png", cv2.bitwise_not(mask))
boxes = pytesseract.image_to_boxes(cv2.bitwise_not(mask))
print(pytesseract.image_to_string(cv2.bitwise_not(mask)))


hImg, wImg, _ = image.shape
for b in boxes.splitlines():
    b = b.split(" ")
    print(b)

    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(image, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
    cv2.putText(image, b[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)

cv2.imwrite("../../target/imread/3-detected-text.png", image)
