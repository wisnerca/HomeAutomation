#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 14
GPIO.setup(LED,GPIO.OUT)
switchtemp = 66
hyst = 2
timewait = 30
state = True

while True:
    humidity, temperature = Adafruit_DHT.read_retry(2302, 3)
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


