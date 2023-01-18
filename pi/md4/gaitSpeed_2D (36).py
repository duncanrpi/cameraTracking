# gaitSpeed_2D (36).py. The variable, angleRange, is removed.
# PROCESSING STAGE at about line 132
# imports
# timeLimits, radial: 37, 25, 17, crosswise: 20, 13, 11
from time import sleep, time
setupStart = time()
from imutils.video import VideoStream
from datetime import datetime
import cv2
import argparse

print ('\n'+__file__)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('correctDist', type=float, nargs="?", default=0.0, \
    help="1st: correct distance in meters")
ap.add_argument('timeLimit', type=float, nargs="?", default=30, \
    help="2nd: recording time limit (s)")
ap.add_argument('fast', type=int, nargs="?", default=1, \
    help="3rd: 0=output of 4 figures, 1=output of 2 figures (faster)")
ap.add_argument('pattern', type=int, nargs="?", default=0, \
    help="4th: for path, 0='homeRad', 1='home4m', 2='home3m', 3='Mom', " \
                + "4='UAB', 5='hosp'")
ap.add_argument('height', type=int, nargs="?", default=320, \
    help="5th: pixel height of frame")
ap.add_argument('width', type=int, nargs="?", default=640, \
    help="6th: pixel width of frame")
ap.add_argument('doctor', type=str, nargs="?", default="", \
    help="7th: doctor's name")
ap.add_argument('patientID', type=str, nargs="?", default="", \
    help="8th: patient ID")
args = ap.parse_args()
correctDist = args.correctDist # (m) measured distance to be walked <class 'float'>
timeLimit = args.timeLimit # timeLimit, totalTime = 3,82
fast = args.fast # see above. Also used in guiWalk.py to calculate time for progress bar.
pattern = args.pattern
height = args.height
width = args.width
doctor = args.doctor
patientID = args.patientID
print ('\ncorrectDist, timeLimit, fast, pattern =', correctDist, timeLimit, fast, pattern)
print ('height, width, doctor, patientID =', height, width, doctor, patientID)
if pattern == 0:
    path = "homeRad"
if pattern == 1:
    path = "home4m"
if pattern == 2:
    path = "home3m"
if pattern == 3:
    path = "Mom"
if pattern == 4:
    path = "UAB"
if pattern == 5:
    path = "hosp"
pixels = width * height
fps = round(3730000 / pixels,1) # pattern = 2
if pattern == 0:
    fps = round(2890000 / pixels,1)
elif pattern == 1:
    fps = round(3050000 / pixels,1)
elif pattern == 3:
    fps = round(3730000 / pixels,1)
faceFound = False
t_raw_ = [] # time array for all recording time including face finding time 
                     # and before trimming start & end (1st)

# LEFT & RIGHT CAMERAS
fwidth02 = 640
fheight02 = 480
sliceHeight02 = height # 200 for 4 to 6m, 320 for all-round height
sliceTop02 = (fheight02 - sliceHeight02) // 2
if pattern == 1 or pattern == 2:
    sliceTop02 = sliceTop02 - 0
elif pattern == 0:
    sliceTop02 = sliceTop02 - 25    
sliceBottom02 = sliceHeight02 + sliceTop02
sliceWidth02 = width # 640 or 480
sliceLeft02 = (fwidth02 - sliceWidth02) // 2
sliceRight02 = sliceWidth02 + sliceLeft02

stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print ('\nstamp = ', stamp, '\n')
recordVideos0of2 = '/home/pi/runs/'+ stamp + ' recordVideos0of2.avi'
recordVideos2of2 = '/home/pi/runs/'+ stamp + ' recordVideos2of2.avi'
fc1 = 0

vs0 = VideoStream(usePiCamera=False,src=0).start() # left Zealinno webcam
vs2 = VideoStream(usePiCamera=False,src=2).start() # right Zealinno webcam
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out0 = cv2.VideoWriter(recordVideos0of2,fourcc, fps, (sliceWidth02,sliceHeight02))
out2 = cv2.VideoWriter(recordVideos2of2,fourcc, fps, (sliceWidth02,sliceHeight02))

sleep(7.0)
setupTime = time() - setupStart
recordStart = time()
while True:
    if fc1 % 2 == 0: # odd frame_count
                             # because += 1 right after read()
        frame00=vs0.read()
        frame22=vs2.read()
    else: # even frame_count
        frame22=vs2.read()
        frame00=vs0.read()        
    fc1 += 1
    if fc1 == 1:
        timeStart = time()
        # print('frame00.shape, frame22.shape =', frame00.shape, frame22.shape)
    t_raw_.append(time() - timeStart)
    # print ('fc1, t_raw = {}, {:.3f}'.format(fc1, time() - timeStart))
    
    frame0 = frame00[sliceTop02:sliceBottom02,sliceLeft02:sliceRight02]
    frame2 = frame22[sliceTop02:sliceBottom02,sliceLeft02:sliceRight02]
    out0.write(frame0)
    out2.write(frame2)
    cv2.imshow('frame0', frame0)
    cv2.imshow('frame2', frame2)
    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if time() - timeStart > timeLimit or key == ord("q"): # press 'q' key to break loop
        break

recordTime = time() - recordStart
processStart = time()
recordFrames = fc1
record_fps = recordFrames/recordTime
print ('recordTime = {:.3f} s'.format(recordTime))
print ('recordFrames = ', recordFrames)
print ('record_fps = {:.3f} frames/second for new fps'.format(record_fps))
print ('Set fps = {:.3f} frames/second'.format(fps))

cv2.destroyAllWindows() # begin ending code
vs0.stop() # stop() is for VideoStream object
vs2.stop() # stop() is for VideoStream object
out0.release()
out2.release()



# PROCESSING STAGE

# imports
from inspect import currentframe, getframeinfo
import numpy as np
from math import sin,cos,pi,tan,atan2,radians,degrees,sqrt,floor,ceil,asin
from statistics import mean
from numpy import median
from scipy.interpolate import interp1d, interp2d
import csv
import pickle

angHalf = atan2(4.0,6.0)/2 # 0.2940013018, radians. In degrees, angHalf = 16.84503376 
lenx = 8
leny = 8
lengrid = lenx*leny
gridx_ = [] # x input coordinates
gridy_ = [] # y input coordinates
gridr_ = [] # radius input coordinates
gridang_ = [] # angle (0 center) input coordinates
for i in range(1,lenx+1):
    for j in range(-1,leny-1):
        gridx_.append(i)
        gridy_.append(j)
        gridr = round(sqrt(i**2+j**2),4)
        gridr_.append(gridr)
        gridang = round(atan2(j,i)-angHalf,6) # radians
        gridang_.append(gridang)

# print ('x input coordinates, len(gridx_) = ', len(gridx_))
# print ('gridx_ = ', gridx_)
# print ('\ny input coordinates, len(gridy_) = ', len(gridy_))
# print ('gridy_ = ', gridy_)
"""
print ('\nradius input coordinates, len(gridr_) = ', len(gridr_))
print ('gridr_[0:8] = ', gridr_[0:8])
print ('gridr_[8:16] = ', gridr_[8:16])
print ('gridr_[16:24] = ', gridr_[16:24])
print ('gridr_[24:32] = ', gridr_[24:32])
print ('gridr_[32:40] = ', gridr_[32:40])
print ('gridr_[40:48] = ', gridr_[40:48])
print ('gridr_[48:56] = ', gridr_[48:56])
print ('gridr_[56:64] = ', gridr_[56:64])
print ('\nangle (0 center) input coordinates, len(gridang_) = ', len(gridang_))
print ('gridang_[0:8] = ', gridang_[0:8])
print ('gridang_[8:16] = ', gridang_[8:16])
print ('gridang_[16:24] = ', gridang_[16:24])
print ('gridang_[24:32] = ', gridang_[24:32])
print ('gridang_[32:40] = ', gridang_[32:40])
print ('gridang_[40:48] = ', gridang_[40:48])
print ('gridang_[48:56] = ', gridang_[48:56])
print ('gridang_[56:64] = ', gridang_[56:64])
"""
# radius output coordinates
# ORIGINAL

gridout_ = [1.9013, 1.1, 1.3163, 1.8037, 2.2508, 2.6257, 2.938, 3.2, \
2.848, 2.2, 2.1645, 2.4446, 2.8147, 3.1831, 3.5222, 3.8264, \
4.1178, 3.41, 3.1891, 3.2677, 3.4913, 3.7678, 4.0525, 4.326, \
5.4558, 4.66, 4.2904, 4.2045, 4.287, 4.4579, 4.6684, 4.8914, \
7.1805, 6.183, 5.6205, 5.3543, 5.2802, 5.3232, 5.4334, 5.5789, \
8.5644, 7.5286, 6.8834, 6.5175, 6.3457, 6.3043, 6.3469, 6.4415, \
10.2096, 9.0, 8.1939, 7.6782, 7.3701, 7.208, 7.1465, 7.1531, \
11.8812, 10.5, 9.5384, 8.8805, 8.4435, 8.1665, 8.0046, 7.9245]
# print ('\nradius output coordinates, len(gridout_) = ', len(gridout_))
# print ('gridout_ = ', gridout_)

rrr_f = interp2d(gridx_, gridy_, gridout_, 'cubic')
# rrr_f = interp2d(xxx_, yyy_, rrr_, 'cubic')

