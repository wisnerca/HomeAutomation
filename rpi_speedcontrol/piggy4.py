#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import random
import sys


ratio = 0.33
timestep = 1.0/10.0
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)
accum = 0.0

ratio = 0.9
ratio = float(sys.argv[1])
print ratio

GPIO.output(LED, True)
time.sleep(2)

while True:
    val = False
    myrand = 0.0 #random.gauss(0, 0.01)
    if (accum < ratio):
        val = True
        accum = accum * (1-ratio) + ratio + myrand 
    else:
        val = False
        accum = accum * ratio + myrand
#    print "      " + str(myrand) + " " + str(val) + " " + str(accum)
    GPIO.output(LED, val)
    time.sleep(timestep)

