import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
while(1):
   # Take each frame
   _, frame = cap.read()
   # Convert BGR to HSV
   hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
   # define range of blue color in HSV
   lower_blue = np.array([110,50,50])
   upper_blue = np.array([130,255,255])
   # Threshold the HSV image to get only blue colors
   mask = cv.inRange(hsv, lower_blue, upper_blue)
   # Bitwise-AND mask and original image
   res = cv.bitwise_and(frame,frame, mask= mask)
   im2, contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
   cv.drawContours(frame,contours,-1,(255,255,0),3)

   cv.imshow('frame',frame)
   cv.imshow('mask',mask)
   cv.imshow('cnt',im2)
##   cv.imshow('res',res)
   k = cv.waitKey(5) & 0xFF
   if k == 27:
       break
cv.destroyAllWindows()
