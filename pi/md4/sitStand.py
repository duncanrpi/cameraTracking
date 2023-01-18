# sitStand.py (adapted from tugTest.py). Sit about 2.0 m from camera
# Set vertical angle at 12 degrees relative to floor marker at 3.5 m distance.

import numpy as np
import cv2
from time import time, sleep
from datetime import datetime
from imutils.video import VideoStream
import argparse
from math import floor, ceil
import pickle

print (__file__)
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('count', type=int, nargs="?", default=5, \
    help="The first value is an int for counting standing & sitting")
args = ap.parse_args()
count = args.count # angle in degrees
c = 0 # present count

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('/home/pi/md4/haarcascades/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
frame_count = 0
fps = 20.0
fwidth = 640 # 1280
fheight = 368 # 960
sliceWidth = 320
sliceLeft = (fwidth - sliceWidth) // 2
sliceRight = sliceWidth + sliceLeft
cue_y_position = int(round(300.0*fheight/960.0))
cue_y_position2 = int(round(420.0*fheight/960.0))
count_y_position = int(round(560.0*fheight/960.0))
frame_y_position = int(round(680.0*fheight/960.0))
time_y_position = int(round(800.0*fheight/960.0))
time_y_position2 = int(round(920.0*fheight/960.0))

y0 = None
startTime = None
elapsedTime = 0.0
started = False
standing = False # standing = False means sitting
previous_standing = False
ended = False
timeLimit = 160.0
fontColor = (0,255,255)
fontColor2 = (0,255,255)
fontSize = 0.8
mark = None
searchArea = None
saLeft = 0 # for search area
saRight = fwidth-1
saTop = 0
saBottom = fheight-1
sideMargin = 7
vertFactor = 40

# mark = int(round(400.0*fheight/960.0))
extraStartTime = None
extraTime = 0.0
videoTime = 0.0
videoStart = 0.0
videoDuration = 0.0

t_ = []
y0_ = []

# floor to multiple of n
def floorn(x,n):
    y = n*floor(x/n)
    return y

# ceil to multiple of n
def ceiln(x,n):
    y = n*ceil(x/n)
    return y

sitStand = '/home/pi/runsSitStand/'+ stamp + ' sitStand.avi'
sitStandFig = '/home/pi/runsSitStand/'+ stamp + ' sitStand.png'

vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out1 = cv2.VideoWriter(sitStand,fourcc, fps, (sliceWidth,fheight))
    # frame rate = 9.42 gives approximately normal playback speed.
    
sleep(1.0) # Self testing: sleep(6.0). Testing others: sleep(1.0)
while 1:
    frame_count += 1
    # frame1 = cap.read()
    frame11 = vs1.read() # center PiCamera
    if frame_count == 1:
        videoStart = time()
        print ('frame11.shape =', frame11.shape) # frame11.shape = (480, 640, 3)

    frame1 = frame11[:,sliceLeft:sliceRight]
    if frame_count == 1:
        print ('frame1.shape =', frame1.shape) # frame1.shape = (480, 480, 3)

    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    if frame_count == 1:
        print ('gray.shape =', gray.shape) # gray.shape = (480, 640)

    searchArea = gray[saTop:saBottom,saLeft:saRight]
    faces = face_cascade.detectMultiScale(searchArea, 1.3, 5)

    yGet = False
    for (x,y,w,h) in faces:
        cv2.rectangle(frame1,(x+saLeft,y+saTop),(x+saLeft+w,y+saTop+h),(255,255,0),2)
        # roi_gray = gray[y+saTop:y+saTop+h, x+saLeft:x+saLeft+w]
        # roi_color = frame1[y+saTop:y+saTop+h, x+saLeft:x+saLeft+w]
        if yGet == False:
            x0 = x+saLeft
            y0 = y+saTop
            w0 = w
            h0 = h
            yGet = True
        
    # get data for plot
    if y0:        
        t_.append(time())
        y0_.append(y0)
        
    if ended == False:        
        # update elapsedTime
        if startTime:
            elapsedTime = time() - startTime
            
        if y0:
            # set horizontal mark above top of head
            if mark == None and started == False:
                mark = y0 - h0//2              
                saLeft = x0-sideMargin*w0//10 # for search area
                saRight = x0+(10+sideMargin)*w0//10
                saTop = max(0,y0-vertFactor*h0//10)
                saBottom = min(fheight-1,y0+17*h0//10)
                
            # update started and get startTime as person starts standing 1st time            
            if started == False and y0 < mark:
                started = True
                startTime = time()
                standing = True
                print ('started')
                
            # update standing
            if started == True:
                if y0 > mark:
                    # print ('103 y0 > mark', '  y0 = ', y0, '  mark = ', mark)
                    standing = False
                    # print ('105 standing = ', standing)
                    # print ('106 previous_standing = ', previous_standing)
                    if previous_standing == True:
                        c += 1
                        # print ('109 c = ', c)
                        previous_standing = False
                        # print ('111 previous_standing = ', previous_standing)                
                else:
                    # print ('113')
                    # print ('114 y0 <= mark', '  y0 = ', y0, '  mark = ', mark)
                    standing = True
                    previous_standing = True
                    
        # update ended
        if c == count:
            ended = True
            extraStartTime = time()
            print ('ended')
        
    # update fontcolor
    if started == True:
        if ended == False:
            fontColor = (0,255,0)
        else:
            fontColor = (0,0,255)
            
    # update extratTime
    if extraStartTime:
        extraTime = time() - extraStartTime        
    
    # put text on screen
    if started == False and mark == None:
        cv2.putText(frame1,'Sit and face',(0,cue_y_position),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
        cv2.putText(frame1,'camera',(0,cue_y_position2),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
    if started == False and mark:
        cv2.putText(frame1,'Begin and keep',(0,cue_y_position),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
        cv2.putText(frame1,'facing camera',(0,cue_y_position2),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
    if started == True and ended == False:
        cv2.putText(frame1,'Continue and keep',(0,cue_y_position),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
        cv2.putText(frame1,'facing camera',(0,cue_y_position2),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
    if ended == True:
        cv2.putText(frame1,'Test is complete',(0,cue_y_position),
            font, fontSize, fontColor, 1, cv2.LINE_AA)        
        
    cv2.putText(frame1,'Count = {} of {}'.format(c, count),(0,count_y_position),
        font, fontSize, fontColor, 1, cv2.LINE_AA)
    cv2.putText(frame1,'Frame = {}'.format(frame_count),(0,frame_y_position),
        font, fontSize, fontColor, 1, cv2.LINE_AA)
    cv2.putText(frame1,'Elapsed time = {:.3f} s'.format(elapsedTime),(0,time_y_position),
        font, fontSize, fontColor, 1, cv2.LINE_AA)
    cv2.putText(frame1,'Record time = {:.3f} s'.format(time()-videoStart),(0,time_y_position2),
        font, fontSize, fontColor2, 1, cv2.LINE_AA)
    if mark:
        cv2.line(frame1, (0, mark), (fwidth-1, mark), (0, 255, 255), 2)
    cv2.rectangle(frame1,(saLeft,saTop),(saRight,saBottom),(255,255,0),2)
    cv2.imshow('frame1',frame1)
    out1.write(frame1)

    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key == ord("q"): # press 'q' key to break loo early
        print ('pressed "q"')
        break
    if extraTime > 1.0:
        print ('extraTime = ', extraTime)
        videoDuration = time() - videoStart
        print ('videoDuration = ', videoDuration)
        break
    if elapsedTime > timeLimit:
        print ('reached time limit = ', timeLimit, ' s')
        break

recordTime = time() - videoStart
recordFrames = frame_count
record_fps = recordFrames/recordTime
print ('recordTime = {:.3f} s'.format(recordTime))
print ('recordFrames = ', recordFrames)
print ('record_fps = {:.3f} frames/second for new fps'.format(record_fps))
print ('Set fps = {:.3f} frames/second'.format(fps))


# GET DOCTOR & PATIENT NAMES
b_file = open("/home/pi/md4/TXT_CSV/doctor.txt", "r")
lines = b_file. readlines()
doctor = lines[-1][0:-1]
b_file. close()

c_file = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "r")
lines = c_file. readlines()
patientID = lines[-1][0:-1]
c_file. close()

# WRITE TO TXT FILE
f = open("/home/pi/md4/TXT_CSV/sitStand.txt", "a")
f.write('\n' + stamp + '\n')
f.write('{:.3f} s\n'.format(elapsedTime))
f.close()

# WRITE TO CSV FILE
f2 = open("/home/pi/md4/TXT_CSV/sitStand.csv", "a")
f2.write(stamp + ',{:.3f},'.format(elapsedTime) + doctor + ',' + patientID + '\n')
f2.close()

sleep(4)
vs1.stop()
out1.release()
cv2.destroyAllWindows()

t_ = [x-startTime for x in t_]
y0_min = min(y0_)
y0_max = max(y0_)
a = 1 / (y0_min - y0_max)
b = (-a) * y0_max
y0_ = [a*x+b for x in y0_]
mark2 = a*mark+b

# SMOOTHED RECTANGULAR PLOTS OF WALKING DISTANCE AND SPEED
# if showPlots == 1 and update_count > 0:
# plot for frame,distance traveled, and speed versus time
import matplotlib as mpl
import matplotlib.pyplot as plt

# from matplotlib.pyplot import figure, show, grid, tight_layout
vw = 9 # vertical line width
f4 = plt.figure(figsize=(30, 30)) # inches wide, inches high
mpl.rcParams['font.size'] = 108 # 24
mpl.rcParams['axes.linewidth'] = 8.0
mpl.rcParams['grid.linewidth'] = 8.0
plt.subplot(1,1,1)
plt.plot(t_, y0_, '.-', linewidth=16, markersize=60, color='darkblue', label='Sitting,\nStanding')
plt.text(1.5*elapsedTime, mark2, 'Start\nStop\nLevel')   
plt.axhline(y=mark2, linestyle='dashed', linewidth=20)
plt.axvline(x=elapsedTime, linestyle='dashed', linewidth=20)
plt.text(1.5*elapsedTime, 0.91, 'Time')
plt.text(1.5*elapsedTime, 0.81, '{:.3f} s'.format(elapsedTime))
plt.title("Sitting, Standing\n(normalized 0 to 1)",pad=30)
plt.xlabel('Time (s)',labelpad=10)
plt.ylabel('Sitting, Standing\n(normalized 0 to 1)',labelpad=10)
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

plt.xticks(np.arange(x_start, x_end, x_inc))
plt.tick_params('x', pad=27.0) # pad is space between tick labels & grid
plt.tick_params('y', pad=27.0) # pad is space between tick labels & grid
plt.grid()
plt.legend()

plt.savefig(sitStandFig, bbox_inches='tight')
    # bbox_inches='tight' keeps label at edge from being trimmed out
# plt.show()
plt.close()

picklePath = '/home/pi/pickle/sitStand' + stamp + '.pkl'
# os.mkdir(picklePath)
dataList="dataList,t_,y0_,elapsedTime"
dataSet=[dataList,t_,y0_,elapsedTime]
with open(picklePath,'wb') as f:
    pickle.dump(dataSet,f)

"""
# to read the data back into variables with pickle
with open((picklePath, 'rb') as f2:
    # picklePath is a string path ending in a .pkl file (.pickle)
    dataLoad = pickle.load(f2) # must remember order to retreive it properly
dataList,t_ = dataLoad[0],dataLoad[1]
y0_,elapsedTime = dataLoad[2],dataLoad[3]
# now plots can be made
# if variables get mixed up, print (dataList) # dataLoad[0]
"""
print ('\nrecord_fps = {:.3f} frames/second for new fps'.format(record_fps))
print ('Set fps = {:.3f} frames/second'.format(fps))

print ('\nALL DONE\n')
