#https://www.sunfounder.com/learn/Super_Kit_V2_for_RaspberryPi/lesson-10-driving-leds-by-74hc595-super-kit-for-raspberrypi.html
#https://www.arduino.cc/en/tutorial/ShiftOut
#https://circuitdigest.com/microcontroller-projects/raspberry-pi-74hc595-shift-register-tutorial

import RPi.GPIO as IO         # calling for header file which helps us use GPIO's of PI
import time                             # calling for time to provide delays in program
IO.setwarnings(False)           # do not show any warnings
x=1                
IO.setmode (IO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as GPIOSR_SH_CP)

SR_DS = 23
SR_SH_CP = 15
SR_ST_CP = 14

IO.setup(SR_DS,IO.OUT)            # initialize GPIO Pins as an output.
IO.setup(SR_SH_CP,IO.OUT)
IO.setup(SR_ST_CP,IO.OUT)
while 1:                               # execute loop forever
    for y in range(8):            # loop for counting up 8 times
        IO.output(SR_DS,1)            # pull up the data pin for every bit.
        time.sleep(0.1)            # wait for 100ms
        IO.output(SR_SH_CP,1)            # pull CLOCK pin high
        time.sleep(0.1)
        IO.output(SR_SH_CP,0)            # pull CLOCK pin down, to send a rising edge
        IO.output(SR_DS,0)            # clear the DATA pin
        IO.output(SR_ST_CP,1)            # pull the SHIFT pin high to put the 8 bit data out parallel
        time.sleep(0.1)
        IO.output(SR_ST_CP,0)            # pull down the SHIFT pin
    time.sleep(1)
    for y in range(8):            # loop for counting up 8 times
        IO.output(SR_DS,0)            # clear the DATA pin, to send 0
        time.sleep(0.1)            # wait for 100ms
        IO.output(SR_SH_CP,1)            # pull CLOCK pin high
        time.sleep(0.1)
        IO.output(SR_SH_CP,0)            # pull CLOCK pin down, to send a rising edge
        IO.output(SR_DS,0)            # keep the DATA bit low to keep the countdown
        IO.output(SR_ST_CP,1)            # pull the SHIFT pin high to put the 8 bit data out parallel
        time.sleep(0.1)
        IO.output(SR_ST_CP,0)