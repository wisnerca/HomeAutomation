import RPi.GPIO as GPIO
import time
import datetime
import threading
import signal

PINS = [2]


def setup():
    GPIO.setmode(GPIO.BCM)    # Number GPIOs by its physical locationS
    for pin in PINS:
        GPIO.setup(pin,GPIO.OUT)
    for i in range(0, len(PINS)):
        GPIO.output(PINS[i], GPIO.LOW)

setup()
