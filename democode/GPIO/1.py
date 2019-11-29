import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)

#ledState = not ledState
GPIO.output(LED, ledState)

