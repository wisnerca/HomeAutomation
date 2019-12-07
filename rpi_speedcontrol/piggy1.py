#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import random

ratio = 0.49
timestep = 1.0/10.0
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)
accum = 0.0

GPIO.output(LED, True)
time.sleep(4)

while True:
    val = False
    myrand = random.gauss(0, 0.025)
    if (accum < ratio):
        val = True
        accum = accum * 0.875 + 0.125 + myrand 
    else:
        val = False
        accum = accum * 0.875 + myrand
    print "      " + str(myrand) + " " + str(val) + " " + str(accum)
    GPIO.output(LED, val)
    time.sleep(timestep)

