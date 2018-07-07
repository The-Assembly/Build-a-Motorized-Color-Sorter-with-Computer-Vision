import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cap = cv2.VideoCapture(0)
# create trackbars for color change
cv2.createTrackbar('H_high','image',0,180,nothing)
cv2.createTrackbar('H_low','image',0,180,nothing)
cv2.createTrackbar('S_high','image',0,255,nothing)
cv2.createTrackbar('S_low','image',0,255,nothing)
cv2.createTrackbar('V_high','image',0,255,nothing)
cv2.createTrackbar('V_low','image',0,255,nothing)



# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    _, frame = cap.read()
    
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    hh = cv2.getTrackbarPos('H_high','image')
    sh = cv2.getTrackbarPos('S_high','image')
    vh = cv2.getTrackbarPos('V_high','image')
    hl = cv2.getTrackbarPos('H_low','image')
    sl = cv2.getTrackbarPos('S_low','image')
    vl = cv2.getTrackbarPos('V_low','image')
    s = cv2.getTrackbarPos(switch,'image')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    upper = np.array([hh,sh,vh])
    lower = np.array([hl,sl,vl])
    mask = cv2.inRange(hsv, lower, upper)

    if s == 0:
        img[:] = 0
    else:
        img = mask

cv2.destroyAllWindows()
