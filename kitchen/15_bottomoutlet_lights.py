import RPi.GPIO as GPIO
import time
import datetime
GPIO.setmode(GPIO.BCM)
LED = 15
ledState = True
GPIO.setup(LED,GPIO.OUT)

def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end


#https://stackoverflow.com/questions/20518122/python-working-out-if-time-now-is-between-two-times
while True:
    GPIO.output(LED, in_between(datetime.datetime.now().time(), datetime.time(22), datetime.time(10)) or in_between(datetime.datetime.now().time(), datetime.time(15, 30), datetime.time(16, 30)) )
    time.sleep(10)
