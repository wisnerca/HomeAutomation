#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 15
GPIO.setup(LED,GPIO.OUT)
switchtemp = 77
hyst = 1.5
timewait = 10
state = True

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    fahrenheit = (temperature * 1.8) + 32
    print 'Temp: {0:0.1f} F  Humidity: {1:0.1f} %'.format(fahrenheit, humidity)
    oldstate = state
    if (state):
        if (fahrenheit <= switchtemp + hyst/2):
            state = False
        else:
            state = True
    else:
        if (fahrenheit <= switchtemp - hyst/2):
            state = False
        else:
            state = True
    if (state != oldstate):
        print "waiting " + str(timewait) + " seconds"
        time.sleep(timewait)
    else:
        GPIO.output(LED, state)
    print state


