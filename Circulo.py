import cv2
import numpy as np


def circulo(mask, img):
    output = img.copy()
    print output.shape[1]/8
    gray =cv2.cvtColor(output,cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    # circles = np.uint16(np.around(circles))
    print circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    cv2.imshow('resultado', output)
    cv2.imshow('original', img)


# img = cv2.imread("C:\\Users\\Jorge\\Downloads\\FHD0003.JPG")
img = cv2.imread("C:\\Users\\Jorge\\Downloads\\18-19-19.jpg")
img = cv2.resize(img, (300, 240))
# cv2.imshow('image', img+3)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
azul_bajo = np.array([100,65,75])
azul_alto = np.array([130,255,255])
mask=cv2.inRange(img,azul_bajo,azul_alto)
circulo(gray, img)

tecla = cv2.waitKey(0) & 0xFF
if tecla == 27:
    cv2.destroyAllWindows()
