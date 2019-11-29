import RPi.GPIO as GPIO
import time
ratio = 0.75
timestep = 1.0/5.0
GPIO.setmode(GPIO.BCM)
LED = 14
ledState = True
GPIO.setup(LED,GPIO.OUT)
while True:
#    ledState = not ledState
    GPIO.output(LED, True)
    time.sleep(ratio * timestep)
    GPIO.output(LED, False)
    time.sleep((1-ratio) * timestep)

