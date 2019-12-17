import cv2
import numpy as np

# Считывание изображения пустой и полной парковки
imgParkingEmpty = cv2.imread("parking_lot_empty_01.png")
imgParkingFull = cv2.imread("parking_lot_full_01.png")

# Создание пустого изображения для определения линий парковки
blank_image_parking = np.zeros((1080, 1920, 3), np.uint8)

# перевод изображения в grayscale
gray = cv2.cvtColor(imgParkingEmpty, cv2.COLOR_BGR2GRAY)

# cv2.imwrite("test.jpg", gray)

# Определяем Edges при помощи алгоритма Canny
edges = cv2.Canny(gray, 120, 300)

# cv2.imwrite("test.jpg", edges)

# Определяем линнии с помощью функции HoughLines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)

# Рисуем линии парковки на пустом изображении
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(blank_image_parking, (x1, y1), (x2, y2), (255, 255, 255), 2)

cv2.imwrite("test.jpg", blank_image_parking)