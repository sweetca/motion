import time
import RPi.GPIO as GPIO

class Sensor(object):

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.IN) # GP4 on pi3
        i = 1
        while i == 1:
            i = GPIO.input(7)

        time.sleep(5)    
        print "start sensor"

    def clean(self):
        GPIO.cleanup()
        print "stop sensor" 
   
    def status(self):
        return GPIO.input(7)