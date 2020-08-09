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

ALLGPIOS = [OUTLET0, OUTLET1, OUTLET2, OUTLET3, OUTLET240, ACFAN0, ACFAN1, ACFAN2]

#https://realpython.com/intro-to-python-threading/
#https://stackoverflow.com/questions/20518122/python-working-out-if-time-now-is-between-two-times

GPIO_PINS = [OUTLET0, OUTLET1, OUTLET2, OUTLET3, OUTLET240]
#GPIO_TIMES = [ [[datetime.time(20), datetime.time(13)], [datetime.time(15, 30), datetime.time(16, 30)]] ]
#LIGHTTIMES1 = [[datetime.time(20), datetime.time(13)]]
LIGHTTIMES1 = [[datetime.time(18), datetime.time(13)]]
VENTTIMES1 = [[datetime.time(18), datetime.time(13)]]
PUMPTIMES1 = [[datetime.time(18), datetime.time(9)]]
GPIO_TIMES = [ LIGHTTIMES1, PUMPTIMES1, VENTTIMES1, LIGHTTIMES1, LIGHTTIMES1]




DCFAN_PIN = 18
DCFAN_TIMESTEP = 0.02
DCFAN_INIT_RATIO = 0.5
DCFAN_TIMES = [ [[datetime.time(21), datetime.time(12)]] ]
#FAN_TIMES = [GPIO_TIMES[0]]
DCFAN_RATIOS = [1.0, 0.5]


ACFANTIMES3 = [[datetime.time(23), datetime.time(11)]]
ACFANTIMES2 = []
ACFANTIMES1 = [[datetime.time(0, 0, 0), datetime.time(23, 59, 59, 999999)]]
ACFAN_TIMES = [ACFANTIMES3, ACFANTIMES2, ACFANTIMES1]

dcfan_ratio = DCFAN_INIT_RATIO
acfanval = 0

keeprunning = True

def exit_signal(signum, frame):
    global keeprunning
    keeprunning = False

def setacfan(val):
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

def thread_times():
    global dcfan_ratio
    global keeprunning
    while keeprunning:
        for i in range(len(GPIO_PINS)):
            newval = GPIO.LOW  if in_time_ranges(GPIO_TIMES[i]) else GPIO.HIGH
            GPIO.output(GPIO_PINS[i], newval)
            #print newval
        
        #do DC fan stuff
        xdcfan_ratio = dcfan_ratio
        for i in range(len(DCFAN_RATIOS)):
            j = len(DCFAN_RATIOS)-i-1
            if (j >= len(DCFAN_TIMES)):
                xdcfan_ratio = DCFAN_RATIOS[j]
            else:
                if (in_time_ranges(DCFAN_TIMES[j])):
                    xdcfan_ratio = DCFAN_RATIOS[j]
        dcfan_ratio = xdcfan_ratio
            
        if (in_time_ranges(ACFAN_TIMES[0])):
            setacfan(3)
        elif (in_time_ranges(ACFAN_TIMES[1])):
            setacfan(2)
        elif (in_time_ranges(ACFAN_TIMES[1])):
            setacfan(1)
        else: 
            setacfan(0)
        time.sleep(10)
    for pin in ALLGPIOS:
        GPIO.output(pin, True)


def dcthread_fan():
    global dcfan_ratio
    global keeprunning
    while keeprunning:
        if (dcfan_ratio > 0):
            GPIO.output(DCFAN_PIN, False)
            time.sleep(dcfan_ratio * DCFAN_TIMESTEP)
        else:
            time.sleep(DCFAN_TIMESTEP)
        
        if (dcfan_ratio < 1):
            GPIO.output(DCFAN_PIN, True)
            time.sleep((1.0-dcfan_ratio) * DCFAN_TIMESTEP)
        else:
            time.sleep(DCFAN_TIMESTEP)
    GPIO.output(DCFAN_PIN, True)
        

if __name__ == '__main__':
    global keeprunning
    #https://gist.github.com/ruedesign/5218221
    signal.signal(signal.SIGINT, exit_signal)
    signal.signal(signal.SIGTERM, exit_signal)

    GPIO.setmode(GPIO.BCM)
    for pin in ALLGPIOS:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, True)

    GPIO.setup(DCFAN_PIN,GPIO.OUT)

    timesthread = threading.Thread(target=thread_times)
    dcfanthread = threading.Thread(target=dcthread_fan)

    timesthread.start()
    dcfanthread.start()

    while timesthread.isAlive and dcfanthread.isAlive and keeprunning:
        try:
            time.sleep(1)
            # synchronization timeout of threads kill
            #[t.join(1) for t in threads
            # if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            # Ctrl-C handling and send kill to threads
            keeprunning = False

