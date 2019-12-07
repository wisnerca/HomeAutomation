#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import threading
import signal

speeds = [ 0.0 ] * 16
pins   = [ 0 ] * 16
stop = False


def main():
    GPIO.setmode(GPIO.BCM)
    LED = 15
    GPIO.setup(LED,GPIO.OUT)
    switchtemp = 77
    hyst = 1.5
    timewait = 10
    state = True
    state1 = True


def sigterm_handler(_signo, _stack_frame):
    stop = True
    # Raises SystemExit(0):
    sys.exit(0)

def (int num):
    laststate = False
    while True:
        if (state1):
            while (state1):
                    GPIO.output(LED, True)
                    time.sleep(ratio * timestep)
                    GPIO.output(LED, False)
                    time.sleep((1-ratio) * timestep)
            laststate = True
        else: 
                GPIO.output(LED, False)
                laststate = False

ratio = 0.75
timestep = 0.1
GPIO.output(LED, False)
t = threading.Thread(target=doStuff)
t.start()


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
        state1 = state
    print state


