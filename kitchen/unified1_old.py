import RPi.GPIO as GPIO
import time
import datetime
import threading

#https://realpython.com/intro-to-python-threading/
#https://stackoverflow.com/questions/20518122/python-working-out-if-time-now-is-between-two-times

GPIO_PINS = [15]
GPIO_TIMES = [ [[datetime.time(22), datetime.time(10)], [datetime.time(15, 30), datetime.time(16, 30)]] ]

FAN_PIN = 27
FAN_TIMESTEP = 0.02
FAN_INIT_RATIO = 0.5
FAN_TIMES = [ [[datetime.time(22), datetime.time(10)], [datetime.time(15, 30), datetime.time(16, 30)]], [[datetime.time(00, 00, 00), datetime.time(23, 59, 59)]] ]
FAN_RATIOS = [1.0, 0.3]

fan_ratio = FAN_INIT_RATIO

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

def thread_times():
    global fan_ratio
    while True:
        for i in range(len(GPIO_PINS)):
            newval = in_time_ranges(GPIO_TIMES[i])
            GPIO.output(GPIO_PINS[i], newval)
            print newval
        for i in range(len(FAN_RATIOS)):
            j = len(FAN_RATIOS)-i-1
            if (in_time_ranges(FAN_TIMES[j])):
                fan_ratio = FAN_RATIOS[j]
        time.sleep(10)


def thread_fan():
    global fan_ratio
    while True:
        if (fan_ratio > 0):
            GPIO.output(FAN_PIN, False)
            time.sleep(fan_ratio * FAN_TIMESTEP)
        else:
            time.sleep(FAN_TIMESTEP)
        
        if (fan_ratio < 1):
            GPIO.output(FAN_PIN, True)
            time.sleep((1.0-fan_ratio) * FAN_TIMESTEP)
        else:
            time.sleep(FAN_TIMESTEP)
        


GPIO.setmode(GPIO.BCM)
for pin in GPIO_PINS:
    GPIO.setup(pin,GPIO.OUT)

GPIO.setup(FAN_PIN,GPIO.OUT)

timesthread = threading.Thread(target=thread_times)
fanthread = threading.Thread(target=thread_fan)

timesthread.start()
fanthread.start()