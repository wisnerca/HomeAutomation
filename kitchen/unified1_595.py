import RPi.GPIO as GPIO
import time
import datetime
import threading
import signal


#https://realpython.com/intro-to-python-threading/
#https://stackoverflow.com/questions/20518122/python-working-out-if-time-now-is-between-two-times

GPIO_PINS = []
GPIO_TIMES = [ [[datetime.time(22), datetime.time(10)], [datetime.time(15, 30), datetime.time(16, 30)]] ]

#https://www.sunfounder.com/learn/Super_Kit_V2_for_RaspberryPi/lesson-10-driving-leds-by-74hc595-super-kit-for-raspberrypi.html
SDI   = 23
RCLK  = 14
SRCLK = 15

FAN_PIN = 18
FAN_TIMESTEP = 0.02
FAN_INIT_RATIO = 0.5
FAN_TIMES = [ [[datetime.time(22), datetime.time(10)], [datetime.time(15, 30), datetime.time(16, 30)]], [[datetime.time(00, 00, 00), datetime.time(23, 59, 59)]] ]
FAN_RATIOS = [1.0, 0.3]

relayvals = 0x00

fan_ratio = FAN_INIT_RATIO

keeprunning = True

#acfan uses 2,3,4
#off = (false, false,  false)
#low = (true,  false,  false)
#med = (true,  false,  false)
#high= (true,  false,  false)

def exit_signal(signum, frame):
    global keeprunning
    keeprunning = False

def hc595_in(dat):
    for bit in range(0, 8):    
        GPIO.output(SDI, 0x80 & (dat << bit))
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
        time.sleep(0.001)

def hc595_out():
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)
    time.sleep(0.001)

def setup():
    global relayvals
    GPIO.setmode(GPIO.BCM)    # Number GPIOs by its physical location
    for pin in GPIO_PINS:
        GPIO.setup(pin,GPIO.OUT)
    GPIO.setup(FAN_PIN,GPIO.OUT)
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)
    hc595_in(0xff^relayvals)
    hc595_out()

def set_relay(num, val):
    global relayvals
    if (val):
        relayvals = relayvals | 1 << (7-num)
    else:
        relayvals = relayvals &  ((1 << (7-num))^0xff)

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
    global keeprunning
    while keeprunning:
        for i in range(len(GPIO_PINS)):
            newval = in_time_ranges(GPIO_TIMES[i])
            #GPIO.output(GPIO_PINS[i], newval)
            set_relay(GPIO_PINS[i], newval)
            #print newval
        for i in range(len(FAN_RATIOS)):
            j = len(FAN_RATIOS)-i-1
            if (in_time_ranges(FAN_TIMES[j])):
                fan_ratio = FAN_RATIOS[j]
        time.sleep(10)

def thread_relays():
    global relayvals
    global keeprunning
    hc595_in(0xff)
    hc595_out()
    relayvals_old = 0x00
    while keeprunning:
        if (relayvals_old != relayvals):
            hc595_in(0xff^relayvals)
            time.sleep(0.1)
            hc595_out()
            relayvals_old = relayvals
        time.sleep(0.1)
    hc595_in(0xff)
    hc595_out()


def thread_fan():
    global fan_ratio
    global keeprunning
    while keeprunning:
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
        
def test1():
    global relayvals
    for i in range(0,127):
        relayvals = i
        time.sleep(3)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_signal)
    signal.signal(signal.SIGTERM, exit_signal)
    
    setup()

    timesthread = threading.Thread(target=thread_times)
    fanthread = threading.Thread(target=thread_fan)
    relaysthread = threading.Thread(target=thread_relays)

    #timesthread.start()
    #fanthread.start()
    relaysthread.start()

    #while (keeprunning):
    #    time.sleep(0.1)


#hc595_in(0x00); hc595_out()