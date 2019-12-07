#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import random

ratio = 0.79
timestep = 1.0/20.0
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)
accum = 0.0

ratio = 0.5

GPIO.output(LED, True)
time.sleep(2)

while True:
    val = False
    myrand = random.gauss(0, 0.01)
    if (accum < ratio):
        val = True
        accum = accum * (1-ratio) + ratio + myrand 
    else:
        val = False
        accum = accum * ratio + myrand
#    print "      " + str(myrand) + " " + str(val) + " " + str(accum)
    GPIO.output(LED, val)
    time.sleep(timestep)

