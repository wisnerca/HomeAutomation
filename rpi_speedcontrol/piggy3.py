#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import threading
import random
import signal

ratio = 0.59
timestep = 1.0/20.0
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)
#global ratio
#global accum
ratio = 0.5
accum = 0.0
GPIO.output(LED, True)
time.sleep(2)

exiti = False
def sigterm_handler(_signo, _stack_frame):
    exiti = True

def workerThread():
    global ratio
    global accum
    while True:
        val = False
        print ratio
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


t = threading.Thread(target=workerThread)
t.start()
while (exiti == False):
    x = str(raw_input("?"))
    if (x == "+"):
        ratioNew = ratio + 0.05
    elif (x == "-"):
        ratioNew = ratio - 0.05
    if (ratioNew >=0 and ratio <=1):
        ratio = ratioNew
    print ratio


