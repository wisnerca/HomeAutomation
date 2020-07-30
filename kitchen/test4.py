import RPi.GPIO as GPIO
import time
import datetime
import threading
import signal


R4 = 27
R1 = 22
R2 = 23
R3 = 17


def setup():
    GPIO.setmode(GPIO.BCM)    # Number GPIOs by its physical locationS
    GPIO.setup(R4,GPIO.OUT)
    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.output(R4, GPIO.LOW)
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)
    GPIO.output(R3, GPIO.LOW)

def setfan(val):
    if (val == 0):
        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.LOW)
    if (val == 1):
        GPIO.output(R1, GPIO.HIGH)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.LOW)
    if (val == 2):
        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.HIGH)
        GPIO.output(R3, GPIO.LOW)
    if (val == 3):
        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.HIGH)
        GPIO.output(R3, GPIO.HIGH)


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