import RPi.GPIO as GPIO
import time
import datetime
import threading
import signal


OUTLET0 = 2
OUTLET1 = 3
ACFAN0 = 4
ACFAN1 = 14
ACFAN2 = 15
OUTLET2 = 17
OUTLET3 = 27
OUTLET240 = 22

RELAYS = [OUTLET0, OUTLET1, ACFAN0, ACFAN1, ACFAN2, OUTLET2, OUTLET3, OUTLET240]
INITIALSTATE = [GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]


def setup():
    GPIO.setmode(GPIO.BCM)    # Number GPIOs by its physical locationS
    for pin in RELAYS:
        GPIO.setup(pin,GPIO.OUT)
    for i in range(0, len(RELAYS)):
        GPIO.output(RELAYS[i], INITIALSTATE[i])

def setfan(val):
    if (val == 3):
        GPIO.output(ACFAN0, GPIO.HIGH)
        GPIO.output(ACFAN1, GPIO.HIGH)
        GPIO.output(ACFAN2, GPIO.HIGH)
    if (val == 0):
        GPIO.output(ACFAN0, GPIO.LOW)
        GPIO.output(ACFAN1, GPIO.HIGH)
        GPIO.output(ACFAN2, GPIO.HIGH)
    if (val == 2):
        GPIO.output(ACFAN0, GPIO.HIGH)
        GPIO.output(ACFAN1, GPIO.LOW)
        GPIO.output(ACFAN2, GPIO.HIGH)
    if (val == 1):
        GPIO.output(ACFAN0, GPIO.HIGH)
        GPIO.output(ACFAN1, GPIO.LOW)
        GPIO.output(ACFAN2, GPIO.LOW)


def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end

def in_time_ranges(times):
    now = datetime.datetime.now().time()
    ison = False
    for x in times:
        start = x[0]
        end = x[1]
        if start <= end:
            ison = ison or (start <= now < end)
        else: # over midnight e.g., 23:30-04:15
            ison = ison or (start <= now or now < end)
    return ison



if __name__ == '__main__':
    # signal.signal(signal.SIGINT, exit_signal)
    # signal.signal(signal.SIGTERM, exit_signal)
    
    setup()
    #    time.sleep(0.1)


#hc595_in(0x00); hc595_out()