import cv2
import numpy

cap = cv2.VideoCapture(0)
opened = cap.isOpened()
print opened
ret,frame = cap.read()
if frame is None:
    print type(frame)