if pattern == 0:
    adjFactor2 = 1.03 # 1.02083 # 1.03583 # 1.0087
elif pattern == 1:
    adjFactor2 = 1.0 # 0.97623 # 0.94322 # 0.96623
else:
    adjFactor2 = 1.0

rt = 8 # in medFilter7(x,n,rt), smooth7(x,n,rt), rt elements at the start are averaged,
       #   and the average is assigned to the first rt elements in the filter result.
       # the same is done for rt elements at the end.
       # the purpose is to smooth the starting and ending points, but also keep them
       #   from being changed by the filter.
       # the starting and ending points are more important because they
       #   can be reference points for distance traveled or angle positions
LL,RR,UU,DD = 5,5,5,5 # larger size for radial (pattern = 0) going far to near


if pattern == 1: # For case of walking left or right
    LL,RR,UU,DD = 5,5,5,5

c = 0.2735 # (meters) separation between left and right cameras
half_c = c/2 # 0.13675
h_field_of_view02 = 60.7 # Zealinno webcam left/right
    # round webcam left/right 21.51008232
dpp02 = h_field_of_view02 / fwidth02 # 0.09484375
focalDepth = 4.0 # (m) Left & right cameras point inward at a point at distance focalDepth
focalAngle = degrees(atan2(half_c, focalDepth)) # 1.958036858 (degrees) Angle inward from parallel
pixAdj = focalAngle / dpp02 # 20.64486968 (pixels, float) Adjustment pixels to add or subtract
    # to get correct subject pixel position from left or right cameras, respectively.
print ('dpp02,focalDepth,focalAngle,pixAdj = {:.5f}, {}, {:.3f}, {:.2f}' \
       .format(dpp02,focalDepth,focalAngle,pixAdj))
angleIncreasing = -1

tracker0 = cv2.TrackerCSRT_create()

cue02 = int(490.0*sliceHeight02/500.0)

data1 = int(560.0*sliceHeight02/500.0)
data2 = int(620.0*sliceHeight02/500.0)
data3 = int(680.0*sliceHeight02/500.0)
data4 = int(740.0*sliceHeight02/500.0)

data5 = int(800.0*sliceHeight02/500.0)
data6 = int(860.0*sliceHeight02/500.0)
data7 = int(920.0*sliceHeight02/500.0)
data8 = int(980.0*sliceHeight02/500.0)
if pattern == 1:
    data1 = int(630.0*sliceHeight02/500.0)
    data2 = int(820.0*sliceHeight02/500.0)
    data3 = int(1010.0*sliceHeight02/500.0)
    data4 = int(1200.0*sliceHeight02/500.0)

    data5 = int(1390.0*sliceHeight02/500.0)
    data6 = int(1580.0*sliceHeight02/500.0)
    data7 = int(1770.0*sliceHeight02/500.0)
    data8 = int(1960.0*sliceHeight02/500.0)
        
blue, green, yellow, orange = (255,0,0), (0,255,0), (0,255,255), (0,125,255)
red, black, white, lblue = (0,0,255), (0,0,0), (255,255,255), (255,50,50)
if pattern == 0:
    fsize = 0.5 # fontsize
    fBold = 1 # fontBoldness
    col1 = 200
    col2 = 400
else:
    fsize = 0.8
    fBold = 2
    col1 = 320
    col2 = 640
fsize2 = 0.8  # fontsize
fBold2 = 2 # fontBoldness
fBold3 = 2
font = cv2.FONT_HERSHEY_SIMPLEX
LT = cv2.LINE_AA
x,y,w,h = 0,0,0,0
faceNum = 0 # fc1 (frame count) when face is found with Haar cascades
faces, dep_raw = None, None
start_i, end_i = 0, 0
minPixels, maxPixels, oldMaxPixels, oldMinPixels = None, None, -1.0, 1000
startPixels, endPixels = None, None
setStart, setEnd = False, False
threshPixels = 10 

# 1-POINT ARRAYS (_ at the end means Python list)
t_raw2_ = [] # (s) time after finding face (2nd)
t_ = [] # (s) time for the final data (3rd)
fc2_ = [] # (frames) fc2_[0] = 1; frame numbers after finding face
# fc3_ = [] # (frames) frame count after reduction (1, 2, 3. ...)
# fc3_2_ = [] # (frames) frame numbers after reduction but from fc2_ (1, n+1, 2n+1, ...)
dep_raw_ = [] # (m) subject depth (distances from center camera) before filtering
dep_ = [] # (m) subject depth (distances from center camera) after filtering
ddep_ = []
z0_raw_ = [] # (pixels) subject float pixel position, left camera, =x0_exp_f+w0_exp_f/2+pixAdj
z0_ = [] # (pixels) subject float pixel position, left camera
z2_raw_ = [] # (pixels) subject float pixel position, right camera, =x2_exp_f+w2_exp_f/2-pixAdj
z2_ = [] # (pixels) subject float pixel position, right camera
ang0_ = [] # (deg) subject angle position, left camera
ang1_raw_ = [] # (deg) subject angle position, center camera before filtering
ang1_ = [] # (deg) subject angle position, center camera after filtering
ang2_ = [] # (deg) subject angle position, right camera
C_ = [] # (deg) triangle angle at subject point
a_ = [] # (m) subject depth from right camera
b_ = [] # (m) subject depth from left camera

# 2-POINT ARRAYS
mov_raw_ = [] # (m)
mov_ = [] # (m) distance moved between frames
movCum_raw_ = [] # (m)
movCum_ = [] # (m) total distance moved
dt_raw_ = [] # (s) elapsed time between frames
dt_ = [] # (s) elapsed time between frames
speed_raw_ = [] # (m/s) speed between frames
speed2_ = [] # (m/s) speed between frames before last median7() filter
speed_ = [] # (m/s) speed between frames

accel_raw_ = [] # (m/s^2) acceleration between frames
accel_ = [] # (m/s^2) acceleration between frames
angSpeed_raw_ = [] # (deg/s) between frames
angSpeed_ = [] # (deg/s) between frames
z0_speed_ = [] # (pix/s) between frames
z2_speed_ = [] # (pix/s) between frames

# FUNCTIONS

def line():
    cf = currentframe()
    return cf.f_back.f_lineno

# Moving average reduction Filter aveReduct2(x,n) replaces each n values
# with 1 value, their average. Any leftover elements are discarded.
# x is the input array. y is the output array.
# len(y) = floor(len(x)/n).
def aveReduct(x,n):
    num = len(x) / n
    y = [0] * floor(num)
    if len(x)>=1:
        for j in range(0,floor(num)):
            y[j]=mean(x[j*n:j*n+n])
    else:
        y=x
    return y

