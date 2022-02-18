#! /usr/local/bin/python3
#
# import the necessary packages
import numpy as np
import cv2
# draw a rectangle
rectangle = np.zeros((300, 300), dtype="uint8")
cv2.rectangle(rectangle, (25, 25), (275, 275), (255,0,0), -1)
cv2.imshow("Rectangle", rectangle)
# draw a circle
circle = np.zeros((300, 300), dtype = "uint8")
cv2.circle(circle, (150, 150), 150, (74,31,200), -1)
cv2.imshow("Circle", circle)

W=400
center = (W//2, W//2)
size = W, W, 3
atom_image = np.zeroes(size, dtype=np.uint8)
myradius = W//4
mycolor = (74,31,200)
thickness = cv2.FILLED
line_type = cv2.LINE_8

cv2.circle(atom_image,
          center,
          W // 4,
            mycolor,
          thickness,
          line_type)
cv2.imshow("Circle", atom_image)

while 1:
    if cv2.waitKey(25) == 27:
        break