# leftRightUpDown.py   moves motor left/right and up/down
# Turning amount controled by time2 variable
import argparse
import time
from time import sleep
import RPi.GPIO as GPIO
import os
GPIO.setmode(GPIO.BOARD)
IN1=33 # IN1
IN2=35 # IN2
IN3=12 # IN3
IN4=32 # IN4

time2 = 0.5 # max = 8.0
# up/down 10 deg/1.0 s. left/right 10 deg/0.5 s
dir = 3 # 0=left, 1=right, 2=up, 3=down
"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('delta', type=int, default=0,
    help="steps right, dir=1. Need int argument. Example: python3 sh.py 10")
args = ap.parse_args()
xdelta = args.delta
if xdelta < 0:
    dir = 0
    xdelta = -xdelta
"""
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)

GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)

# Signals are True only when used. 
# Otherwise, all signals are False. 

# BACKWARD SIGNAL
def right():
    #os.system('clear')
    GPIO.output(IN1, True)
    sleep (time2)
    GPIO.output(IN1, False)

# FORWARD SIGNAL
def left(): 
    #os.system('clear')
    GPIO.output(IN2, True)
    sleep (time2)
    GPIO.output(IN2, False)

# DOWN SIGNAL
def up(): 
    #os.system('clear')
    GPIO.output(IN3, True)
    sleep (time2)
    GPIO.output(IN3, False)

# DOWN SIGNAL
def down(): 
    #os.system('clear')
    GPIO.output(IN4, True)
    sleep (time2)
    GPIO.output(IN4, False)

"""
start_time = time.time()
if dir == 0:  # 0 moves left or up
    left(xdelta)
    print ('Moved {:.1f} degrees left'.format(xdelta*360/512))
else:
    right(xdelta)
    print ('Moved {:.1f} degrees right'.format(xdelta*360/512))
time_now = time.time()
dtime = time.time() - start_time
print ('Execution time = ', dtime, ' sec')
print ('RPM = ', xdelta*60.0/(512.0*dtime))
print ('deg_per_sec = ', 360.0*xdelta/(512.0*dtime))
"""
if dir == 0:
    left()
    print('left, time2 = {} s'.format(time2))
elif dir == 1:
    right()
    print('right, time2 = {} s'.format(time2))
elif dir == 2:
    up()
    print('up, time2 = {} s'.format(time2))
else:
    down()
    print('down, time2 = {} s'.format(time2))
GPIO.cleanup()
print("ALL DONE")
