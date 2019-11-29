import RPi.GPIO as GPIO
import time
import random
GPIO.setmode(GPIO.BCM)
LED = 21
ledState = True
GPIO.setup(LED,GPIO.OUT)
while True:

    #ledState = not ledState
    r = random.random()
    GPIO.output(LED, r > 0.9)
    time.sleep(0.5)

