import RPi.GPIO as GPIO
import time
import sys
ratio = 0.75
timestep = 0.1
GPIO.setmode(GPIO.BCM)
LED = 14
ledState = True
GPIO.setup(LED,GPIO.OUT)
ratio = float(sys.argv[1])
print ratio
while True:
#    ledState = not ledState
    GPIO.output(LED, True)
    time.sleep(ratio * timestep)
    GPIO.output(LED, False)
    time.sleep((1-ratio) * timestep)

