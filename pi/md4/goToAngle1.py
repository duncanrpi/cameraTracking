# goToAngle.py
# IMPORTANT NOTE: Use dim to medium brightness light on the marker.
# If it is not working, DIM THE LIGHT!!! 
# imports
from imutils.video import VideoStream
import imutils
import numpy as np
from time import sleep, time
import cv2
from math import ceil
import RPi.GPIO as GPIO
import argparse
from datetime import datetime

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('angle', type=float, nargs="?", default=0, \
    help="The first value is a float angle")
ap.add_argument('choice', type=int, nargs="?", default=0, \
    help="The second int value: 0=turnLeftRight,1=turnUpDown,2=goToXAngle,3=goToYAngle")

args = ap.parse_args()
angle = args.angle # angle in degrees
choice = args.choice # see above

print (__file__)
print ('angle, choice = ', angle, choice)

video = False

fps = 2
timeFactorLR = 0.06
timeFactorUD = 0.12
extraUpDown = 1
extraLeftRight = 1
previousDirection = ''

time2 = 0
timeLimit = 20 # time to end loop
if choice == 0 or choice == 1:
    timeLimit = 10
startTime = None
frame_count_limit = 50
"""
timeDelay = 0
minTimeDelay = 0.5
delayFactor = 3.0 # must be > 1.1
delayStart = 0
"""
fwidth = 1280
fheight = 960
offset = 0 # camera height = 1.555 m, marker height = 1.555 m
# offset = 100*fwidth/1000 # 55 mm marker at height = 35 mm & at 3.5 m floor distance,
                         # camera height = 1.54 m
# offset = 0 # case of a level marker
qq = 8*fwidth/1000 # offset to left of x-axis degree numbers
rr = 8*fwidth/1000 # offset upward of y-axis degree numbers
print ('\noffset, rr = ', offset, rr)
markLength = round(15.625*fwidth/1000) # pixel length of all axis marks
textPointTop = round(39.84375*fwidth/1000) # y-coordinate of lower left of axis number text
textPointLeft = round(27.34375*fwidth/1000) # x-coordinate of lower left of axis number text

print ('\nmarkLength, textPointTop, textPointLeft = ', markLength, textPointTop, textPointLeft)

xmarker, ymarker = None, None
template = cv2.imread('/home/pi/md4/images/29-0.png',0) # numpy.ndarray (13, 13)
w5, h5 = template.shape[::-1]
print ('template.shape =', template.shape, '   w5 = ', w5, '   h5 = ', h5)
deg_inc = 5
h_field_of_view = 63.6 # PiCamera degrees wide, original 62.2
    # Zealinno webcam left/right 60.7
pix_inc = deg_inc * fwidth / h_field_of_view
font=cv2.FONT_HERSHEY_SIMPLEX
fontSize = round(0.78125*fwidth/1000,1) # fontSize=1.0 with fwidth=1280, float or int required
fontThickness = ceil(1.5625*fwidth/1000) # fontThickness=2 with fwidth=1280, int required
lineThickness = ceil(1.5625*fwidth/1000) # lineThickness=2 with fwidth=1280, int required
frame_count = 0
turnCount = 0
threshold = 0.8

half_fwidth = (fwidth-1)/2.0
half_fheight = (fheight-1)/2.0

half_fwidth1 = fwidth//2 - 1
half_fheight1 = fheight//2 - 1
half_fwidth2 = fwidth//2
half_fheight2 = fheight//2

ptheta = 0 # platform angle in degrees
angleDiff = 0 # angleDiff = angle - ptheta

R = h_field_of_view / fwidth # degrees/pixel

# pin setup and sequences
GPIO.setmode(GPIO.BOARD)
IN1=33 # IN1
IN2=35 # IN2
IN3=12 # IN3
IN4=32 # IN4

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

if video == True:
    stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    gotoangle = "/home/pi/md4/" + stamp + " goToAngle1.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out1 = cv2.VideoWriter(gotoangle, fourcc, fps, (fwidth,fheight))

vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
sleep(3.0)

