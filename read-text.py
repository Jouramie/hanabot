# Import required packages
import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Read image from which text needs to be extracted
img = cv2.imread("test/ressources/first-turn-3-players.png")


# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
nonoise = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)
cv2.imwrite("nonoise.png", nonoise)

displayed = img.copy()

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(nonoise, 200, 255, cv2.THRESH_BINARY_INV)
# thresh1 = cv2.adaptiveThreshold(nonoise, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
cv2.imwrite("thresh.png", thresh1)
# text = pytesseract.image_to_string(nonoise)
boxes = pytesseract.image_to_boxes(nonoise)

hImg, wImg = nonoise.shape
for b in boxes.splitlines():
    b = b.split(" ")
    print(b)

    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
    cv2.putText(img, b[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)

cv2.imwrite("Detected text.png", img)
cv2.waitKey(0)
