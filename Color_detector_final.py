import cv2 as cv
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
prev_detection = 0
servo1 = 35
servo2 = 33
def prev_pred(prev):
    global prev_detection
    prev_detection = prev
class Box:
    def __init__(self):
        self.isDetected = False
        self.color = None
        self.cnt = 0

    def proccess(self, img, color):
        _, self.contours, self.hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        self.contour_sizes = [(cv.contourArea(contour), contour) for contour in self.contours]
        if not len(self.contour_sizes) == 0:
            self.biggest_contour = max(self.contour_sizes, key=lambda x: x[0])[1]
            if cv.contourArea(self.biggest_contour) > 400:
                self.isDetected = True
                self.cnt = self.biggest_contour
                self.color = color
            else:
                self.isDetected = False

    def drawBox(self,frame):
        if self.isDetected == True:
            x,y,w,h = cv.boundingRect(self.cnt)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv.putText(frame,self.color,(x,y), font, 2,(0,0,255),2,cv.LINE_AA)
        else: 
            x,y,w,h = 0,0,0,0
def findBoxes(frame):
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    blue_mask = cv.inRange(hsv, lower_blue, upper_blue)
##    cv.imshow('Blue',blue_mask)
    yellow_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
##    cv.imshow('Yellow',yellow_mask)
    red_mask = cv.inRange(hsv, lower_red, upper_red)
##    cv.imshow('Red',red_mask)
    box_b.proccess(blue_mask,"Blue")
    box_y.proccess(yellow_mask,"Yellow") 
    box_r.proccess(red_mask, "Red")
    box_b.drawBox(frame)
    box_y.drawBox(frame)
    box_r.drawBox(frame)
def setAngle(servo,angle):

    pwm=GPIO.PWM(servo, 50)
    pwm.start(2)
    duty = angle / 18 + 2
    GPIO.output(servo , True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.4)
    pwm.stop()
##    print("setting servo")
   
def pushTo(angle):
    setAngle(servo2,angle)
    print("Servo at: " + str(angle))
    setAngle(servo1,90)
    sleep(1)
    setAngle(servo1,0)
def push():
    
    if box_b.isDetected:
        if (prev_detection == "Not Detected"):
            print("Blue Detected")
            pushTo(60)
            prev_pred("Blue Detected")
                
    elif box_r.isDetected:
        if (prev_detection == "Not Detected"):
            print("Red Detected")
            pushTo(120)
            prev_pred("Red Detected")
        
    elif box_y.isDetected:
        if (prev_detection == "Not Detected"):
            print("Yellow Detected")
            pushTo(180)
            prev_pred("Yellow Detected")
        
    else:
        print("Not Detected")
        prev_pred("Not Detected")

def main():
    cap = cv.VideoCapture(0)
    while(1):
        _, frame = cap.read() 
        findBoxes(frame)
        push()
     
        cv.imshow('frame',frame)
        
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    cv.destroyAllWindows() 
if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(33, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
    
    box_b = Box()
    box_y = Box()
    box_r = Box()
    
    main()

