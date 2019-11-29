import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)
while True:
    ledState = not ledState
    time.sleep(1.0/60)
    GPIO.output(LED, ledState)

