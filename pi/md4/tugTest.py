# tugTest.py (adapted from tugTest_vs0.py)
# Standing at 4 m distance, set camera level about 25 cm lower than eye level, or
# Set vertical angle at 18 degrees relative to floor marker at 3.5 m distance.
# camera angle y=-2 with marker height = camera height
# It uses the center camera.
# Subject sits in a chair at 4m distance, stands, walks towards cameras
# until reaching 1m distance, about face, return to chair, about face, sits.
# Follow the screen prompts.
import numpy as np
import cv2
from time import time, sleep
from datetime import datetime
from imutils.video import VideoStream
import imutils
from math import floor, ceil
import pickle

print (__file__)
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('/home/pi/md4/haarcascades/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
frame_count = 0
# cap = cv2.VideoCapture(0)
fps = 22
fwidth = 1280
fheight = 320
sliceWidth = 320
sliceLeft = (fwidth - sliceWidth) // 2
sliceRight = sliceWidth + sliceLeft
cue_y_position = int(round(300.0*fheight/960.0))
cue_y_position2 = int(round(420.0*fheight/960.0))
frame_y_position = int(round(680.0*fheight/960.0))
time_y_position = int(round(800.0*fheight/960.0))
time_y_position2 = int(round(920.0*fheight/960.0))
y0 = None
startTime = None
elapsedTime = 0.0
videoStart = 0.0
started = False
ended = False
timeLimit = 160.0
fontColor = (0,255,255)
fontColor2 = (0,255,255)
fontSize = 0.7
mark = None
searchArea = None
saLeft = 0 # for search area
saRight = fwidth-1
saTop = 0
saBottom = fheight-1
sideMargin = 7
vertFactor = 40
extraStartTime = None
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

tugTest = '/home/pi/runsTUG/'+ stamp + ' tugTest.avi'
tugFig = '/home/pi/runsTUG/'+ stamp + ' tugTest.png'
vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out1 = cv2.VideoWriter(tugTest,fourcc, fps, (sliceWidth,fheight))
    # frame rate = 12.13 give approximately normal playback speed.
    
sleep(1.0) # Self testing: sleep(6.0). Testing others: sleep(1.0)
while 1:
    frame_count += 1
    frame11 = vs1.read() # center PiCamera
    if frame_count == 1:
        videoStart = time()
        print ('frame11.shape =', frame11.shape)

    frame1 = frame11[:,sliceLeft:sliceRight]
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    if frame_count == 1:
        print ('gray.shape =', gray.shape) # gray.shape = (480, 640)
        
    searchArea = gray[saTop:saBottom,saLeft:saRight]
    faces = face_cascade.detectMultiScale(searchArea, 1.3, 5)            
    
    for (x,y,w,h) in faces:
        # draw rectangle around face
        cv2.rectangle(frame1,(x+saLeft,y+saTop),(x+saLeft+w,y+saTop+h),(255,255,0),2)
        x0 = x+saLeft
        y0 = y+saTop
        w0 = w
        h0 = h    

    # If y0 is not None, then the face has been found one or more times
    if y0:
        
        # set horizontal mark above top of head when sitting at start
        # the timer does not start
        if mark == None and started == False:
            mark = y0 - h0//2
            saLeft = x0-sideMargin*w0//10 # for search area
            saRight = x0+(10+sideMargin)*w0//10
            saTop = max(0,y0-vertFactor*h0//10)
            saBottom = min(fheight-1,y0+17*h0//10)
            
        # Case of face detected above mark at start while starting to stand.
        # the timer was not running, but starts now
        if started == False and y0 < mark:
            startTime = time()
            fontColor = (0,255,0)
            started = True
            print ('standing up,', '  y0 = ', y0, '  mark = ', mark)            
            # saTop = max(0,mark)
            
        # get data for plot
        if y0:        
            t_.append(time())
            y0_.append(y0)
        
        # Case of face detected below mark near end while starting to sit.
        if started == True and ended == False and y0 > mark:
            ended = True
            elapsedTime = time() - startTime
            fontColor = (0,0,255)
            extraStartTime = time()
            print ('1. ended = True, sat down,', '  y0 = ', y0, '  mark = ', mark)
            
    if startTime and ended == False:
        elapsedTime = time() - startTime
    
    # put text on screen
    if started == False and mark == None:
        cv2.putText(frame1,'Sit and face camera',(0,cue_y_position),
            font, fontSize, fontColor, 2, cv2.LINE_AA)
    if started == False and mark:
        cv2.putText(frame1,'Stand up and keep',(0,cue_y_position),
            font, fontSize, fontColor, 1, cv2.LINE_AA)        
        cv2.putText(frame1,'facing camera',(0,cue_y_position2),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
    if started == True and ended == False:
        cv2.putText(frame1,'Continue and face',(0,cue_y_position),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
        cv2.putText(frame1,'camera at end',(0,cue_y_position2),
            font, fontSize, fontColor, 1, cv2.LINE_AA)
    if ended == True:
        cv2.putText(frame1,'Test is complete',(0,cue_y_position),
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

    if extraStartTime:
        extraTime = time() - extraStartTime

    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key == ord("q"): # press 'q' key to break loo early
        print ('pressed "q"')
        break
    if ended == True and extraTime > 1.0:
        print ('2. ended = True, sat down')
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
f = open("/home/pi/md4/TXT_CSV/tugTest.txt", "a")
f.write('\n' + stamp + '\n')
f.write('{:.3f} s\n'.format(elapsedTime))
f.close()

# WRITE TO CSV FILE
f2 = open("/home/pi/md4/TXT_CSV/tugTest.csv", "a")
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
plt.plot(t_, y0_, '.-', linewidth=16, markersize=60, color='darkblue', label='Sitting,\nStanding,\nWalking')
plt.text(1.5*elapsedTime, mark2, 'Start\nStop\nLevel')   
plt.axhline(y=mark2, linestyle='dashed', linewidth=20)
plt.axvline(x=elapsedTime, linestyle='dashed', linewidth=20)
plt.text(1.5*elapsedTime, 0.91, 'Time')
plt.text(1.5*elapsedTime, 0.81, '{:.3f} s'.format(elapsedTime))
plt.title("Sitting, Standing, Walking\n(normalized 0 to 1)",pad=30)
plt.xlabel('Time (s)',labelpad=10)
plt.ylabel('Sitting, Standing, Walking\n(normalized 0 to 1)',labelpad=10)
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
mpl.rcParams['legend.loc'] = 'center'
plt.grid()
plt.legend()

plt.savefig(tugFig, bbox_inches='tight')
    # bbox_inches='tight' keeps label at edge from being trimmed out
# plt.show()
plt.close()

picklePath = '/home/pi/pickle/tugTest' + stamp + '.pkl'
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
