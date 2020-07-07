import RPi.GPIO as GPIO
import time
import sys
ratio = 0.75
timestep = 0.02
GPIO.setmode(GPIO.BCM)
LED = 27
ledState = True
GPIO.setup(LED,GPIO.OUT)
ratio = 1.0-float(sys.argv[1])
print ratio
while True:
#    ledState = not ledState
    GPIO.output(LED, True)
    time.sleep(ratio * timestep)
    GPIO.output(LED, False)
    time.sleep((1-ratio) * timestep)