# x is the input array. n = 2K + 1, the filter size. y is the output array.
# Required: n >= 3. n is odd. len(x) > n.
def medFilter7(x,n,rt): 
    if len(x)>=n:       
        y = [0] * len(x)  
        # print ('medFilter7 rt, n, len(x) =', rt, n, len(x))
        fff = n//2-rt+1
        ggg = n-rt
        hhh = ggg//fff
        # print ('medFilter7 fff, ggg, hhh =', fff, ggg, hhh)
        for j in range(len(x)):
            
            # first rt elements
            if j < rt:
                y[j]=median(x[0:rt])            
                
            # other first few elements    
            elif j >= rt and j < n//2:
                y[j]=median(x[0:rt+(j-rt+1)*hhh])  
                
            # other last few elements  
            elif j >= len(x)-n//2 and j < len(x)-rt:
                y[j]=median(x[(1-hhh)*(len(x)-rt)+j*hhh:len(x)])   
                
            # last rt elements
            elif j >= len(x)-rt:
                y[j]=median(x[len(x)-rt:len(x)])
                
            # rest of elements away from edges
            else:
                y[j]=median(x[j-n//2:j+n//2+1])
    else:
        y=x
    return y

def smooth7(x,n,rt): 
    if len(x)>=n:       
        y = len(x) * [0]
        # print ('smooth7 rt, n, len(x) =', rt, n, len(x))
        fff = n//2-rt+1
        ggg = n-rt
        hhh = ggg//fff
        # print ('smooth7 fff, ggg, hhh =', fff, ggg, hhh)
        for j in range(len(x)):
            
            # first rt elements
            if j < rt:
                y[j]=mean(x[0:rt])            
            
            # other first few elements     
            elif j >= rt and j < n//2:
                y[j]=mean(x[0:rt+(j-rt+1)*hhh])  
                
            # other last few elements  
            elif j >= len(x)-n//2 and j < len(x)-rt:
                y[j]=mean(x[(1-hhh)*(len(x)-rt)+j*hhh:len(x)])
                
            # last rt elements
            elif j >= len(x)-rt:
                y[j]=mean(x[len(x)-rt:len(x)])
                
            # rest of elements away from edges
            else:
                y[j]=mean(x[j-n//2:j+n//2+1])
    else:
        y=x
    return y

# Returns distance between 2 points, (r1, theta1) and (r2, theta2), polar coordinates (2D).
# theta1 and theta2 are in degrees and are converted to radians for the function
def polar_dist_moved(r1,r2,theta1,theta2):
    return sqrt(r1**2 + r2**2 - 2*r1*r2*cos(radians(theta2-theta1)))

def showWrite025():
    global frame02, frame025, out025
    frame02 = np.hstack((frame0, frame2))
    frame025 = np.vstack((frame02, frame5))
    cv2.imshow('frame025',frame025)
    out025.write(frame025)

def draw_arrow(axis):
    global ang1_
    if ang1_[0] < 0: # up arrow
        axis.annotate("Walking\nDirection",
                xy=(1.30, 0.58), xycoords='axes fraction',
                xytext=(1.27, 0.48), textcoords='axes fraction',ha='center',va='top',
                arrowprops=dict(width=12,headwidth=48,shrink=0.05,
                                headlength=72,color='black'),
        )
    else: # down arrow
        axis.annotate("Walking\nDirection",
                xy=(1.27, 0.42), xycoords='axes fraction',
                xytext=(1.30, 0.52), textcoords='axes fraction',ha='center',va='bottom',
                arrowprops=dict(width=12,headwidth=48,shrink=0.05,
                                headlength=72,color='black'),
        )

def draw_arrow2(axis):
    axis.annotate("Walking Direction",
            xy=(1.32, 0.53), xycoords='axes fraction',
            xytext=(1.42, 0.53), textcoords='axes fraction',ha='left',va='center',
            arrowprops=dict(width=12,headwidth=48,shrink=0.05,
                            headlength=72,color='black'),
    )

# floor to multiple of n
def floorn(x,n):
    y = n*floor(x/n)
    return y

# ceil to multiple of n
def ceiln(x,n):
    y = n*ceil(x/n)
    return y

# get distance from time array (ta_) and speed array (sa_)
def distance_from_speed_(ta_, sa_):
    distance = 0.0
    for i in range(len(ta_)-1):
        distance = distance + (ta_[i+1]-ta_[i])*(sa_[i+1]+sa_[i])/2.0
    return distance

big = 3 # needed for enlargement of frame0 so that haar cascades can find the face at a greater distance
less_original = 3 # needed for template matching, left & right
less = less_original
less2 = 0 # needed for template matching, top & bottom 
face_cascade = cv2.CascadeClassifier('/home/pi/md4/haarcascades/haarcascade_frontalface_default.xml')
fc2 = -1 # It counts each frame of PROCESSING STAGE output video
cap0 = cv2.VideoCapture(recordVideos0of2)
cap2 = cv2.VideoCapture(recordVideos2of2)
processVideos025 = '/home/pi/runs/'+ stamp + ' processVideos.avi'
if pattern == 1:
    less = 0
    less2 = 0
    out025 = cv2.VideoWriter(processVideos025,fourcc,fps, \
                             (2*sliceWidth02,4*sliceHeight02))
    frame5 = np.zeros([3*sliceHeight02, 2*sliceWidth02, 3], dtype=np.uint8)
else:
    out025 = cv2.VideoWriter(processVideos025,fourcc,fps, \
                             (2*sliceWidth02,2*sliceHeight02))
    frame5 = np.zeros([sliceHeight02, 2*sliceWidth02, 3], dtype=np.uint8)
frame5.fill(255) # or frame5[:] = 255
print ('frame5.shape = ', frame5.shape)

capSleep = 1.0
sleep(capSleep)

while 1:
    ret0, frame0 = cap0.read()
    ret2, frame2 = cap2.read()
    if frame0 is None:
        print ('line', line(), ', End of video, frame0 is None')
        break
    fc2 += 1
    
    ### START OF 1ST LOOP ### START OF 1ST LOOP ### START OF 1ST LOOP ###
    # frame0 starts with haar cascades, and updates with CSRT, all with floats
        # CSRT initializes with bb0 input and uodates with box0 output.
        # Both bb0 and box0 are tuples containing 4 floats
        # bb0 remains, but box0 keeps changing
    # frame2 does all with template matching with templates from frame0, all with ints
    
    # find face in frame0 with haar cascades
    if faceFound == False:        
        frame0_exp = cv2.resize(frame0, (0, 0), fx=big,fy=big) # frame0_exp is enlargement
            # of frame0 so that haar cascades can find the face at a greater distance
        gray0_exp = cv2.cvtColor(frame0_exp, cv2.COLOR_BGR2GRAY) # gray0_exp is enlarged also

        if fc2 == 0:
            print ('line', line(), ', FACE FINDING STAGE')
            print ('frame0.shape =', frame0.shape)
            print ('frame0_exp.shape, gray0_exp.shape =', frame0_exp.shape, gray0_exp.shape)            

        # FIND FACE POSITION IN frame0
        faces = face_cascade.detectMultiScale(gray0_exp, 1.3, 5)
        if len(faces) == 0:
            cv2.putText(frame0,'No face, fc2={}'.format(fc2),
                    (0,cue02), font, fsize2, yellow, fBold2, LT)
            showWrite025()

            key0 = cv2.waitKey(1) & 0xFF
            if key0 == ord("q"): # press 'q' key to break early
                print ('line', line(), ', pressed "q"')
                break
            print ('No face, frame0, fc2 = ', fc2)
            continue # go to next while loop

        num = len(faces)
        xx,yy,ww,hh = 0,0,0,0
        for (x,y,w,h) in faces: # (x,y,w,h) is a tuple containing type int     
            xx,yy,ww,hh = xx+x,yy+y,ww+w,hh+h
        x0_f,y0_f,w0_f,h0_f = xx/(num*big),yy/(num*big),ww/(num*big),hh/(num*big)
            # float averages & scale back to original size
            # face without background from unexpanded rectangle in frame0/gray0
        x0,y0,w0,h0 = int(x0_f), int(y0_f), int(w0_f), int(h0_f) # unexpanded int box

        print ('\nline', line(), ', averages: x0_f,y0_f,w0_f,h0_f = ' \
               + '{:.1f}, {:.1f}, {:.1f}, {:.1f}'.format(x0_f,y0_f,w0_f,h0_f))
        print ('line', line(), ',        expand numbers: LL,RR,UU,DD =', LL,RR,UU,DD)
        x0_exp_f,y0_exp_f,w0_exp_f,h0_exp_f = x0_f-LL*w0_f/10, y0_f-UU*h0_f/10, \
                  (10+LL+RR)*w0_f/10, (10+UU+DD)*h0_f/10 # expanded float box
        x0_exp, y0_exp, w0_exp, h0_exp = int(x0_exp_f), int(y0_exp_f), \
                        int(w0_exp_f), int(h0_exp_f) # expanded int box
        
        bb0 = (x0_exp_f, y0_exp_f, w0_exp_f, h0_exp_f)
            # expanded float box for CSRT initialization, line 415
        print ('line', line(), ', expanded int box: x0_exp, y0_exp, ' \
            + 'w0_exp, h0_exp = ', x0_exp, y0_exp, w0_exp, h0_exp)
        print ('expanded float box (bb0): x0_exp_f, y0_exp_f, w0_exp_f, h0_exp_f = ' \
            + '{:.1f}, {:.1f}, {:.1f}, {:.1f}'.format(x0_exp_f, y0_exp_f, w0_exp_f, h0_exp_f))
        print ('   bb0 = ', ' '.join(format(f, '.1f') for f in bb0))

        # FIND FACE POSITION IN frame2 with template matching to frame0 rectangle
        gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        template = gray0[y0:y0+h0, x0:x0+w0] # face without background
            # from unexpanded rectangle in gray0
        
        # choose search area/ region of interest (roi) 
        # from x2_red, y2_red, w2_red, h2_red of previous loop
        roiLeft = max(int(x0 - 16*w0/10),0)
        roiRight  = min(int(x0 + 26*w0/10),sliceWidth02-1)
        roiTop = max(int(y0 - 12*h0/10),0)
        roiBottom = min(int(y0 + 22*h0/10),sliceHeight02-1)
        
        roi = gray2[roiTop:roiBottom, roiLeft:roiRight]                
        
        res = cv2.matchTemplate(roi,template,cv2.TM_SQDIFF)
        
        # For TM_SQDIFF, Good match yields minimum value; bad match yields large values
        # For all others it is exactly opposite, max value = good fit.
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = min_loc  #Change to max_loc for all except for TM_SQDIFF
        bottom_right = (top_left[0] + w0, top_left[1] + h0) # top_left is (x,y) location        
        
        # get (x,y) locations in gray2/frame2
        x2,y2,w2,h2 = top_left[0]+roiLeft,top_left[1]+roiTop,w0,h0
        x2_red, y2_red, w2_red, h2_red = x2,y2,w2,h2 # needed in UPDATE LOOPS
        
        faceNum = fc2 # faceNum = 0 if successful on first try
        t_raw2_ = t_raw_[faceNum+1:] # get times for frames after faceNum
        t_raw2_ = [x-t_raw2_[0] for x in t_raw2_] # shift times to start at 0.
        
        # initialize the frame0 tracker at the faceNum frame
        tracker0.init(frame0,bb0)
            # frame0, bb0 exist. bb0 is expanded float box input, line 482
        print ('\nfaceNum =', faceNum)
        print ('line', line(), ', TRACKER 0 INITIATED')        
        faceFound = True
        
        # DRAW FACE RECTANGLES ON frame0 & frame2
        cv2.rectangle(frame0, (x0_exp, y0_exp), (x0_exp+w0_exp, y0_exp+h0_exp), green, 2)
            # expanded int box, line 384
        cv2.rectangle(frame0, (x0, y0), (x0+w0, y0+h0), green, 2)
            # unexpanded int box, line 378   
        
        cv2.rectangle(frame2, (x2, y2), (x2+w2, y2+h2), green, 2)
            # int hit box, unexpanded, 1st loop, line 405
        
        cv2.rectangle(frame2, (roiLeft, roiTop), (roiRight, roiBottom), yellow, 2)
            # int search box, 1st loop, lines 498-501
        
        showWrite025()        
        
        continue   

    ### END OF 1ST LOOP ### END OF 1ST LOOP ### END OF 1ST LOOP ###
    
    ### START OF UPDATE LOOPS ### START OF UPDATE LOOPS ### START OF UPDATE LOOPS ###

    # Note that tracker.init() was done at fc2 = faceNum
    # near end of FACE FINDING STAGE for frame0
    # update the frame0 tracker at all frames after faceNum frame
    # use template matching for each frame2 update
    
    (success0,box0) = tracker0.update(frame0)
    if not success0:
        print ('line', line(), ', frame0 TRACKING FAILURE')
        cv2.putText(frame0,'FAIL fc2={}'.format(fc2), (0,cue02), font, fsize2, red, fBold2, LT)
        showWrite025()
        
        keyCfail0 = cv2.waitKey(1) & 0xFF
        if keyCfail0 == ord("q"): # press 'q' key to break early
            print ('line', line(), ', pressed "q"')
            break
        break
    x0_exp_f,y0_exp_f,w0_exp_f,h0_exp_f = box0 # CSRT keeps track of this for each update
    (x0_exp,y0_exp,w0_exp,h0_exp) = [int(a) for a in box0]
        # these ints are used for rectangle, line 482
    z0_raw = x0_exp_f+w0_exp_f/2+pixAdj
    z0_raw_.append(z0_raw) # subject float pixel position, left camera
            
    # FIND FACE POSITION IN frame2 with template matching to frame0 rectangle
    # reduce the expanded frame0 box to rectangle like a haar cascades hit
    w0 = int(10*w0_exp_f/(10+LL+RR))
    h0 = int(10*h0_exp_f/(10+UU+DD))
    x0 = int(x0_exp_f + LL*w0/10)
    y0 = int(y0_exp_f + UU*h0/10)
    
    if pattern == 0 and dep_raw:
        if dep_raw > 4.82:
            less = less_original
        elif dep_raw > 3.87:
            less = int(less_original*1.246)
        elif dep_raw > 3.10:
            less = int(less_original*1.552)
        elif dep_raw > 2.49:
            less = int(less_original*1.933)
        else:
            less = int(less_original*2.408)        
        
    x0_red = x0+less
    y0_red = y0+less2
    w0_red = w0-2*less
    h0_red = h0-2*less2
    
    gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # choose search area/ region of interest (roi2) 
    # from x2_red, y2_red, w2_red, h2_red of previous loop
    roiLeft = max(int(x2_red - 6*w2_red/10),0)
    roiRight  = min(int(x2_red + 16*w2_red/10),sliceWidth02-1)
    roiTop = max(int(y2_red - 3*h2_red/10),0)
    roiBottom = min(int(y2_red + 13*h2_red/10),sliceHeight02-1)

    roi2 = gray2[roiTop:roiBottom, roiLeft:roiRight]

    template = gray0[y0_red:y0_red+h0_red, x0_red:x0_red+w0_red] # face without background
        # from reduced rectangle in gray0           
    res = cv2.matchTemplate(roi2,template,cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # all results are ints for roi2

    top_left = min_loc  #Change to max_loc for all except for TM_SQDIFF
    bottom_right = (top_left[0] + w0_red, top_left[1] + h0_red)
        # top_left & bottom_right are (x,y) locations in roi2    

    # get (x,y) locations in gray2/frame2
    x2_red, y2_red, w2_red, h2_red = top_left[0]+roiLeft, top_left[1]+roiTop, \
        w0_red, h0_red # all ints. width & height were reduced by 2*less
            # & 2 * less2, respectively, to make template. hit is same dimensions.
    
    z2_raw = x2_red+w2_red/2-pixAdj
    z2_raw_.append(z2_raw) # subject float pixel position, right camera

    if fc2 > faceNum:
        fc2_.append(fc2)
        ang0 = (sliceWidth02/2 - z0_raw) * dpp02
        ang2 = (sliceWidth02/2 - z2_raw) * dpp02        
        A = 90 + ang0
        B = 90 - ang2
        C = 180 - A - B
        a = c * sin(radians(A)) / sin(radians(C)) # subject distance from right camera
        b = c * sin(radians(B)) / sin(radians(C)) # subject distance from left camera
        Cx = b*cos(radians(ang0))
        Cy = b*sin(radians(ang0)) + half_c
        ang1_raw = degrees(atan2(Cy,Cx))
        # ang1_raw = (ang0 + ang2) / 2
        ang0_.append(ang0) # subject angle position, left camera      
        ang1_raw_.append(ang1_raw) # subject angle position, center camera
        dep_raw = sqrt(b**2 + half_c**2 - 2*b*half_c*cos(radians(A)))
              # subject distance from center camera
        ang2_.append(ang2) # subject angle position, right camera
        C_.append(C) # triangle angle at subject point
        a_.append(a) # subject distance from right camera
        b_.append(b) # subject distance from left camera
        dep_raw_.append(dep_raw) # (depth array), subject distance from center camera             
    if fc2 == faceNum+1:
        mov_raw = 0.0
        movCum_raw = 0.0
        dt_raw = 0.0
        speed_raw = 0.0
        
        if ang1_raw_[0] < 0:
            angleIncreasing = 1
        maxPixels = z0_raw_[0] - pixAdj # The z0_raw_[0] - pixAdj is a frame coordinate.
            # z0_raw_[0] is a world coordinate for a parallel camera view used for depth
            # calculations. The frame view is a non-parallel camera view and is therefore
            # offset by pixAdj pixels.
        minPixels = z0_raw_[0] - pixAdj
        print ('\nline', line(), ', fc2, minPixels, maxPixels = {}, {:.2f}, {:.2f}\n' \
               .format(fc2, minPixels, maxPixels))
            
        if ang1_raw < -10:
            angleName = 'angle0'
        elif ang1_raw < 2:
            angleName = 'angle1'
        elif ang1_raw < 11:
            angleName = 'angle2'
        else:
            angleName = 'angle3'
    if fc2 > faceNum+1:
        mov_raw = adjFactor2*polar_dist_moved(dep_raw, \
            dep_raw_[len(dep_raw_)-2], ang1_raw, ang1_raw_[len(ang1_raw_)-2])
        movCum_raw = movCum_raw + mov_raw
        dt_raw = t_raw_[fc2-faceNum-1] - t_raw_[fc2-faceNum-2]
        speed_raw = mov_raw / dt_raw        

        # Update maxPixels, minPixels, setStart, start_i, end_i
        maxPixels = max(z0_raw - pixAdj, maxPixels)
        minPixels = min(z0_raw - pixAdj, minPixels)
        
        if angleIncreasing == 1:
            startPixels = maxPixels - threshPixels     
            if setStart == False:            
                if z0_raw - pixAdj <= startPixels:
                    start_i = fc2-1 # fc2 = frame, fc2_[0] = 1
                    setStart = True # NOTE 1: do not assign start_i again unless pixels
                                    # (z0_raw-pixAdj) are again startPixels or before
                    # print ('\nstart_i, fc2 = ', start_i, fc2, '\n')
            
            # see if pixels are again startPixels or before
            else: # case of setStart = True
                if z0_raw - pixAdj > startPixels: 
                    setStart = False
                if z0_raw - pixAdj == startPixels:                                           
                    start_i = fc2-1 # keep setStart = True # NOTE 1
                    # print ('\nstart_i, fc2 = ', start_i, fc2, '\n')
                    
            if minPixels < oldMinPixels:                
                endPixels = minPixels + threshPixels
                oldMinPixels = minPixels
                for i in range(end_i, len(z0_raw_)):
                    if z0_raw_[i] - pixAdj <= endPixels:
                        if i < len(z0_raw_)-1:                        
                            if max(z0_raw_[i+1:]) - pixAdj < endPixels:
                                end_i = i
                                # print ('\nend_i, fc2 = ', end_i, fc2, '\n')
                                break
                        else:
                            end_i = i
                            break
            """
            if fc2 < 5:
                if start_i:
                    print ('\nline', line(), ', fc2-1, start_i, maxPixels, startPixels = ', \
                           fc2-1, start_i, maxPixels, startPixels)
                if end_i:
                    print ('\nline', line(), ', fc2-1, end_i, minPixels, endPixels = ', \
                           fc2-1, end_i, minPixels, endPixels)
            """     
        else: # case of angleIncreasing = -1
            startPixels = minPixels + threshPixels     
            if setStart == False:            
                if z0_raw - pixAdj >= startPixels:
                    start_i = fc2-1 # fc2 = frame, fc2_[0] = 1
                    setStart = True # NOTE 1: do not assign start_i again unless pixels (z0_raw-pixAdj)
                                    # are again startPixels or before
                    # print ('\nstart_i, fc2 = ', start_i, fc2, '\n')
                    
            # see if pixels are again startPixels or before
            else: # case of setStart = True
                if z0_raw - pixAdj < startPixels:
                    setStart = False
                if z0_raw - pixAdj == startPixels:
                    start_i = fc2-1 # setStart = True, remains # NOTE 1
                
            
            if maxPixels > oldMaxPixels:                
                endPixels = maxPixels - threshPixels
                oldMaxPixels = maxPixels
                for i in range(end_i, len(z0_raw_)):
                    if z0_raw_[i] - pixAdj >= endPixels:
                        if i < len(z0_raw_)-1:                            
                            if min(z0_raw_[i+1:]) - pixAdj > endPixels:
                                end_i = i
                                # print ('\nend_i, fc2 = ', end_i, fc2, '\n')
                                break
                        else:
                            end_i = i
                            break
            """    
            if fc2 < 5:
                if start_i:
                    print ('\nline', line(), ', fc2-1, start_i, minPixels, startPixels = ', \
                           fc2-1, start_i, minPixels, startPixels)
                if end_i:
                    print ('\nline', line(), ', fc2-1, end_i, maxPixels, endPixels = ', \
                           fc2-1, end_i, maxPixels, endPixels)
            """                    
    mov_raw_.append(mov_raw)
    movCum_raw_.append(movCum_raw)
    dt_raw_.append(dt_raw)
    speed_raw_.append(speed_raw)
    
    # DRAW VERTICAL ANGLE LINES ON frame0
    # DRAW FACE RECTANGLES ON frame0 & frame2
    """
    for i in range(50,width,100):
        cv2.line(frame0, (i, 0), (i, height-1), black, 1)
    for i in range(0,width,100):
        cv2.line(frame0, (i, 0), (i, height-1), white, 1)
    """
    if fc2 > faceNum+1:
        cv2.line(frame0, (int(minPixels), 0), (int(minPixels), height-1), green, 2) # light blue
        cv2.line(frame0, (int(startPixels), 0), (int(startPixels), height-1), orange, 2) # green
    
        cv2.line(frame0, (int(endPixels), 0), (int(endPixels), height-1), orange, 2) # orange    
        cv2.line(frame0, (int(maxPixels), 0), (int(maxPixels), height-1), green, 2) # red
    cv2.rectangle(frame0,(x0_exp,y0_exp),(x0_exp+w0_exp,y0_exp+h0_exp),red,2)
        # expanded int hit box from line 450
        # This frame0 with rectangle is for this loop.
        # The next CSRT update is done on frame0 of next loop that
        # does not have a rectangle yet
    cv2.rectangle(frame0,(x0,y0),(x0+w0,y0+h0),red,2)
        # not expanded, not reduced from lines 457-460    
    cv2.rectangle(frame0,(x0_red,y0_red),(x0_red+w0_red,y0_red+h0_red),red,2)
        # template box, reduced, from lines 464-467, 319
        
    cv2.rectangle(frame2,(x2_red,y2_red),(x2_red+w2_red,y2_red+h2_red),red,2)
        # template hit, reduced, line 472
    cv2.rectangle(frame2,(roiLeft,roiTop),(roiRight,roiBottom),yellow,2)
        # search area roi2, lines 

    roiLeft = max(int(x2_red - 3*w2_red/2),0)
    roiRight  = min(int(x2_red + 5*w2_red/2),sliceWidth02-1)
    roiTop = max(int(y2_red - h2_red),0)
    roiBottom = min(int(y2_red + 2*h2_red),sliceHeight02-1)    

    frame02 = np.hstack((frame0, frame2))
    frame025 = np.vstack((frame02, frame5))
    
    if fc2 > faceNum:          
        cv2.putText(frame025,'time {:.3f} of {} s'.format(t_raw2_[fc2-faceNum-1],timeLimit),
                (2,data1), font, fsize, black, fBold, LT)
            # current t_raw2_ index = fc2-faceNum-1.
            # When fc2 = faceNum+1, fc2-faceNum-1 = 0
        cv2.putText(frame025,'fc2 {} of {} frames'.format(fc2, recordFrames),
                (2,data2), font, fsize, black, fBold, LT)
        cv2.putText(frame025,'z0_raw {:.2f} pix'.format(z0_raw),
                (2,data3), font, fsize, black, fBold, LT)
        cv2.putText(frame025,'z2_raw {:.2f} pix'.format(z2_raw),
                (2,data4), font, fsize, black, fBold, LT)        
        cv2.putText(frame025,'ang0 {:.3f} deg'.format(ang0),
                (2,data5), font, fsize, black, fBold, LT)
        cv2.putText(frame025,'ang2 {:.3f} deg'.format(ang2),
                (2,data6), font, fsize, black, fBold, LT)        
        cv2.putText(frame025,'A {:.3f} deg'.format(A),
                (2,data7), font, fsize, black, fBold, LT)
        cv2.putText(frame025,'B {:.3f} deg'.format(B),
                (2,data8), font, fsize, black, fBold, LT)
        
        cv2.putText(frame025,'C {:.3f} deg'.format(C),
                (col1,data1), font, fsize, black, fBold, LT)            
        cv2.putText(frame025,'a {:.3f} m'.format(a),
                (col1,data2), font, fsize, black, fBold, LT)   
        cv2.putText(frame025,'b {:.3f} m'.format(b),
                (col1,data3), font, fsize, black, fBold, LT)             
        cv2.putText(frame025,'dep_raw {:.3f} m'.format(dep_raw),
                (col1,data4), font, fsize, black, fBold, LT)
        cv2.putText(frame025,'ang1_raw {:.3f} deg'.format(ang1_raw),
                (col1,data5), font, fsize, black, fBold, LT)    
        cv2.putText(frame025,'mov_raw {:.3f} m'.format(mov_raw),
                (col1,data6), font, fsize, black, fBold, LT)         
        cv2.putText(frame025,'movCum_raw {:.3f} m'.format(movCum_raw),
                (col1,data7), font, fsize, black, fBold, LT)          
        cv2.putText(frame025,'dt_raw {:.3f} s'.format(dt_raw),
                (col1,data8), font, fsize, black, fBold, LT)
        
        cv2.putText(frame025,'speed_raw {:.3f} m/s'.format(speed_raw),
                (col2,data1), font, fsize, black, fBold, LT)
        if fc2 > faceNum+1:
            cv2.putText(frame025,'minPixels {:.2f}'.format(minPixels),
                    (col2,data2), font, fsize, green, fBold, LT)        
            cv2.putText(frame025,'maxPixels {:.2f}'.format(maxPixels),
                    (col2,data3), font, fsize, green, fBold, LT)        
            cv2.putText(frame025,'startPixels {:.2f}'.format(startPixels),
                    (col2,data5), font, fsize, orange, fBold, LT)
            cv2.putText(frame025,'start_i {}'.format(start_i),
                    (col2,data7), font, fsize, black, fBold, LT)
            
            cv2.putText(frame025,'endPixels {:.2f}'.format(endPixels),
                    (col2,data6), font, fsize, orange, fBold, LT)
            cv2.putText(frame025,'end_i {}'.format(end_i),
                    (col2,data8), font, fsize, black, fBold, LT)      
        
    cv2.imshow('frame025',frame025)    
    
    if fc2 == faceNum:
        print ('\nline', line(), ', imshow(frame025)')
        print ('line', line(), ', frame0.shape = ', frame0.shape)
        print ('line', line(), ', frame2.shape = ', frame2.shape)
        print ('line', line(), ', frame02.shape = ', frame02.shape)
        print ('line', line(), ', frame5.shape = ', frame5.shape)
        print ('line', line(), ', frame025.shape = ', frame025.shape)
        continue
       
    out025.write(frame025) # the above continue command makes out025.write() start at fc2=1
    
    keyC = cv2.waitKey(1) & 0xFF
    if keyC == ord("q"): # press 'q' key to break early
        print ('line', line(), ', pressed "q"')
        break
    
cap0.release() # begin ending 3rd while loop
cap2.release()
out025.release()
cv2.destroyAllWindows()

print ('\nline', line(), ', start_i, minPixels, startPixels = {}, {:.3f}, {:.3f}' \
                .format(start_i, minPixels, startPixels))
                
print ('\nline', line(), ', end_i, maxPixels, endPixels = {}, {:.3f}, {:.3f}' \
                .format(end_i, maxPixels, endPixels))

# CALCULATIONS AND FILTERING
t_ = t_raw2_
elapsedTime = t_[end_i]-t_[start_i] # see line 286 for n1,n2,n3,n4
if pattern == 0:
    n1,n2,n3,n4 = 21,21,21,21 # 31,31,31,31 # 59,59,59,59 # 29,29,29,29 # n values for 2 filters: medFilter7, smooth7, medFilter7. 
    # See lines 506-514, 539.
    # n values for 4 filters: medFilter7, aveReduct & timeReduct, smooth7
    # suggest n1,n2 about 1/2 or 2/3 fps
elif pattern == 1:
    n1,n2,n3,n4 = 51,51,51,51
print ('\nn1,n2,n3,n4,elapsedTime = ', n1,n2,n3,n4,elapsedTime)
if pattern == 1 or pattern == 0:
    normTime = 4 # for elapsedTime above normTime, n1,n2,n3,n4 are proportionally increased
    n1 = max(n1,n1+2*int(n1*(elapsedTime-normTime)/(2*normTime)))
    n2 = max(n2,n2+2*int(n2*(elapsedTime-normTime)/(2*normTime)))
    n3 = max(n3,n3+2*int(n3*(elapsedTime-normTime)/(2*normTime)))
    n4 = max(n4,n4+2*int(n4*(elapsedTime-normTime)/(2*normTime)))
else:
    n1,n2,n3,n4 = 59,59,59,59
print ('\nn1,n2,n3,n4,elapsedTime = ', n1,n2,n3,n4,elapsedTime)

z0_raw3_ = smooth7(z0_raw_,n1,rt)
z0_raw4_ = medFilter7(z0_raw3_,n2,rt)
z0_raw5_ = smooth7(z0_raw4_,n3,rt)
# z0_raw6_ = medFilter7(z0_raw5_,n4,rt)
z0_ = z0_raw5_

z2_raw3_ = smooth7(z2_raw_,n1,rt)
z2_raw4_ = medFilter7(z2_raw3_,n2,rt)
z2_raw5_ = smooth7(z2_raw4_,n3,rt)
# z2_raw6_ = medFilter7(z2_raw5_,n4,rt)
z2_ = z2_raw5_

# GET ang1_ AND dep_ FROM FILTERED z0_ AND z2_, NOT RAW

for i in range(len(t_)):
    ang0 = (sliceWidth02/2 - z0_[i]) * dpp02
    ang2 = (sliceWidth02/2 - z2_[i]) * dpp02        
    A = 90 + ang0
    B = 90 - ang2
    C = 180 - A - B
    a = c * sin(radians(A)) / sin(radians(C)) # subject distance from right camera
    b = c * sin(radians(B)) / sin(radians(C)) # subject distance from left camera
    Cx = b*cos(radians(ang0))
    Cy = b*sin(radians(ang0)) + half_c
    ang11 = atan2(Cy,Cx) # radians
    ang1 = degrees(ang11) # degrees
        
    ddep = sqrt(b**2 + half_c**2 - 2*b*half_c*cos(radians(A))) # detected depth
    # dep = ddep
    xxx = ddep*cos(ang11+angHalf) # ang11 & angHalf=0.2940013 are in radians
    yyy = ddep*sin(ang11+angHalf) # angHalf=0.2940013 is a shift so that angle0 = 0
    
    dep = rrr_f(xxx,yyy)[0]
        # corrected depth, subject distance from center camera
        
    ang1_.append(ang1) # subject angle position, center camera
    dep_.append(dep) # (depth array), subject distance from center camera
    ddep_.append(ddep)

# GET 2-POINT DATA FROM ang1_, dep_, AND t_ (FROM FILTERED z0_ AND z2_, NOT RAW)
for i in range(len(t_)):        
    if i == 0:
        mov = 0.0
        dt = 0.0        
        speed = 0.0
        movCum = 0.0
    else:
        mov = adjFactor2*polar_dist_moved(dep_[i], \
            dep_[i-1], ang1_[i], ang1_[i-1])
        movCum = movCum + mov
        dt = t_[i] - t_[i-1]
        speed = mov / dt
    mov_.append(mov)
    movCum_.append(movCum)
    dt_.append(dt)
    speed2_.append(speed)

speed_ = medFilter7(speed2_,3,rt) # speed_ needs extra filtering because it is very noisy

t_ = [x-t_[start_i] for x in t_]
movCum_ = [x-movCum_[start_i] for x in movCum_]

# 1-point list lengths
print ('\nline', line())
print ('1-point list lengths')
print ('len(t_raw_), len(t_raw2_), len(t_), len(fc2_) = {}, {}, {}, {}' \
               .format(len(t_raw_), len(t_raw2_), len(t_), len(fc2_)))
print ('len(z0_raw_), len(z2_raw_), len(z0_), len(z2_) = {}, {}, {}, {}' \
               .format(len(z0_raw_), len(z2_raw_), len(z0_), len(z2_)))
print ('len(ang0_), len(ang2_) = {}, {}'.format(len(ang0_), len(ang2_)))
print ('len(C_), len(a_), len(b_) = {}, {}, {}' \
               .format(len(C_), len(a_), len(b_)))
print ('len(dep_raw_), len(dep_), len(ang1_raw_), len(ang1_) = {}, {}, {}, {}' \
               .format(len(dep_raw_), len(dep_), len(ang1_raw_), len(ang1_)))

# 2-point list lengths
print ('\n2-point list lengths')
print ('len(mov_raw_), len(mov_), len(movCum_raw_),len(movCum_) = {}, {}, {}, {}' \
                        .format(len(mov_raw_), len(mov_), len(movCum_raw_),len(movCum_)))
print ('len(dt_raw_), len(dt_), len(speed_raw_), len(speed_) = {}, {}, {}, {}' \
                        .format(len(dt_raw_), len(dt_), len(speed_raw_), len(speed_)))

# LIST LENGTH NOTES
print ('Number of frames used for data is len(t_raw_)-faceNum-1:', \
       len(t_raw_), '-',faceNum, '-', 1, ' = ', len(t_raw_)-faceNum-1)

# WRITE LINES TO gaitSpeedError.csv FILE

distance = movCum_[end_i]-movCum_[start_i]
aveSpeed = distance/elapsedTime
distanceFromSpeed = distance_from_speed_(t_[start_i:end_i+1], speed_[start_i:end_i+1])
aveSpeedFromSpeed = distanceFromSpeed / elapsedTime    

if correctDist != 0.0:
    error = 100 * (distance - correctDist) / correctDist
    print ('\nerror = {:.2f}%'.format(error))
else:
    error = 0.0

with open("/home/pi/md4/TXT_CSV/gaitSpeedError.csv", 'r') as f:
    mycsv = csv.reader(f) # # mycsv may be all the lines as 1 string
    mycsv = list(mycsv) # mycsv is a list of line strings
    run = int(mycsv[-1][0]) # The -1 line is the last line.
                            # The 0 character is the 1st character.
                            # run is the 1st character on the last line
    errorTotal = 0.0
    if run > 0:
        for my in mycsv[-run:]:
            # mycsv[-run:] is the lines from -run to the last line.
            # -run is the index of the lines starting from the last line and going up.
            # If run=2, then -2 is the index of the line above the last line, and
            #    -1 is the index of the last line.
            # The -run: would be for an iteration thru the last 2 lines.
            errorTotal = errorTotal + abs(float(my[4])) # my[4] is the the index 4 character
                # (5th character) on each line.
    errorTotal = errorTotal + abs(error)
    aveAbsError = errorTotal / (run + 1)
    print ('aveAbsError = {:.2f}%'.format(aveAbsError))    

f = open("/home/pi/md4/TXT_CSV/gaitSpeedError.csv", "a")  
if run == 0:
    f.write('Run,Time stamp,Correct distance,Detected distance,Error,aveAbsError,' \
        + 'Time,Average speed,Average speed from speed,,Doctor,Patient ID,,setupTime,recordTime,' \
        + 'processTime,totalTime\n')    
    f.write('(run),(y-m-d h:m:s),(m),(m),(%),(%),(s),(m/s),(m/s),,,,,(s),(s),(s),(s)\n')
run += 1 # get current run number
runStr = str(run)
f.write('{},'.format(run))
f.write('{},'.format(stamp))
f.write('{:.3f},'.format(correctDist))
f.write('{:.3f},'.format(distance))
f.write('{:.3f},'.format(error))
f.write('{:.3f},'.format(aveAbsError))
f.write('{:.3f},'.format(elapsedTime))
f.write('{:.3f},'.format(aveSpeed))
f.write('{:.3f},,'.format(aveSpeedFromSpeed))
f.write('{},'.format(doctor))
f.write('{},,'.format(patientID)) # lack of \n because line continues near end of program
f.close()

# WRITE LINES TO gaitSpeed.csv FILE, RAW DATA FIRST
fcsv = open("/home/pi/md4/TXT_CSV/gaitSpeed.csv", "a")  
fcsv.write('\n,run,' + runStr + '\n')
fcsv.write(stamp + ',,')
fcsv.write('fps =,{:.3f},,'.format(record_fps))

fcsv.write('time =,{:.3f},,'.format(elapsedTime))
fcsv.write('distance =,{:.3f},,'.format(distance))
fcsv.write('ave speed =,{:.3f}\n'.format(aveSpeed))

fcsv.write('t_raw2,fc2,z0_raw,z2_raw,ang0,ang2,C,a,b,dep_raw,' \
           + 'ang1_raw,mov_raw,movCum_raw,dt_raw,speed_raw\n')
fcsv.write('(s),(frame),(pix),(pix),(deg),(deg),(deg),(m),(m),(m),' \
           + '(deg),(m),(m),(s),(m/s)\n')
for fc in range(len(t_raw2_)-1):      
    fcsv.write('{:.3f},'.format(t_raw2_[fc]))
    fcsv.write('{},'.format(fc2_[fc]))    
    fcsv.write('{:.3f},'.format(z0_raw_[fc]))
    fcsv.write('{:.3f},'.format(z2_raw_[fc]))
    fcsv.write('{:.3f},'.format(ang0_[fc]))
    fcsv.write('{:.3f},'.format(ang2_[fc]))  
    fcsv.write('{:.3f},'.format(C_[fc]))    
    
    fcsv.write('{:.3f},'.format(a_[fc]))
    fcsv.write('{:.3f},'.format(b_[fc]))    
    fcsv.write('{:.3f},'.format(dep_raw_[fc]))
    fcsv.write('{:.3f},'.format(ang1_raw_[fc]))        
    fcsv.write('{:.3f},'.format(mov_raw_[fc]))    
    fcsv.write('{:.3f},'.format(movCum_raw_[fc]))  
    fcsv.write('{:.3f},'.format(dt_raw_[fc]))
    fcsv.write('{:.3f}\n'.format(speed_raw_[fc]))      
fcsv.write('t_raw2,fc2,z0_raw,z2_raw,ang0,ang2,C,a,b,dep_raw,' \
           + 'ang1_raw,mov_raw,movCum_raw,dt_raw,speed_raw\n')
fcsv.write('(s),(frame),(pix),(pix),(deg),(deg),(deg),(m),(m),(m),' \
           + '(deg),(m),(m),(s),(m/s)\n')

# CONTINUE WRITING LINES TO gaitSpeed.csv FILE, FILTERED DATA
fcsv.write('\nt,fc2,z0,z2,dep,ang1,mov,movCum,dt,speed\n')
fcsv.write('(s),(frame),(pix),(pix),(m),(deg),(m),(m),(s),(m/s)\n')
for fc in range(len(t_)-1):      
    fcsv.write('{:.3f},'.format(t_[fc]))
    fcsv.write('{},'.format(fc2_[fc]))    
    fcsv.write('{:.3f},'.format(z0_[fc]))
    fcsv.write('{:.3f},'.format(z2_[fc]))
    
    fcsv.write('{:.3f},'.format(dep_[fc]))
    fcsv.write('{:.3f},'.format(ang1_[fc]))
    fcsv.write('{:.3f},'.format(mov_[fc]))
    fcsv.write('{:.3f},'.format(movCum_[fc]))
    fcsv.write('{:.3f},'.format(dt_[fc]))
    fcsv.write('{:.3f}\n'.format(speed_[fc]))
fcsv.write('\nt,fc2,z0,z2,dep,ang1,mov,movCum,dt,speed\n')
fcsv.write('(s),(frame),(pix),(pix),(m),(deg),(m),(m),(s),(m/s)\n')
fcsv.close()

# INCLUDE ALL BELOW FOR PLOTTING FROM PICKLE

runZfill = str(run).zfill(3)
    # new run number as string, but padded on left with zeros to have 3 digits

runStr1 = '/home/pi/runs/' + stamp + ' ' + runZfill + ' Fig 1.png'
runStr2 = '/home/pi/runs/' + stamp + ' ' + runZfill + ' Fig 2.png'
runStr3 = '/home/pi/runs/' + stamp + ' ' + runZfill + ' Fig 3.png'
runStr4 = '/home/pi/runs/' + stamp + ' ' + runZfill + ' Fig 4.png'


# SMOOTHED RECTANGULAR PLOTS OF WALKING DISTANCE AND SPEED
# if showPlots == 1 and update_count > 0:
# plot for frame,distance traveled, and speed versus time
import matplotlib as mpl
import matplotlib.pyplot as plt

# from matplotlib.pyplot import figure, show, grid, tight_layout
vw = 13 # vertical line width
vw2 = 18
vw3 = 23
f4 = plt.figure(figsize=(60, 30)) # inches wide, inches high
mpl.rcParams['font.size'] = 84 # 24
mpl.rcParams['axes.linewidth'] = 8.0
mpl.rcParams['grid.linewidth'] = 8.0
plt.subplot(1,2,1)
plt.plot(t_, movCum_, linestyle='solid', linewidth=24, color='darkblue', \
         label='Distance\nWalked (m)')
plt.axvline(x=t_[start_i], linestyle='dashed', linewidth=24)
plt.axvline(x=t_[end_i], linestyle='dashed', linewidth=24)
plt.axhline(y=correctDist, linestyle='dashed', linewidth=24)
plt.text(-0.9, correctDist-0.75, 'Correct Distance\n{:.3f} m'.format(correctDist))
plt.text(-0.9, correctDist-1.75, 'Detected\n{:.3f} m, {:.3f} s'.format(distance,elapsedTime))
plt.title("Total Distance Walked",pad=30)
plt.xlabel('Time (s)',labelpad=10)
plt.ylabel('Total Distance Walked (m)',labelpad=10)
if ceil(max(t_))+1 - floor(min(t_)) < 13:    
    x_start = floor(min(t_))
    x_end = ceil(max(t_))+1
    x_inc = 1.0
elif ceil(max(t_))+1 - floor(min(t_)) < 21:       
    x_start = floorn(min(t_),2)
    x_end = ceiln(max(t_),2)+1
    x_inc = 2.0
else:   
    x_start = floorn(min(t_),4)
    x_end = ceiln(max(t_),4)+1
    x_inc = 4.0
print ('\nint(x_inc) =', int(x_inc))
# plt.minorticks_on()
# plt.grid(which='minor')

plt.xticks(np.arange(x_start, x_end, x_inc))
plt.tick_params('x', pad=30.0) # pad is space between tick labels & grid
plt.tick_params('y', pad=30.0) # pad is space between tick labels & grid
plt.grid()
# plt.legend(prop={'size':42},ncol=1,labelspacing=0.5,columnspacing=0.5,frameon=False, \
           # bbox_to_anchor=(1.3,0.1))
    # sets legend font size, number of columns, row spacing, space between columns, 
    # legend box show or not (contents still there)
mpl.rcParams['legend.loc'] = 'lower center' # 'upper left'
plt.legend()

plt.subplot(1,2,2)
plt.fill_between(t_[start_i:end_i+1], speed_[start_i:end_i+1], color='lightgreen')
plt.plot(t_, speed_, linestyle='solid', linewidth=24, color='darkblue', label='Speed (m/s)')
plt.axhline(y=aveSpeed, linewidth=36, color='red', label='Ave Speed 1')
plt.axhline(y=aveSpeedFromSpeed, linestyle=(0,(0.01,2.5)), linewidth=78, \
            dash_capstyle='round', color='orange', label='Ave Speed 2')
plt.axvline(x=t_[start_i], linestyle='dashed', linewidth=24)
plt.axvline(x=t_[end_i], linestyle='dashed', linewidth=24)
plt.title("Walking Speed",pad=30)
plt.xlabel('Time (s)',labelpad=10)
plt.ylabel('Walking Speed (m/s)',labelpad=10)
# plt.minorticks_on()
# plt.grid(which='minor')

plt.xticks(np.arange(x_start, x_end, x_inc))
plt.tick_params('x', pad=30.0) # pad is space between tick labels & grid
plt.tick_params('y', pad=30.0) # pad is space between tick labels & grid
plt.grid()
mpl.rcParams['legend.loc'] = 'lower center' # 'lower center'
plt.legend()

# legend.get_frame().set_linewidth(0.5)
f4.subplots_adjust(wspace=0.35) # wspace=width space, 0.4 is relative to a supplot width
plt.savefig(runStr1, bbox_inches='tight')
# plt.show()
plt.close()


if fast != 1: # fast = 1 means not taking time to make this plot
    # UNSMOOTHED RECTANGULAR PLOTS OF WALKING DISTANCE AND SPEED
    f5 = plt.figure(figsize=(60, 30)) # inches wide, inches high
    mpl.rcParams['font.size'] = 84 # 24
    mpl.rcParams['axes.linewidth'] = 8.0
    mpl.rcParams['grid.linewidth'] = 8.0
    plt.subplot(1,2,1)
    plt.get_current_fig_manager().full_screen_toggle()
    plt.plot(t_raw2_, movCum_raw_, linestyle='solid', linewidth=24, \
                                     label='Total Distance Walked (m)')
    plt.axvline(x=t_[start_i], linestyle='dashed', linewidth=24)
    plt.axvline(x=t_[end_i], linestyle='dashed', linewidth=24)
    plt.title("Total Distance Walked, raw",pad=30)
    plt.xlabel('Time (s)',labelpad=10)
    plt.ylabel('Total Distance Walked (m)',labelpad=10)
    # plt.minorticks_on()
    # plt.grid(which='minor')

    plt.xticks(np.arange(x_start, x_end, x_inc))
    plt.grid()
    plt.legend()

    plt.subplot(1,2,2)
    plt.fill_between(t_[start_i:end_i+1], speed_raw_[start_i:end_i+1], color='lightblue')
    plt.plot(t_raw2_, speed_raw_, linestyle='solid', linewidth=24, label='Speed (m/s)')
    plt.axvline(x=t_[start_i], linestyle='dashed', linewidth=24)
    plt.axvline(x=t_[end_i], linestyle='dashed', linewidth=24)
    plt.title("Walking Speed, raw",pad=30)
    plt.xlabel('Time (s)',labelpad=10)
    plt.ylabel('Walking Speed (m/s)',labelpad=10)
    # plt.ylim((0,6))
    # plt.minorticks_on()
    # plt.grid(which='minor')

    plt.xticks(np.arange(x_start, x_end, x_inc))
    plt.grid()
    plt.legend()
    f4.subplots_adjust(wspace=0.35) # wspace=width space, 0.4 is relative to a supplot width
    # plt.tight_layout(pad=4.0)
    plt.savefig(runStr3, bbox_inches='tight')
    # plt.show()
    plt.close()


# POLAR PLOTS OF PATHS

mpl.rcParams['font.size'] = 84 # 18
mpl.rcParams['axes.linewidth'] = 8.0
mpl.rcParams['grid.linewidth'] = 8.0
ang1_raw_rad_ = [radians(x) for x in ang1_raw_]
ang1_rad_ = [radians(x) for x in ang1_]
# p_ang_unique = np.unique(ptheta_arr)
p_ang_unique_ = np.unique([0.0])

# SMOOTHED POLAR PLOT
f2 = plt.figure(figsize=(50, 40))
ax2 = f2.add_subplot(111, polar=True)

# Walk patterns
# path = "homeRad"
if path == "home4m":
    theta1_in,theta2_in,r1_in,r2_in,distance_in = 15.8966, -15.8966, 7.1334, 6.0008, 3.7588
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -15,15,-20,20,7,7.5
elif path == "homeRad":
    theta1_in,theta2_in,r1_in,r2_in,distance_in = 15.8966, -15.8966, 2.4354, 5.7169, 3.8661
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -15,15,-20,20,6,6.5
elif path == "home3m":
    theta1_in,theta2_in,r1_in,r2_in,distance_in = 17.4865, -17.4865, 4.9394, 4.0005, 2.8316    
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -15,15,-20,20,5,5.5
elif path == "Mom":
    theta1_in,theta2_in,r1_in,r2_in,distance_in = 25.6167, -25.6167, 4.4360, 4.4360, 3.8358
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -25,25,-27,27,4,5
elif path == "UAB":
    theta1_in,theta2_in,r1_in,r2_in,distance_in = 21.9286, -21.9286, 5.1097, 5.1097, 3.8164
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -20,20,-24,24,5,5.5
elif path == "hosp":
    theta1_in,theta2_in,r1_in,r2_in,distance_in = 17.4866, -17.4866, 6.2907, 6.2907, 3.7805
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -20,20,-20,20,6,6.5
print ('path = ', path)
ang_ = [radians(theta1_in),radians(theta2_in)]
rad_ = [r1_in,r2_in]
ax2.plot(ang_, rad_, '.-', linewidth=24, markersize=90, color='blue', label='Walk Pattern')     

if pattern == 1:
    ax2.plot(ang1_rad_[start_i:end_i], dep_[start_i:end_i], linestyle='dashed', linewidth=24, \
        color='red', label='Walk Detected')
else:
    ax2.plot(ang1_rad_[start_i:end_i], dep_[start_i:end_i], linestyle='solid', linewidth=24, \
    color='red', label='Walk Detected')

"""
# OPTIONAL PLOT POINTS
ax2.plot(ang1_rad_[0:start_i], dep_[0:start_i], linestyle='solid', linewidth=16, \
         color='purple', label='Walk, Before start')
ax2.plot(ang1_rad_[end_i:], dep_[end_i:], linestyle='solid', linewidth=16, \
         color='green', label='Walk, After end')
"""
for zz in range(len(p_ang_unique_)):
    ax2.arrow(radians(p_ang_unique_[zz]),0,0,1.7,length_includes_head=True,linewidth=10.0, \
              head_length=0.2,edgecolor="black",facecolor="black",head_width=0.08,overhang=0.3)
if pattern == 0:
    draw_arrow2(ax2) # arrow for walking direction
if pattern == 1:
    draw_arrow(ax2) # arrow for walking direction

ax2.set_aspect('equal')

yticks = yticksmax+1
ax2.set_yticks(np.linspace(0,yticksmax,yticks))
ax2.set_rmax(rmax)
ax2.set_rmin(0)

xticks = int((xticksmax-xticksmin)/5+1)
ax2.set_xticks(pi/180 * np.linspace(xticksmin,xticksmax,xticks))
ax2.set_thetamin(thetamin)
ax2.set_thetamax(thetamax)

ax2.tick_params('x', pad=100.0) # x is angles. pad is space between tick labels & grid
ax2.tick_params('y', pad=30.0) # y is radii. pad is space between tick labels & grid

ax2.set_xlabel('Angle Theta',rotation=90)
ax2.xaxis.set_label_coords(1.15,0.63)

ax2.text(0.15,0.35,'Distance from Center Camera, r (m)',rotation=360+thetamin, \
             transform=ax2.transAxes,ha='center',va='top')

ax2.text(0.0,0.65,'Camera\nPlatform',transform=ax2.transAxes)
ax2.text(0.0,0.80,'Arrow Shows Camera\nPlatform Direction', \
         transform=ax2.transAxes,ha='left',va='center')
ax2.set_axisbelow(True)
plt.legend(loc='lower left',bbox_to_anchor=(1.1,0.75),frameon=False)
# plt.grid()
plt.tight_layout(pad=0.0)
plt.savefig(runStr2, bbox_inches='tight')
# plt.show()
plt.close()

if fast != 1:
    # UNSMOOTHED POLAR PLOT
    f3 = plt.figure(figsize=(50, 40))
    ax3 = f3.add_subplot(111, polar=True)
    
    # Walk patterns
    ax3.plot(ang_, rad_, '.-', linewidth=12, markersize=45, color='blue', label='Walk Pattern') 

    ax3.plot(ang1_raw_rad_[start_i:end_i], dep_raw_[start_i:end_i], linestyle='solid', \
             linewidth=12, color='orange', label='Walk Detected')
    """    
    # OPTIONAL PLOT POINTS
    ax3.plot(ang1_raw_rad_[0:start_i], dep_raw_[0:start_i], linestyle='solid', linewidth=24, \
             color='purple', label='Walk, Before start')
    ax3.plot(ang1_raw_rad_[end_i:], dep_raw_[end_i:], linestyle='solid', linewidth=24, \
             color='green', label='Walk, After end')
    """
    for zz in range(len(p_ang_unique_)):
        ax3.arrow(radians(p_ang_unique_[zz]),0,0,1.7,length_includes_head=True, \
            linewidth=10.0,head_length=0.2,edgecolor="black",facecolor="black", \
            head_width=0.08,overhang=0.3) 
    if pattern == 0:
        draw_arrow2(ax3) # arrow for walking direction 
    if pattern == 1:
        draw_arrow(ax3) # arrow for walking direction    
    
    ax3.set_aspect('equal')

    # yticks = yticksmax+1
    ax3.set_yticks(np.linspace(0,yticksmax+2,yticks+2))
    ax3.set_rmax(rmax+2)
    ax3.set_rmin(0)

    # xticks = int((xticksmax-xticksmin)/5+1)
    ax3.set_xticks(pi/180 * np.linspace(xticksmin,xticksmax,xticks))
    ax3.set_thetamin(thetamin)
    ax3.set_thetamax(thetamax)


    ax3.tick_params('x', pad=100.0) # x is angles. pad is space between tick labels & grid
    ax3.tick_params('y', pad=30.0) # y is radii. pad is space

    ax3.set_xlabel('Angle Theta',rotation=90)
    ax3.xaxis.set_label_coords(1.15,0.63)

    ax3.text(0.15,0.35,'Distance from Center Camera, r (m)',rotation=360+thetamin, \
                 transform=ax3.transAxes,ha='center',va='top')
    ax3.text(0.0,0.65,'Camera\nPlatform',transform=ax3.transAxes)
    ax3.text(0.0,0.80,'Arrow Shows Camera\nPlatform Direction', \
             transform=ax3.transAxes,ha='left',va='center')
    ax3.set_axisbelow(True)
    plt.legend(loc='lower left',bbox_to_anchor=(1.1,0.75),frameon=False)
    # plt.grid()
    plt.tight_layout(pad=0.0)
    plt.savefig(runStr4, bbox_inches='tight')
    # plt.show()
    plt.close()

print ('Time = {:.3f}'.format(elapsedTime))
print ('Distance = {:.3f}'.format(distance))
print ('Average speed = {:.3f}'.format(aveSpeed))
print ('Average speed from speed = {:.3f}'.format(aveSpeedFromSpeed))

print ('t_raw_[0], t_raw_[len(t_raw_)-1] = {:.3f}, {:.3f}'.format(t_raw_[0], t_raw_[len(t_raw_)-1]))

processTime = time() - processStart
totalTime = time() - setupStart
processFrames = fc2 + faceNum + 1 # frames in process video
print ('\nsetupTime, recordTime, processTime = {:.3f} s, {:.3f} s, {:.3f} s' \
       .format(setupTime, recordTime, processTime))
print ('recordFrames, processFrames = ', recordFrames, processFrames, 'Should be same')
totalTimeCheck = setupTime + recordTime + processTime
print ('totalTime, totalTimeCheck = {:.3f} s, {:.3f} s'.format(totalTime, totalTimeCheck))

f = open("/home/pi/md4/TXT_CSV/gaitSpeedError.csv", "a")  
f.write('{:.3f},'.format(setupTime))
f.write('{:.3f},'.format(recordTime))
f.write('{:.3f},'.format(processTime))
f.write('{:.3f}\n'.format(totalTime))
f.close()

picklePath = '/home/pi/pickle/gaitSpeed' + stamp + '.pkl'
# os.mkdir(picklePath)
dataList="dataList,t_,movCum_,start_i,end_i,speed_,aveSpeed,aveSpeedFromSpeed,run," \
          + "t_raw2_,movCum_raw_,speed_raw_,angHalf,ang1_,dep_,ang1_raw_,pattern," \
          + "dep_raw_,distance,elapsedTime"
dataSet=[dataList,t_,movCum_,start_i,end_i,speed_,aveSpeed,aveSpeedFromSpeed,run, \
          t_raw2_,movCum_raw_,speed_raw_,angHalf,ang1_,dep_,ang1_raw_,pattern, \
          dep_raw_,distance,elapsedTime]
with open(picklePath,'wb') as f:
    pickle.dump(dataSet,f)
    
print ('record_fps = {:.3f} frames/second for new fps'.format(record_fps))
print ('Set fps = {:.3f} frames/second'.format(fps))

print ('ALL DONE\n\n')

