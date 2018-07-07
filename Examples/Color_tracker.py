import cv2 as cv
import numpy as np

class Box:
    def __init__(self):
        self.isDetected = False
        self.color = None
        self.cnt = 0


    def process(self, img, color):
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


    def drawBox(self,frame,cc):
        if self.isDetected == True:
            x,y,w,h = cv.boundingRect(self.cnt)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.rectangle(frame,(x,y),(x+w,y+h),cc,2)
            cv.putText(frame,self.color,(x,y), font, 2,cc,2,cv.LINE_AA)
        else:
            x,y,w,h = 0,0,0,0

def findBoxes(frame):
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])

    yellow_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
    # cv.imshow('Yellow',yellow_mask)

    box_y.process(yellow_mask,"Yellow")

    box_y.drawBox(frame,(0,255,255))


def main():
    cap = cv.VideoCapture(0)
    while(1):

        _, frame = cap.read()

        findBoxes(frame)
        # push()

        cv.imshow('frame',frame)

        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    cv.destroyAllWindows()

if __name__ == "__main__":

    box_y = Box()

    main()
