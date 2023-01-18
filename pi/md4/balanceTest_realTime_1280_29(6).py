# balanceTest.py (adapted from tugTest_vs0.py)
# It uses the center camera.
# Subject looks down and stands at distance of 4 m.
# Subject looks up to face camera. Head must not be tilted down at start. Time starts.
# Subject tries to stand without moving the feet.
# Shifting other body parts and arms to stay balanced is okay.
# Follow the screen prompts.
import numpy as np
import cv2
from time import time, sleep
from datetime import datetime
from imutils.video import VideoStream
import imutils
from math import floor, ceil, pi
from inspect import currentframe, getframeinfo

print (__file__)
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('/home/pi/md4/haarcascades/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
frame_count = 0
# cap = cv2.VideoCapture(0)
fps = 1.5 # SET fps = 2.0 OR HIGHER IF THERE IS A VIDEO RECORDING PROBLEM
fwidth = 1280
fheight = 960
sliceWidth = 200
sliceLeft = (fwidth - sliceWidth) // 2
sliceRight = sliceWidth + sliceLeft

sliceHeight = 500
sliceTop = (fheight - sliceHeight) // 2
sliceBottom = sliceHeight + sliceTop

cue_y_position = int(round(400.0*sliceHeight/960.0))
time_y_position = int(round(500.0*sliceHeight/960.0))
fc_y_position = int(round(600.0*sliceHeight/960.0))

useHead = True
y1 = None
startTime = None
elapsedTime = 0.0
videoStart = 0.0
ended = False
timeLimit = 20.0
fontsize2 = 0.7
fontBoldness2 = 2
blue, green, yellow = (255,0,0), (0,255,0), (0,255,255)
red, black, white = (0,0,255), (0,0,0), (255,255,255)
extraStartTime = None
extraTime = None
faceFound = False
passThreshold = False
threshold = 20 # millimeters (mm)
headThreshold = 25 # millimeters (mm)
LL0,RR0,UU0,DD0 = 3,-7,-73,75 # for tracker0 viewed on left
LL2,RR2,UU2,DD2 = -7,3,-73,75 # for tracker2 viewed on right
LL1,RR1,UU1,DD1 = 3,3,3,3 # for tracker1 viewed on head
LL,RR,UU,DD = 3,3,-73,75 # for rectangle containing trackers 0 & 2

h_field_of_view = 63.6 # PiCamera degrees wide, original 62.2
    # Zealinno webcam left/right 60.7
dpp = h_field_of_view / fwidth # dpp = degrees/pixel
mpp = 8.544*pi*dpp/360 # (meters/degree)*dpp = meters/pixel
headmpp = 8.004*pi*dpp/360 # (headMeters/degree)*dpp = headMeters/pixel
"""
Floor distance = 4 m. Vertical distance = 1.5 m (height difference of camera and ankle)
Distance = sqrt(4**2 + 1.5**2) = 4.272 m
At 4 m, Circumference C = 2*pi*4.272 = 8.544*pi
meters/degree = C/360 = 8.544*pi/360.
mpp = (meters/degree)*dpp = meters/pixel = 8.544*pi*dpp/360
meters moved = mpp*pixels

headDistance = sqrt(4**2 + 0.12**2) = 4.002 m
At 4 m, headCircumference headC = 2*pi*4.002 = 8.004*pi
headMeters/degree = headC/360 = 8.004*pi/360.
headmpp = (headMeters/degree)*dpp = headMeters/pixel = 8.004*pi*dpp/360
headMeters moved = headmpp*pixels

"""
t_ = []
x0_f_ = []
y0_f_ = []
x1_f_ = []
y1_f_ = []
x2_f_ = []
y2_f_ = []

# floor to multiple of n
def floorn(x,n):
    y = n*floor(x/n)
    return y

# ceil to multiple of n
def ceiln(x,n):
    y = n*ceil(x/n)
    return y

def line():
    cf = currentframe()
    return cf.f_back.f_lineno

tracker0 = cv2.TrackerCSRT_create() # foot viewed on left
if useHead == True:
    tracker1 = cv2.TrackerCSRT_create() # head viewed
tracker2 = cv2.TrackerCSRT_create() # foot viewed on right
balanceTest = '/home/pi/runsBalance/'+ stamp + ' balanceTest.avi'
balanceFig = '/home/pi/runsBalance/'+ stamp + ' balanceTest.png'
vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out1 = cv2.VideoWriter(balanceTest,fourcc, fps, (sliceWidth,sliceHeight))
print('\nsliceWidth,sliceHeight = ', sliceWidth,sliceHeight)
sleep(6.0)

while 1:
    frame_count += 1
    frame11 = vs1.read() # center PiCamera
    if frame_count == 1:
        videoStart = time()
        print ('frame11.shape =', frame11.shape)
    
    # find face in frame1 with haar cascades
    if faceFound == False:
        gray11 = cv2.cvtColor(frame11, cv2.COLOR_BGR2GRAY) # gray11_exp is enlarged also
        
        if frame_count == 1:
            print ('line', line(), ', FACE FINDING STAGE')
            print ('gray11.shape =', gray11.shape)

        # FIND FACE POSITION IN frame1
        faces = face_cascade.detectMultiScale(gray11, 1.3, 5)
        if len(faces) == 0:
            frame1 = frame11[sliceTop:sliceBottom,sliceLeft:sliceRight]
            
            cv2.putText(frame1,'Face camera',
                    (2,cue_y_position), font, fontsize2, yellow, fontBoldness2, cv2.LINE_AA)
            cv2.putText(frame1,'Frame = {}'.format(frame_count),
                    (2,fc_y_position), font, fontsize2, yellow, fontBoldness2, cv2.LINE_AA)

            cv2.imshow('frame1',frame1)
            print('\nline', line(), ', frame1.shape = ', frame1.shape)
            out1.write(frame1)

            key0 = cv2.waitKey(1) & 0xFF
            if key0 == ord("q"): # press 'q' key to break early
                print ('line', line(), ', pressed "q"')
                break
            print ('No face, frame1, frame_count = ', frame_count)
            continue # go to next while loop
        
        startTime = time()
        t_.append(startTime)
        elapsedTime = t_[0] - startTime # 0.0
        num = len(faces)
        xx,yy,ww,hh = 0,0,0,0
        
        # EVERYTHING FROM HERE IS frame11 with size (fwidth,fheight)
        for (x,y,w,h) in faces: # (x,y,w,h) is a tuple containing type int     
            xx,yy,ww,hh = xx+x,yy+y,ww+w,hh+h
        xx1_f,yy1_f,ww1_f,hh1_f = xx/num,yy/num,ww/num,hh/num
            # float averages & scale back to original size, HEAD
            # face without background from unexpanded rectangle in frame1/gray1            
        xx1,yy1,ww1,hh1 = int(xx1_f), int(yy1_f), int(ww1_f), int(hh1_f) # unexpanded int box, HEAD
        

        print ('\nline', line(), ',    float averages: xx1_f,yy1_f,ww1_f,hh1_f = ', \
               xx1_f,yy1_f,ww1_f,hh1_f)
        print ('\nline', line(), ',      int averages: xx1,yy1,ww1,hh1 = ', \
               xx1,yy1,ww1,hh1)
        print ('line', line(), ',        expand numbers0: LL0,RR0,UU0,DD0 =', LL0,RR0,UU0,DD0)
        print ('line', line(), ',        expand numbers2: LL2,RR2,UU2,DD2 =', LL2,RR2,UU2,DD2)
        print ('line', line(), ',        expand numbers1: LL1,RR1,UU1,DD1 =', LL1,RR1,UU1,DD1)
        print ('line', line(), ',        expand numbers: LL,RR,UU,DD =', LL,RR,UU,DD)

        x3_11_f,y3_11_f,w3_11_f,h3_11_f = xx1_f-LL*ww1_f/10, yy1_f-UU*hh1_f/10, \
                  (10+LL+RR)*ww1_f/10, (10+UU+DD)*hh1_f/10 # shifted float box, FEET
        x3_11, y3_11, w3_11, h3_11 = int(x3_11_f), int(y3_11_f), \
                        int(w3_11_f), int(h3_11_f) # shifted int box, FEET

        x0_11_f,y0_11_f,w0_11_f,h0_11_f = xx1_f-LL0*ww1_f/10, yy1_f-UU0*hh1_f/10, \
            (10+LL0+RR0)*ww1_f/10, (10+UU0+DD0)*hh1_f/10 # shifted float box, FOOT VIEWED ON LEFT
        x0_11, y0_11, w0_11, h0_11 = int(x0_11_f), int(y0_11_f), \
            int(w0_11_f), int(h0_11_f) # shifted int box, FOOT VIEWED ON LEFT
        
        x2_11_f,y2_11_f,w2_11_f,h2_11_f = xx1_f-LL2*ww1_f/10, yy1_f-UU2*hh1_f/10, \
            (10+LL2+RR2)*ww1_f/10, (10+UU2+DD2)*hh1_f/10 # shifted float box, FOOT VIEWED ON RIGHT
        x2_11, y2_11, w2_11, h2_11 = int(x2_11_f), int(y2_11_f), \
            int(w2_11_f), int(h2_11_f) # shifted int box, FOOT VIEWED ON RIGHT
        
        if useHead == True:
            x1_11_f,y1_11_f,w1_11_f,h1_11_f = xx1_f-LL1*ww1_f/10, yy1_f-UU1*hh1_f/10, \
                (10+LL1+RR1)*ww1_f/10, (10+UU1+DD1)*hh1_f/10 # shifted float box, HEAD
            x1_11, y1_11, w1_11, h1_11 = int(x1_11_f), int(y1_11_f), \
                int(w1_11_f), int(h1_11_f) # shifted int box, HEAD
        
        # last time these are set
        sliceBottom = int(min(y3_11_f+h3_11_f+20,fheight-1))        
        sliceTop = int(max(sliceBottom-sliceHeight,0))
        sliceLeft = int(max(x3_11_f+w3_11_f/2-sliceWidth/2,0))
        sliceRight = int(min(x3_11_f+w3_11_f/2+sliceWidth/2,fwidth-1))
        
        frame1 = frame11[sliceTop:sliceBottom,sliceLeft:sliceRight]
        print ('line', line(), ', frame1.shape =', frame1.shape)
        
        # get coordinates for frame1 tracker0 which is reduced to size (sliceWidth,sliceHeight)
        x0_f, y0_f, w0_f, h0_f = x0_11_f-sliceLeft, y0_11_f-sliceTop, w0_11_f, h0_11_f
        bb0 = (x0_f, y0_f, w0_f, h0_f) 
            # shifted float box for CSRT initialization, FOOT VIEWED ON LEFT
        x0, y0, w0, h0 = int(x0_f), int(y0_f), int(w0_f), int(h0_f)
            # shifted int box for rectangle, FOOT VIEWED ON LEFT
        print ('line', line(), ',      shifted int box: x0, y0, w0, h0 = ', \
                x0, y0, w0, h0)
        print ('shifted float box (bb0): x0_f, y0_f, w0_f, h0_f = ', \
               x0_f, y0_f, w0_f, h0_f)
        print ('                                          bb0 =',bb0)        
        
        # get coordinates for frame1 tracker2 which is reduced to size (sliceWidth,sliceHeight)
        x2_f, y2_f, w2_f, h2_f = x2_11_f-sliceLeft, y2_11_f-sliceTop, w2_11_f, h2_11_f
        bb2 = (x2_f, y2_f, w2_f, h2_f) 
            # shifted float box for CSRT initialization, FOOT VIEWED ON RIGHT
        x2, y2, w2, h2 = int(x2_f), int(y2_f), int(w2_f), int(h2_f)
            # shifted int box for rectangle, FOOT VIEWED ON RIGHT
        print ('line', line(), ',      shifted int box: x2, y2, w2, h2 = ', \
                x2, y2, w2, h2)
        print ('shifted float box (bb1): x2_f, y2_f, w2_f, h2_f = ', \
               x2_f, y2_f, w2_f, h2_f)
        print ('                                          bb2 =',bb2)        
        
        if useHead == True:
            # get coordinates for frame1 tracker1 which is reduced to size (sliceWidth,sliceHeight)
            x1_f, y1_f, w1_f, h1_f = x1_11_f-sliceLeft, y1_11_f-sliceTop, w1_11_f, h1_11_f
            bb1 = (x1_f, y1_f, w1_f, h1_f) 
                # shifted float box for CSRT initialization, HEAD
            x1, y1, w1, h1 = int(x1_f), int(y1_f), int(w1_f), int(h1_f)
                # shifted int box for rectangle, HEAD
            print ('line', line(), ',      shifted int box: x1, y1, w1, h1 = ', \
                    x1, y1, w1, h1)
            print ('shifted float box (bb1): x1_f, y1_f, w1_f, h1_f = ', \
                   x1_f, y1_f, w1_f, h1_f)
            print ('                                          bb1 =',bb1)

        # initialize the frame1 trackers at the faceNum frame
        tracker0.init(frame1,bb0)
        
        if useHead == True:
            tracker1.init(frame1,bb1)
            
        tracker2.init(frame1,bb2)
            # frame1, bb0, & bb2 exist. bb0 & bb2 are downward-shifted float box input, line 482
        print ('line', line(), ', TRACKERS 0, (1), & 2 INITIATED')        
        faceFound = True

        x0_f_.append(x0_f+w0_f/2)
        y0_f_.append(y0_f+h0_f/2)
        x0_0 = x0_f_[0]
        y0_0 = y0_f_[0]        
        
        x2_f_.append(x2_f+w2_f/2)
        y2_f_.append(y2_f+h2_f/2)
        x2_0 = x2_f_[0]
        y2_0 = y2_f_[0]        
        
        if useHead == True:
            x1_f_.append(x1_f+w1_f/2)
            y1_f_.append(y1_f+h1_f/2)
            x1_0 = x1_f_[0]
            y1_0 = y1_f_[0]        
        
        
        # DRAW FACE & FEET RECTANGLES ON frame1.
        cv2.rectangle(frame1, (x0, y0), (x0+w0, y0+h0), green, 2)
            # shifted int box, FOOT VIEWED ON LEFT
        cv2.rectangle(frame1, (x2, y2), (x2+w2, y2+h2), green, 2)
            # shifted int box, FOOT VIEWED ON RIGHT
        
        if useHead == True:
            cv2.rectangle(frame1, (x1, y1), (x1+w1, y1+h1), green, 2)
                # int box, HEAD, line 378
        
        # WRITE TEXT ON frame1.
        cv2.putText(frame1,'Face found',(2,cue_y_position),
            font, fontsize2, green, 1, cv2.LINE_AA)        
        cv2.putText(frame1,'Time = {:.2f} s'.format(elapsedTime),(2,time_y_position),
            font, fontsize2, green, 1, cv2.LINE_AA)
        cv2.putText(frame1,'Frame = {}'.format(frame_count),(2,fc_y_position),
            font, fontsize2, green, 1, cv2.LINE_AA)
        
        cv2.imshow('frame1',frame1)
        print('\nline', line(), ', frame1.shape = ', frame1.shape)
        out1.write(frame1)
        
        key1 = cv2.waitKey(1) & 0xFF
        if key1 == ord("q"): # press 'q' key to break early
            print ('line', line(), ', pressed "q"')
            break
        print ('Face found, frame1, frame_count = ', frame_count)
        
        continue

    ### END OF 1ST LOOP ### END OF 1ST LOOP ### END OF 1ST LOOP ###    
    
    ### START OF UPDATE LOOPS ### START OF UPDATE LOOPS ### START OF UPDATE LOOPS ###

    # Note that tracker.init() was done
    # near end of FACE FINDING STAGE for frame1
    # update the frame1 trackers at all frames after that rame
    frame1 = frame11[sliceTop:sliceBottom,sliceLeft:sliceRight]
    
    (success0,box0) = tracker0.update(frame1)
    if not success0:
        print ('line', line(), ', frame1 TRACKING FAILURE')
        cv2.putText(frame1,'Time = {:.2f} s'.format(elapsedTime),(2,time_y_position),
            font, fontsize2, red, 1, cv2.LINE_AA)
        cv2.putText(frame1,'FAIL frame = {}'.format(frame_count),
            (2,cue_y_position), font, fontsize2, red, fontBoldness2, cv2.LINE_AA)
        cv2.imshow('frame1',frame1)
        print('\nline', line(), ', frame1.shape = ', frame1.shape)
        out1.write(frame1)
        
        key2 = cv2.waitKey(1) & 0xFF
        if key2 == ord("q"): # press 'q' key to break early
            print ('line', line(), ', pressed "q"')
            break
        break
    x0_f, y0_f, w0_f, h0_f = box0 # CSRT keeps track of this for each update, FEET
    (x0, y0, w0, h0) = [int(a) for a in box0]
        # these ints are used for rectangle, FOOT VIEWED ON LEFT        
    
    (success2,box2) = tracker2.update(frame1)
    if not success2:
        print ('line', line(), ', frame1 TRACKING FAILURE')
        cv2.putText(frame1,'Time = {:.2f} s'.format(elapsedTime),(2,time_y_position),
            font, fontsize2, red, 1, cv2.LINE_AA)
        cv2.putText(frame1,'FAIL frame = {}'.format(frame_count),
            (2,cue_y_position), font, fontsize2, red, fontBoldness2, cv2.LINE_AA)
        cv2.imshow('frame1',frame1)
        print('\nline', line(), ', frame1.shape = ', frame1.shape)
        out1.write(frame1)
        
        key2B = cv2.waitKey(1) & 0xFF
        if key2B == ord("q"): # press 'q' key to break early
            print ('line', line(), ', pressed "q"')
            break
        break
    x2_f, y2_f, w2_f, h2_f = box2 # CSRT keeps track of this for each update, FEET
    (x2, y2, w2, h2) = [int(a) for a in box2]
        # these ints are used for rectangle, FOOT VIEWED ON RIGHT        

    
    if useHead == True:
        (success1,box1) = tracker1.update(frame1)
        if not success1:
            print ('line', line(), ', frame1 TRACKING FAILURE')
            cv2.putText(frame1,'Time = {:.2f} s'.format(elapsedTime),(2,time_y_position),
                font, fontsize2, red, 1, cv2.LINE_AA)
            cv2.putText(frame1,'FAIL frame = {}'.format(frame_count),
                (2,cue_y_position), font, fontsize2, red, fontBoldness2, cv2.LINE_AA)
            cv2.imshow('frame1',frame1)
            print('\nline', line(), ', frame1.shape = ', frame1.shape)
            out1.write(frame1)
            
            key2C = cv2.waitKey(1) & 0xFF
            if key2C == ord("q"): # press 'q' key to break early
                print ('line', line(), ', pressed "q"')
                break
            break
        x1_f, y1_f, w1_f, h1_f = box1 # CSRT keeps track of this for each update, HEAD
        (x1, y1, w1, h1) = [int(a) for a in box1]
            # these ints are used for rectangle, HEAD      

    cv2.rectangle(frame1,(x0,y0),(x0+w0,y0+h0),red,2)
        # shifted int hit box, FOOT VIEWED ON LEFT        
    
    cv2.rectangle(frame1,(x2,y2),(x2+w2,y2+h2),red,2)
        # shifted int hit box, FOOT VIEWED ON RIGHT
    
    
    if useHead == True:
        cv2.rectangle(frame1,(x1,y1),(x1+w1,y1+h1),red,2)
            # shifted int hit box, HEAD    
    
    t_.append(time())
    x0_f_.append(x0_f+w0_f/2)
    y0_f_.append(y0_f+h0_f/2)
    x2_f_.append(x2_f+w2_f/2)
    y2_f_.append(y2_f+h2_f/2) 
    
    if useHead == True:
        x1_f_.append(x1_f+w1_f/2)
        y1_f_.append(y1_f+h1_f/2)
        
    x0Var = 1000*mpp*abs(x0_0 - x0_f-w0_f/2)
    y0Var = 1000*mpp*abs(y0_0 - y0_f-h0_f/2)
    x2Var = 1000*mpp*abs(x2_0 - x2_f-w2_f/2)
    y2Var = 1000*mpp*abs(y2_0 - y2_f-h2_f/2)
    
    if useHead == True:
        x1Var = 1000*headmpp*abs(x1_0 - x1_f-w1_f/2)
        y1Var = 1000*headmpp*abs(y1_0 - y1_f-h1_f/2)

    if useHead == True:
        if x0Var > threshold or y0Var > threshold or x2Var > threshold or y2Var > threshold \
                                          or x1Var > headThreshold or y1Var > headThreshold:
            passThreshold = True
    else:
        if x0Var > threshold or y0Var > threshold or x2Var > threshold or y2Var > threshold:
            passThreshold = True
    if ended == False:
        elapsedTime = t_[len(t_)-1] - startTime
        if elapsedTime >= 10 or passThreshold:
            ended = True
            if elapsedTime >= 10 and passThreshold == False:
                elapsedTime = t_[len(t_)-1] - startTime            
            if passThreshold == True:
                elapsedTime = t_[len(t_)-2] - startTime
            
    # put text on screen
    if faceFound == False:
        cv2.putText(frame1,'Face camera',(2,cue_y_position),
            font, fontsize2, yellow, 1, cv2.LINE_AA)
    if faceFound == True and ended == False:        
        cv2.putText(frame1,'Stand still',(2,cue_y_position),
            font, fontsize2, yellow, 1, cv2.LINE_AA)
    if ended == True:
        cv2.putText(frame1,'Test is done',(2,cue_y_position),
            font, fontsize2, red, 1, cv2.LINE_AA)
        if extraStartTime == None:
            extraStartTime = time()

    cv2.putText(frame1,'Time = {:.2f} s'.format(elapsedTime),(2,time_y_position),
        font, fontsize2, yellow, 1, cv2.LINE_AA)
    cv2.putText(frame1,'Frame = {}'.format(frame_count),(2,fc_y_position),
        font, fontsize2, yellow, 1, cv2.LINE_AA)

    cv2.imshow('frame1',frame1)
    print('\nline', line(), ', frame1.shape = ', frame1.shape)
    out1.write(frame1)

    if extraStartTime:
        extraTime = time() - extraStartTime

    key3 = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key3 == ord("q"): # press 'q' key to break loo early
        print ('pressed "q"')
        break
    if ended == True:
        if extraTime > 2:
            print ('ended = True, reached 10 seconds')
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
f = open("/home/pi/md4/TXT_CSV/balanceTest.txt", "a")
f.write('\n' + stamp + '\n')
f.write('{:.2f} s\n'.format(elapsedTime))
f.close()

# WRITE TO CSV FILE
f2 = open("/home/pi/md4/TXT_CSV/balanceTest.csv", "a")
f2.write(stamp + ',{:.2f},'.format(elapsedTime) + doctor + ',' + patientID + '\n')
f2.close()

sleep(4)
vs1.stop()
out1.release()
cv2.destroyAllWindows()
# (x-x1_0) is x pixel difference between initial point & present point
# 1000*mpp*(x-x1_0) is x difference between initial point & present point in mm
# see lines 60-69 for more about mpp (meters per pixel) 
t_ = [x-startTime for x in t_]
x0_mm_ = [1000*mpp*(x-x0_0) for x in x0_f_]
y0_mm_ = [-1000*mpp*(y-y0_0) for y in y0_f_] # "-1000" makes negative y0_mm mean down
x2_mm_ = [1000*mpp*(x-x2_0) for x in x2_f_]
y2_mm_ = [-1000*mpp*(y-y2_0) for y in y2_f_]

if useHead == True:
    x1_mm_ = [1000*headmpp*(x-x1_0) for x in x1_f_]
    y1_mm_ = [-1000*headmpp*(y-y1_0) for y in y1_f_]

# SMOOTHED RECTANGULAR PLOTS OF WALKING DISTANCE AND SPEED
# if showPlots == 1 and update_count > 0:
# plot for frame,distance traveled, and speed versus time
import matplotlib as mpl
import matplotlib.pyplot as plt
vw = 13
# from matplotlib.pyplot import figure, show, grid, tight_layout
vw = 9 # vertical line width
f4 = plt.figure(figsize=(30, 30)) # inches wide, inches high
mpl.rcParams['font.size'] = 60 # 24
mpl.rcParams['axes.linewidth'] = 8.0
mpl.rcParams['grid.linewidth'] = 8.0
plt.subplot(1,1,1)
plt.plot(t_, x0_mm_, '.-', linewidth=16, markersize=60, color='blue', \
         label='Left foot x')
plt.plot(t_, y0_mm_, '.-', linewidth=16, markersize=60, color='green', \
         label='Left foot y')
plt.plot(t_, x2_mm_, '.-', linewidth=16, markersize=60, color='orange', \
         label='Right foot x')
plt.plot(t_, y2_mm_, '.-', linewidth=16, markersize=60, color='red', \
         label='Right foot y')
if useHead == True:    
    plt.plot(t_, x1_mm_, '.-', linewidth=16, markersize=60, color='black', \
             label='Head x')
    plt.plot(t_, y1_mm_, '.-', linewidth=16, markersize=60, color='purple', \
             label='Head y')    
    plt.text(6.3, -headThreshold+0.3, 'headThreshold')
    plt.text(6.3, headThreshold+0.3, 'headThreshold')    
    plt.axhline(y=-headThreshold, linewidth=vw)
    plt.axhline(y=headThreshold, linewidth=vw)
    
plt.text(6.3, -threshold+0.3, 'Threshold')
plt.text(6.3, threshold+0.3, 'Threshold')
plt.text(elapsedTime+0.1, 20.3, 'Time')
plt.axvline(x=elapsedTime, linewidth=vw)
plt.axhline(y=-threshold, linewidth=vw)
plt.axhline(y=threshold, linewidth=vw)
plt.title("Standing Balance Test\nx and y Position Variations (mm), " \
          + "\nStart Point Normalized to 0)",pad=30)
plt.xlabel('Time (s)',labelpad=10)
plt.ylabel('Standing Balance Test\nLeft foot, Right Foot, and Head, ' \
        + 'x and y Positions (mm), \nStart Point Normalized to 0)',labelpad=10)
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
mpl.rcParams['legend.loc'] = 'upper left'
plt.grid()
plt.legend()

plt.savefig(balanceFig, bbox_inches='tight')
    # bbox_inches='tight' keeps label at edge from being trimmed out
# plt.show()
plt.close()

print ('\nALL DONE\n')
