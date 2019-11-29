#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 21
GPIO.setup(LED,GPIO.OUT)
#state = True

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    if (temperature >= 28):
        GPIO.output(LED, False)
    else:
        GPIO.output(LED, True)




