import RPi.GPIO as GPIO   
from time import sleep 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
servo1 = 33

def SetAngle(servo,angle):  
    pwm=GPIO.PWM(servo, 50)  
    pwm.start(0)   
    duty = angle / 18 + 2
    GPIO.output(servo , True)  
    pwm.ChangeDutyCycle(duty)
    sleep(0.4)  
    pwm.stop()  

SetAngle(servo1, 90)  
SetAngle(servo1, 0)
GPIO.cleanup()  
