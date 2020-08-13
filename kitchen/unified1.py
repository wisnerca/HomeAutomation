import RPi.GPIO as GPIO
import time
import datetime
import threading
import signal

global keeprunning
keeprunning = True

OUTLET0 = 2     #Lights
OUTLET1 = 3     #Air pump
ACFAN0 = 4      
ACFAN1 = 14     
ACFAN2 = 15     
OUTLET2 = 17    #Vent fan
OUTLET3 = 27    #Water pump
OUTLET240 = 20  #Lights

DCFAN1 = 21     #DC fan PWM

ALLGPIOS = [OUTLET0, OUTLET1, OUTLET2, OUTLET3, OUTLET240, ACFAN0, ACFAN1, ACFAN2]

#https://realpython.com/intro-to-python-threading/
#https://stackoverflow.com/questions/20518122/python-working-out-if-time-now-is-between-two-times

GPIO_PINS = [OUTLET0, OUTLET1, OUTLET2, OUTLET3, OUTLET240]
#GPIO_TIMES = [ [[datetime.time(20), datetime.time(13)], [datetime.time(15, 30), datetime.time(16, 30)]] ]
#LIGHTTIMES1 =  [[datetime.time(20), datetime.time(13)]]
LIGHTTIMES1 =   [[datetime.time(19), datetime.time(12)]]
VENTTIMES1 =    [[datetime.time(19), datetime.time(13)]]
PUMPTIMES1 =    [[datetime.time(18), datetime.time(9)]]
EBBFLOWTIMES1 = [[datetime.time(21), datetime.time(21,20)], [datetime.time(1,45), datetime.time(2,5)], [datetime.time(7), datetime.time(7,20)], [datetime.time(14), datetime.time(14,20)]]   

GPIO_TIMES = [ LIGHTTIMES1, PUMPTIMES1, VENTTIMES1, EBBFLOWTIMES1, LIGHTTIMES1]




DCFAN_PINS = [18, 21]
DCFAN_TIMESTEP = 0.02
DCFAN_INIT_RATIO = 0.5
#DCFAN_TIMES = [ [[[datetime.time(21), datetime.time(12)]]], [[[datetime.time(0, 0, 0), datetime.time(23, 59, 59, 999999)]]]]
DCFAN_TIMES = [ [[[datetime.time(21), datetime.time(12)]]], [LIGHTTIMES1]]
#FAN_TIMES = [GPIO_TIMES[0]]
DCFAN_RATIOS = [[0.5, 0.3], [0.3, 0]]


#ACFANTIMES1 = [[datetime.time(23), datetime.time(11)]]
ACFANTIMES3 = [[datetime.time(3), datetime.time(11)]]
ACFANTIMES1 = [[datetime.time(0, 0, 0), datetime.time(23, 59, 59, 999999)]]
ACFANTIMES2 = LIGHTTIMES1
ACFAN_TIMES = [ACFANTIMES3, ACFANTIMES2, ACFANTIMES1]

dcfan_ratios = [DCFAN_INIT_RATIO, DCFAN_INIT_RATIO]
acfanval = 0

keeprunning = True

def exit_signal(signum, frame):
    global keeprunning
    keeprunning = False

def setacfan(val):
    #print val
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
        for k in range(len(DCFAN_PINS)):
            xdcfan_ratio = dcfan_ratios[k]
            for i in range(len(DCFAN_RATIOS[k])):
                j = len(DCFAN_RATIOS[k])-i-1
                if (j >= len(DCFAN_TIMES[k])):
                    xdcfan_ratio = (DCFAN_RATIOS[k])[j]
                else:
                    if (in_time_ranges(DCFAN_TIMES[k][j])):
                        xdcfan_ratio = DCFAN_RATIOS[k][j]
            dcfan_ratios[k] = xdcfan_ratio
            
        if (in_time_ranges(ACFAN_TIMES[0])):
            setacfan(3)
        elif (in_time_ranges(ACFAN_TIMES[1])):
            setacfan(2)
        elif (in_time_ranges(ACFAN_TIMES[2])):
            setacfan(1)
        else: 
            setacfan(0)
        time.sleep(10)
    for pin in ALLGPIOS:
        GPIO.output(pin, True)


def dcthread_fan(fannum):
    global dcfan_ratios
    global keeprunning
    while keeprunning:
        if (dcfan_ratios[fannum] > 0):
            GPIO.output(DCFAN_PINS[fannum], False)
            time.sleep(dcfan_ratios[fannum] * DCFAN_TIMESTEP)
        else:
            time.sleep(DCFAN_TIMESTEP)
        
        if (dcfan_ratios[fannum] < 1):
            GPIO.output(DCFAN_PINS[fannum], True)
            time.sleep((1.0-dcfan_ratios[fannum]) * DCFAN_TIMESTEP)
        else:
            time.sleep(DCFAN_TIMESTEP)
    GPIO.output(DCFAN_PINS[fannum], True)
        

if __name__ == '__main__':
    #https://gist.github.com/ruedesign/5218221
    signal.signal(signal.SIGINT, exit_signal)
    signal.signal(signal.SIGTERM, exit_signal)

    GPIO.setmode(GPIO.BCM)
    for pin in ALLGPIOS:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, True)

    for pin in DCFAN_PINS:
        GPIO.setup(pin,GPIO.OUT)

    timesthread = threading.Thread(target=thread_times)
    dcfanthreads = []

    for i in range(len(DCFAN_PINS)):
            dcfanthreads.append(threading.Thread(target=dcthread_fan, args=[i]))
            dcfanthreads[i].start()
#    dcfanthread = threading.Thread(target=dcthread_fan)

    timesthread.start()
#    dcfanthread.start()

    while keeprunning:
        try:
            time.sleep(1)
            # synchronization timeout of threads kill
            #[t.join(1) for t in threads
            # if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            # Ctrl-C handling and send kill to threads
            keeprunning = False

