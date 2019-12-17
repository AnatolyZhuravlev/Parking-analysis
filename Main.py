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

# Создание пустого изоброжения для определения машин
blank_image_cars = np.zeros((1080, 1920, 3), np.uint8)

# Указываем границы HSV
hsv_min = np.array((0, 45, 5), np.uint8)
hsv_max = np.array((187, 255, 255), np.uint8)

# меняем цветовую модель с BGR на HSV
hsv = cv2.cvtColor(imgParkingFull, cv2.COLOR_BGR2HSV)
# применяем цветовой фильтр
thresh = cv2.inRange(hsv, hsv_min, hsv_max)
# Ищем контуры на изображении
contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# cv2.imshow("linesDetected", contours0)

boxArr = [];
# перебираем все найденные контуры в цикле
for cnt in contours0:
    # пытаемся вписать прямоугольник
    rect = cv2.minAreaRect(cnt)
    # поиск четырех вершин прямоугольника
    box = cv2.boxPoints(rect)
    # округление координат
    box = np.int0(box)
    # вычисление площади
    area = int(rect[1][0] * rect[1][1])
    if area > 10000:
        cv2.drawContours(blank_image_cars, [box], 0, (255, 255, 255), -1)
        cv2.drawContours(imgParkingFull, [box], 0, (0, 255, 0), 2)
        boxArr.append(box)

# Сохранение контуров машин и линий парковки
# cv2.imwrite("lines.jpg", blank_image_parking)
cv2.imwrite("cars.jpg", blank_image_cars)