while True:
    frame1=vs1.read()
    frame_count += 1

    if frame_count == 1:
        startTime = time()
        print ('frame1.shape = ', frame1.shape)

    if frame_count == 2 and (choice == 0 or choice == 1):

        if choice == 0: # moving left or right
            if angle < 0:
                time2 = -timeFactorLR*angle
                right()
                previousDirection = 'right'
                print('right, time2 = {} s'.format(time2))                
            else:
                time2 = timeFactorLR*angle
                left()                
                previousDirection = 'left'
                print('left, time2 = {} s'.format(time2))
        if choice == 1: # moving up or down
            if angle < 0:
                time2 = -timeFactorUD*angle
                down()
                previousDirection = 'down'
                print('down, time2 = {} s'.format(time2)) 
            else:
                time2 = timeFactorUD*angle
                up()
                previousDirection = 'up'
                print('up, time2 = {} s'.format(time2))
        turnCount += 1

    if frame_count > 2 and (choice == 2 or choice == 3):
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        if frame_count == 3:
            print ('gray.shape =', gray.shape)
        res = cv2.matchTemplate(gray,template, cv2.TM_SQDIFF)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = min_loc  #Change to max_loc for all except for TM_SQDIFF
        bottom_right = (top_left[0] + w5, top_left[1] + h5)
            # top_left is (x,y) location

        # get (x,y) locations in gray/frame1
        x2,y2,w2,h2 = top_left[0],top_left[1],w5,h5

        cv2.rectangle(frame1, (x2, y2), (x2+w2, y2+h2), (0,0,255), lineThickness)
        xmarker = x2+w2//2
        ymarker = y2+h2//2

        # move platform to correct angle
        # if time()-delayStart > timeDelay:
        if frame_count < frame_count_limit and frame_count % 3 == 0:
            print ('frame_count = ', frame_count)
            
            if choice == 2:
                # print ('goToXAngle, choice 2')
                ptheta = (xmarker-half_fwidth)*R
                # ptheta is platform xangle in degrees.
                angleDiff = ptheta - angle
                if angleDiff < 0:
                    if previousDirection == 'left' or previousDirection == '':
                        extraAngle = 0.1*extraLeftRight # extraAngle accounts for play in the turning mechanism
                    else:
                        extraAngle = extraLeftRight
                    time2 = -timeFactorLR*(angleDiff - extraAngle)
                    """
                    timeDelay = max(delayFactor*time2,minTimeDelay)
                    delayStart = time()                    
                    """
                    left()
                    previousDirection = 'left'                    
                    print('left, time2 = {} s'.format(time2))
                else:
                    if previousDirection == 'right' or previousDirection == '':
                        extraAngle = 0.1*extraLeftRight
                    else:
                        extraAngle = extraLeftRight
                    time2 = timeFactorLR*(angleDiff + extraAngle)
                    """
                    timeDelay = max(delayFactor*time2,minTimeDelay)
                    delayStart = time()
                    """
                    right()
                    previousDirection = 'right'
                    print('right, time2 = {} s'.format(time2))
            if choice == 3: 
                # print ('goToYAngle, choice 3')
                ptheta = (ymarker - half_fheight - offset)*R
                # ptheta is platform vertical angle in degrees.
                angleDiff = angle - ptheta

                if angleDiff < 0:
                    if previousDirection == 'down' or previousDirection == '':
                        extraAngle = 0
                    else:
                        extraAngle = extraUpDown
                    time2 = -timeFactorUD*(angleDiff - extraAngle)
                    """
                    timeDelay = max(delayFactor*time2,minTimeDelay)
                    delayStart = time()
                    """
                    down()
                    previousDirection = 'down'
                    print('down, time2 = {} s'.format(time2))
                else:
                    if previousDirection == 'up' or previousDirection == '':
                        extraAngle = 0
                    else:
                        extraAngle = extraUpDown
                    time2 = timeFactorUD*(angleDiff + extraAngle)
                    """
                    timeDelay = max(delayFactor*time2,minTimeDelay)
                    delayStart = time()
                    """
                    up()
                    previousDirection = 'up'
                    print('up, time2 = {} s'.format(time2))   
            turnCount += 1            
                
        # x-axis labels
        num_L = int(xmarker / pix_inc + 1)
        # mark the degrees at the top of the frames & put numbers
        num_R = int(((fwidth-1) - xmarker) / pix_inc + 1)
        for ii in range(num_L):
            cv2.line(frame1, (int(round(xmarker-ii*pix_inc)), 0), \
               (int(round(xmarker-ii*pix_inc)), markLength), \
               (0, 0, 255), lineThickness)
            cv2.putText(frame1, str(deg_inc*ii), \
               (int(round(xmarker-ii*pix_inc-qq)), textPointTop), \
               font, fontSize, (0, 0, 255), fontThickness)
        for jj in range(1,num_R):
            cv2.line(frame1, (int(round(xmarker+jj*pix_inc)), 0), \
                (int(round(xmarker+jj*pix_inc)), markLength), \
                (0, 0, 255), lineThickness)
            cv2.putText(frame1, str(-deg_inc*jj), \
                (int(round(xmarker+jj*pix_inc-qq)), textPointTop), \
                font, fontSize, (0, 0, 255), fontThickness)
        
        # y-axis labels
        ymarker2 = ymarker - offset
        num_L2 = int(ymarker2 / pix_inc + 1)
            # mark the degrees at the left of the frames & put numbers
        num_R2 = int(((fheight-1) - ymarker2) / pix_inc + 1)
        for kk in range(num_L2):
            cv2.line(frame1, (0, int(round(ymarker2-kk*pix_inc))), \
                (markLength, int(round(ymarker2-kk*pix_inc))), \
                (0, 0, 255), lineThickness)
            cv2.putText(frame1, str(deg_inc*kk), \
                (textPointLeft, int(round(ymarker2-kk*pix_inc)+rr)), \
                font, fontSize, (0, 0, 255), fontThickness)            
        for mm in range(1,num_R2):
            cv2.line(frame1, (0, int(round(ymarker2+mm*pix_inc))), \
                (markLength, int(round(ymarker2+mm*pix_inc))), \
                (0, 0, 255), lineThickness)
            cv2.putText(frame1, str(-deg_inc*mm), (textPointLeft, \
                int(round(ymarker2+mm*pix_inc)+rr)), \
                font, fontSize, (0, 0, 255), fontThickness)     
        
    elapsed_time = time() - startTime
        
    cv2.putText(frame1, 'turnCount = {}'.format(turnCount), (int(0.20*fwidth), int(0.20*fheight)), \
        font, fontSize, (0, 0, 255), fontThickness)
    cv2.putText(frame1, 'Rotated '+previousDirection, (int(0.20*fwidth), int(0.25*fheight)), \
        font, fontSize, (0, 0, 255), fontThickness)
    cv2.putText(frame1, 'frame_count = {}'.format(frame_count), (int(0.20*fwidth), int(0.30*fheight)), \
        font, fontSize, (0, 0, 255), fontThickness)
    cv2.putText(frame1, 'elapsed_time = {:.3f}'.format(elapsed_time), (int(0.20*fwidth), \
        int(0.35*fheight)), font, fontSize, (0, 0, 255), fontThickness)

    
    cv2.putText(frame1, 'time2 = {:.3f}'.format(time2), \
        (int(0.55*fwidth), int(0.20*fheight)), font, fontSize, (0, 0, 255), fontThickness)
    """
    cv2.putText(frame1, 'timeDelay = {:.3f}'.format(timeDelay), \
        (int(0.55*fwidth), int(0.25*fheight)), font, fontSize, (0, 0, 255), fontThickness)
    cv2.putText(frame1, 'delayFactor = {:.3f}'.format(delayFactor), \
        (int(0.55*fwidth), int(0.30*fheight)), font, fontSize, (0, 0, 255), fontThickness)
    """
  
    cv2.line(frame1, (half_fwidth1, int(fheight*0.07)), \
        (half_fwidth1, int(fheight*0.46)), (0, 255, 255), \
        lineThickness) # Upper vertical line
    cv2.line(frame1, (half_fwidth1, int(fheight*0.54)), \
        (half_fwidth1, fheight-1), (0, 255, 255), lineThickness)
            # Lower vertical line
    cv2.line(frame1, (int(fwidth*0.05), half_fheight1), (int(fwidth*0.47), \
        half_fheight1), (0, 255, 255), lineThickness) # Left horizontal line
    cv2.line(frame1, (int(fwidth*0.53), half_fheight2), (fwidth-1, half_fheight1), \
        (0, 255, 255), lineThickness) # Right horizontal line
    
    cv2.imshow('frame1', frame1)
    """
    if frame_count < 6:
        print ('elapsed time = {:.3f}'.format(elapsed_time))
    """
    if video == True:
        out1.write(frame1)
    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key == ord("q") or time()-startTime > timeLimit:
        # press 'q' key to break loop
        break
cv2.destroyAllWindows() # begin ending code 
vs1.stop() # stop() is for VideoStream object
if video == True:
    out1.release() # release() is for cv2.VideoWriter object
GPIO.cleanup()
