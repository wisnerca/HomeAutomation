import RPi.GPIO as GPIO
import time
ratio = 0.35
cycleCount = 6
timestep = cyclecount * 1.0/60.0
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)

err = 0.0
while True:
#    ledState = not ledState
    curRatio = round((ratio+err) * cycleCount) / cycleCount
    err = ratio - curRatio
    print curRatio + " " + err
    GPIO.output(LED, True)
    time.sleep(curRatio * timestep)
    GPIO.output(LED, False)
    time.sleep((1-curRatio) * timestep)

