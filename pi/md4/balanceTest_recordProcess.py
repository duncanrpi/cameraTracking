# balanceTest_recordProcess.py 
# IMPORTANT POINTS:
# Aim camera at crotch level of subject at 4 m distance.
# Paper marker is at 3.5 m.
# Good lighting but not too bright on the marker on the floor.

# It uses the center camera with the subject's closest toes at a distance of 
#    4 m for side-by-side
#    4 m for semi-tandem
#    4 m for tandem
# Subject faces the camera. Time starts.
# Subject tries to stand without moving the feet (or head).
# Shifting other body parts and arms to stay balanced is okay.
# Follow the screen prompts.

from time import sleep, time
setupStart = time()
from imutils.video import VideoStream
from datetime import datetime
import cv2

print (__file__)

fps = 23.0 # SET fps = 2.0 OR HIGHER IF THERE IS A VIDEO RECORDING PROBLEM
fwidth = 1888 # 1840 # 2592 # IT WILL NOT WORK FOR fwidth=1840
fheight = 848 # 1200 # 1088 1136
sliceWidth = 304 # 400 # 320 # 304 # 432 # 496 464
sliceLeft = (fwidth - sliceWidth) // 2
sliceRight = sliceWidth + sliceLeft

sliceHeight = fheight
sliceTop = (fheight - sliceHeight) // 2
sliceBottom = sliceHeight + sliceTop
print('line 45, sliceWidth,sliceHeight =', sliceWidth,sliceHeight)

timeLimit = 12.5
t_ = []

stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
balanceRecord = '/home/pi/runsBalance/'+ stamp + ' balanceRecord.avi'
vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out1 = cv2.VideoWriter(balanceRecord,fourcc, fps, (sliceWidth,sliceHeight))
fc1 = 0

sleep(6.0)
setupTime = time() - setupStart
recordStart = time()
while True:
    frame11=vs1.read()
    fc1 += 1
    if fc1 == 1:
        startTime1 = time()
    t_.append(time() - startTime1)    
    frame1 = frame11[sliceTop:sliceBottom,sliceLeft:sliceRight]
    
    if fc1 == 1:
        print('frame11.shape = ', frame11.shape)
        print('frame1.shape = ', frame1.shape)
        print('sliceWidth,sliceHeight =', sliceWidth,sliceHeight)
    
    out1.write(frame1)
    cv2.imshow('frame1', frame1)
    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if time() - startTime1 > timeLimit or key == ord("q"): # press 'q' key to break loop
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
vs1.stop() # stop() is for VideoStream object
out1.release()


# PROCESSING STAGE

# imports
import numpy as np
from math import floor, ceil, pi
from inspect import currentframe, getframeinfo
import pickle
import os

face_cascade = cv2.CascadeClassifier \
        ('/home/pi/md4/haarcascades/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

sliceWidth2 = 288 # 400
sliceLeft2 = (sliceWidth - sliceWidth2) // 2
sliceRight2 = sliceLeft2 + sliceWidth2 

sliceHeight2 = 832 # 1168
sliceTop2 = (sliceHeight - sliceHeight2) // 2
sliceBottom2 = sliceTop2 + sliceHeight2

print ('\nsliceWidth2, sliceLeft2, sliceRight2 = ', \
       sliceWidth2, sliceLeft2, sliceRight2)
print ('\nsliceHeight2, sliceTop2, sliceBottom2 = ', \
       sliceHeight2, sliceTop2, sliceBottom2)

cue_y_position = int(round(300.0*sliceHeight2/960.0))
time_y_position = int(round(400.0*sliceHeight2/960.0))
fc_y_position = int(round(500.0*sliceHeight2/960.0))

useHead = True
startTime2 = None
elapsedTime = 0.0

ended = False
fontsize2 = round(0.540123*fwidth/1000,1) # fontsize2=1.4 with fwidth=2592
fontBoldness2 = round(1.54321*fwidth/1000) # fontBoldness2=4 with fwidth=2592
blue, green, yellow = (255,0,0), (0,255,0), (0,255,255)
red, black, white = (0,0,255), (0,0,0), (255,255,255)
extraStartTime = None
extraTime = None
faceFound = False
passThreshold = False
footThreshold = 25 # millimeters (mm) 25
headThreshold = 35 # millimeters (mm) 30
LL0,RR0,UU0,DD0 = 50, -10, 160, 0 # for tracker0 viewed on left 3, -6, -84, 98
LL2,RR2,UU2,DD2 = RR0, LL0, UU0, DD0 # for tracker2 viewed on right -6, 3, UU0, DD0
LL1,RR1,UU1,DD1 = 2,2,2,2 # for tracker1 viewed on head
LL,RR,UU,DD = LL0, RR2, UU0, DD0 # for rectangle containing trackers 0 & 2
footWidth = 55
footHeight = 3.4*footWidth
footLevel = 50

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

Floor distance = 4 m. Vertical distance = 0.12 m (height difference of camera and face)
headDistance = sqrt(4**2 + 0.12**2) = 4.002 m
At 4 m, headCircumference headC = 2*pi*4.002 = 8.004*pi
headMeters/degree = headC/360 = 8.004*pi/360.
headmpp = (headMeters/degree)*dpp = headMeters/pixel = 8.004*pi*dpp/360
headMeters moved = headmpp*pixels

"""
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
tracker2 = cv2.TrackerCSRT_create() # foot viewed on right

if useHead == True:
    tracker1 = cv2.TrackerCSRT_create() # head viewed

fc2 = -1 # It counts each frame of PROCESSING STAGE output video
cap1 = cv2.VideoCapture(balanceRecord) # (sliceWidth, sliceHeight) values from Recording stage, lines 20, 24
balanceProcess = '/home/pi/runsBalance/'+ stamp + ' balanceProcess.avi'
balanceFig = '/home/pi/runsBalance/'+ stamp + ' balanceTest.png'

out1p = cv2.VideoWriter(balanceProcess,fourcc,fps,(sliceWidth2,sliceHeight2))
print('\nline', line(), ', out1p, sliceWidth2, sliceHeight2 = {}, {}'.format(sliceWidth2,sliceHeight2))

capSleep = 1.0
sleep(capSleep)
while 1:    
    ret11, frame11p = cap1.read()    
    if frame11p is None:
        print ('line', line(), ', End of video, frame11p is None')
        break
    fc2 += 1
    
    # find face in frame11p with haar cascades
    if faceFound == False:
        gray11p = cv2.cvtColor(frame11p, cv2.COLOR_BGR2GRAY) 
        
        if fc2 == 0:
            print ('line', line(), ', FACE FINDING STAGE')
            print ('gray11p.shape =', gray11p.shape)
            print ('frame11p.shape =', frame11p.shape)    

        # FIND FACE POSITION IN frame11p
        faces = face_cascade.detectMultiScale(gray11p, 1.3, 5)
        if len(faces) == 0:
            frame1p = frame11p[sliceTop2:sliceBottom2,sliceLeft2:sliceRight2]
            
            cv2.putText(frame1p,'Face camera',
                    (2,cue_y_position), font, fontsize2, yellow, fontBoldness2, cv2.LINE_AA)
            cv2.putText(frame1p,'Frame = {}'.format(fc2),
                    (2,fc_y_position), font, fontsize2, yellow, fontBoldness2, cv2.LINE_AA)

            cv2.imshow('frame1p',frame1p)
            print('\nline', line(), ', frame1p.shape = ', frame1p.shape)
            out1p.write(frame1p)

            key0 = cv2.waitKey(1) & 0xFF
            if key0 == ord("q"): # press 'q' key to break early
                print ('line', line(), ', pressed "q"')
                break
            print ('No face, frame1p, fc2 = ', fc2)
            continue # go to next while loop
        
        faceNum = fc2 # faceNum = 0 if successful on first try
        print ('\nfaceNum =', faceNum)
        startTime2 = t_[faceNum]
        elapsedTime = 0.0 # = t_[fc2] - t_[faceNum]
        num = len(faces)
        xx,yy,ww,hh = 0,0,0,0
        
        # EVERYTHING FROM HERE IS frame11p with size (sliceWidth,sliceHeight)

        for (x,y,w,h) in faces: # (x,y,w,h) is a tuple containing type int     
            xx,yy,ww,hh = xx+x,yy+y,ww+w,hh+h
        xx1_f,yy1_f,ww1_f,hh1_f = xx/num,yy/num,ww/num,hh/num
            # float averages, HEAD
            # face without background from unexpanded rectangle in frame11p/gray11p            
        xx1,yy1,ww1,hh1 = int(xx1_f), int(yy1_f), int(ww1_f), int(hh1_f) # unexpanded int box, HEAD        

        print ('\nline', line(), ',    float averages: xx1_f, yy1_f, ww1_f, hh1_f = ', \
               xx1_f,yy1_f,ww1_f,hh1_f)
        print ('\nline', line(), ',      int averages: xx1, yy1, ww1, hh1 = ', \
               xx1,yy1,ww1,hh1)
        print ('line', line(), ',        expand numbers0: LL0, RR0, UU0, DD0 =', LL0,RR0,UU0,DD0)
        print ('line', line(), ',        expand numbers2: LL2, RR2, UU2, DD2 =', LL2,RR2,UU2,DD2)
        print ('line', line(), ',        expand numbers1: LL1, RR1, UU1, DD1 =', LL1,RR1,UU1,DD1)
        print ('line', line(), ',        expand numbers: LL, RR, UU, DD =', LL,RR,UU,DD)

        x1_11_f,y1_11_f,w1_11_f,h1_11_f = xx1_f-LL1*ww1_f/10, yy1_f-UU1*hh1_f/10, \
            (10+LL1+RR1)*ww1_f/10, (10+UU1+DD1)*hh1_f/10 # float box, HEAD
        x1_11, y1_11, w1_11, h1_11 = int(x1_11_f), int(y1_11_f), \
            int(w1_11_f), int(h1_11_f) # expanded int box, HEAD
        print ('\nline', line(), ',    float averages: x1_11_f,y1_11_f,w1_11_f,h1_11_f = ', \
               x1_11_f,y1_11_f,w1_11_f,h1_11_f)
        
        
        # last time these are set
        sliceTop2 = int(max(y1_11_f-2*hh1_f/10,0)) # sliceTop2 must be >= 0
        sliceTop2 = min(sliceTop2,sliceHeight-sliceHeight2)
                    # sliceTop2 must be <= sliceHeight-sliceHeight2 so that
                    # sliceBottom2 is <= sliceHeight
        sliceBottom2 = sliceTop2 + sliceHeight2

        sliceLeft2 = int(max(xx1_f+ww1_f/2-sliceWidth2/2,0))
            # sliceLeft2 is so that bottom of box for FEET is centered but
            # sliceLeft2 >= 0
        sliceLeft2 = min(sliceLeft2, sliceWidth - sliceWidth2)
            # sliceLeft2 <= sliceWidth - sliceWidth2 so that sliceRight2 <= sliceWidth
        sliceRight2 = sliceLeft2 + sliceWidth2
        
        print ('\nline', line(), ', PROCESS OUTPUT frame1p')
        print ('sliceWidth2, sliceLeft2, sliceRight2 = ', \
                sliceWidth2, sliceLeft2, sliceRight2)
        print ('sliceHeight2, sliceTop2, sliceBottom2 = ', \
                sliceHeight2, sliceTop2, sliceBottom2)
        
        frame1p = frame11p[sliceTop2:sliceBottom2,sliceLeft2:sliceRight2]
        gray1p = gray11p[sliceTop2:sliceBottom2,sliceLeft2:sliceRight2]
        print ('\nline', line(), ', frame1p.shape =', frame1p.shape)              
        
        # FIND ANGLE MARKER POSITION IN frame11p with template matching
        template = cv2.imread('/home/pi/md4/images/23-0.png',0) # 13-0.png
        (hm, wm) = template.shape 
        
        # choose search area/ region of interest (roi) 
        # from x2_red, y2_red, w2_red, h2_red of previous loop
        roiLeft = int(sliceWidth2/3)
        roiRight  = int(2*sliceWidth2/3)
        roiTop = int(3*sliceHeight2/4)
        roiBottom = int(sliceHeight2)
        
        roi = gray1p[roiTop:roiBottom, roiLeft:roiRight]
        res = cv2.matchTemplate(roi,template,cv2.TM_SQDIFF)
        
        # For TM_SQDIFF, Good match yields minimum value; bad match yields large values
        # For all others it is exactly opposite, max value = good fit.
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = min_loc  #Change to max_loc for all except for TM_SQDIFF
        bottom_right = (top_left[0] + wm, top_left[1] + hm) # top_left is (x,y) location        
        
        xm, ym = top_left[0]+roiLeft, top_left[1]+roiTop # locations in frame1p

        # EVERYTHING FROM HERE IS frame1p with size (sliceWidth2,sliceHeight2)

        # get coordinates for frame1p tracker0 which is reduced to size (sliceWidth2,sliceHeight2)
        gap = 3*ww1_f/100
        w0_f, h0_f = footWidth*ww1_f/100, footHeight*hh1_f/100
        x0_f, y0_f = (xm+wm/2)-gap-w0_f-1, (ym+hm/2)-footLevel*hh1_f/100-h0_f # float box, FOOT VIEWED ON LEFT

        # get coordinates for frame1p tracker2 which is reduced to size (sliceWidth2,sliceHeight2)
        w2_f, h2_f = footWidth*ww1_f/100, footHeight*hh1_f/100
        x2_f, y2_f = (xm+wm/2)+gap+1, (ym+hm/2)-footLevel*hh1_f/100-h2_f # float box, FOOT VIEWED ON LEFT

        # get coordinates for frame1p tracker1 which is reduced to size (sliceWidth2,sliceHeight2)
        x1_f, y1_f, w1_f, h1_f = x1_11_f-sliceLeft2, y1_11_f-sliceTop2, w1_11_f, h1_11_f
        bb1 = (x1_f, y1_f, w1_f, h1_f) 
            # float box for CSRT initialization, HEAD

        x1, y1, w1, h1 = int(x1_f), int(y1_f), int(w1_f), int(h1_f)
            # int box for rectangle, HEAD
        print ('\nline', line(), ',      int box in frame1p: x1, y1, w1, h1 = ', \
                x1, y1, w1, h1)
        print ('float box (bb1): x1_f, y1_f, w1_f, h1_f = ', \
               x1_f, y1_f, w1_f, h1_f)
        print ('     bb1 = ', ' '.join(format(f, '.1f') for f in bb1))

        # EVERYTHING FROM HERE IS frame1p0 and frame1p2

        # GET NUMBERS FOR FRAMES FOR LEFT & RIGHT FEET (frame1p0 & frame1p2)
        # Best if frame1p0 & frame1p2 extend inward to middle slightly more than tracking boxes 
        
        # frame for LEFT FOOT
        sliceTop20 = int(y0_f-10*hh1_f/10) 
        sliceBottom20 = sliceHeight2
        sliceHeight20 = sliceBottom20-sliceTop20

        sliceLeft20 = 0        
        sliceRight20 = int(xm+wm/2-gap)
        sliceWidth20 = sliceRight20-sliceLeft20
        
        # frame for RIGHT FOOT
        sliceTop22 = int(y2_f-10*hh1_f/10) 
        sliceBottom22 = sliceHeight2
        sliceHeight22 = sliceBottom22-sliceTop22

        sliceLeft22 = int(xm+wm/2+gap)
        sliceRight22 = sliceWidth2
        sliceWidth22 = sliceRight22-sliceLeft22

        print ('\nline', line(), ', LEFT FOOT frame1p0')
        print ('sliceWidth20, sliceLeft20, sliceRight20 = ', \
                sliceWidth20, sliceLeft20, sliceRight20)
        print ('sliceHeight20, sliceTop20, sliceBottom20 = ', \
                sliceHeight20, sliceTop20, sliceBottom20)

        print ('\nline', line(), ', RIGHT FOOT frame1p2')
        print ('sliceWidth22, sliceLeft22, sliceRight22 = ', \
                sliceWidth22, sliceLeft22, sliceRight22)
        print ('sliceHeight22, sliceTop22, sliceBottom22 = ', \
                sliceHeight22, sliceTop22, sliceBottom22)


        # GET FRAMES FOR LEFT & RIGHT FEET (frame1p0 & frame1p2)

        frame1p0 = frame1p[sliceTop20:sliceBottom20,sliceLeft20:sliceRight20]
        print ('\nline', line(), ', frame1p0.shape =', frame1p0.shape)

        frame1p2 = frame1p[sliceTop22:sliceBottom22,sliceLeft22:sliceRight22]
        print ('line', line(), ', frame1p2.shape =', frame1p2.shape)

        # Get coordinates for tracker0 in frame1p0
        x0_f0 = x0_f
        y0_f0 = y0_f-sliceTop20
        w0_f0 = w0_f
        h0_f0 = h0_f
        x0, y0, w0, h0 = int(x0_f), int(y0_f), int(w0_f), int(h0_f)
            # int box for rectangle in frame1p, FOOT VIEWED ON LEFT
        print ('\nline', line(), ',      int box in frame1p: x0, y0, w0, h0 = ', \
                x0, y0, w0, h0)
        print ('float box in frame1p: x0_f, y0_f, w0_f, h0_f = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x0_f, y0_f, w0_f, h0_f))
        print ('float box in frame1p0 for bb0: x0_f0, y0_f0, w0_f0, h0_f0 = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x0_f0, y0_f0, w0_f0, h0_f0))
        bb0 = (x0_f0, y0_f0, w0_f0, h0_f0)
            # float box in frame1p0 for CSRT initialization, FOOT VIEWED ON LEFT
        print ('   bb0 = ', ' '.join(format(f, '.1f') for f in bb0))        

        # Get coordinates for tracker2 in frame1p2
        x2_f2 = x2_f-sliceLeft22
        y2_f2 = y2_f-sliceTop22
        w2_f2 = w2_f
        h2_f2 = h2_f
        x2, y2, w2, h2 = int(x2_f), int(y2_f), int(w2_f), int(h2_f)
            # int box for rectangle in frame1p, FOOT VIEWED ON RIGHT
        print ('\nline', line(), ',      int box in frame1p: x2, y2, w2, h2 = ', \
                x2, y2, w2, h2)
        print ('float box in frame1p: x2_f, y2_f, w2_f, h2_f = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x2_f, y2_f, w2_f, h2_f))
        print ('float box in frame1p2 for bb2: x2_f2, y2_f2, w2_f2, h2_f2 = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x2_f2, y2_f2, w2_f2, h2_f2))
        bb2 = (x2_f2, y2_f2, w2_f2, h2_f2)
            # float box in frame1p2 for CSRT initialization, FOOT VIEWED ON RIGHT
        print ('   bb2 = ', ' '.join(format(f, '.1f') for f in bb2))        
        
        tracker0.init(frame1p0,bb0) # initialize the frame1p0 tracker0 at faceNum frame 
        if useHead == True:
            tracker1.init(frame1p,bb1) # initialize the frame1p tracker1 
        tracker2.init(frame1p2,bb2) # initialize the frame1p2 tracker2
        print ('line', line(), ', TRACKERS 0, (1), & 2 INITIATED') 

        faceFound = True

        # data is appended for frame1p
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
                
        # DRAW FACE & FEET RECTANGLES ON frame1p.

        cv2.rectangle(frame1p, (sliceLeft20, sliceTop20), \
            (sliceLeft20+ sliceWidth20, sliceTop20+ sliceHeight20-1), yellow, 2)
            # int box of frame1p0, FOOT VIEWED ON LEFT
        cv2.rectangle(frame1p, (sliceLeft22, sliceTop22), \
            (sliceLeft22+ sliceWidth22-1, sliceTop22+ sliceHeight22-1), yellow, 2)
            # int box of frame1p2, FOOT VIEWED ON RIGHT

        cv2.rectangle(frame1p, (x0, y0), (x0+w0, y0+h0), green, 2)
            # int box, FOOT VIEWED ON LEFT
        cv2.rectangle(frame1p, (x2, y2), (x2+w2, y2+h2), green, 2)
            # int box, FOOT VIEWED ON RIGHT
        cv2.rectangle(frame1p, (xx1-sliceLeft2, yy1-sliceTop2), \
                      (xx1-sliceLeft2+ww1, yy1-sliceTop2+hh1), green, 2)
            # unexpanded int box, HEAD        
        cv2.rectangle(frame1p, (xm, ym), (xm+wm, ym+hm), green, 2)
            # ANGLE MARKER RECTANGLE IN frame1p
                
        
        if useHead == True:
            cv2.rectangle(frame1p, (x1, y1), (x1+w1, y1+h1), green, 2)
                # expanded int box, HEAD
        
        # WRITE TEXT ON frame1p.
        cv2.putText(frame1p,'Face found',(2,cue_y_position),
            font, fontsize2, green, 1, cv2.LINE_AA)        
        cv2.putText(frame1p,'Time = {:.3f} s'.format(elapsedTime),(2,time_y_position),
            font, fontsize2, green, 1, cv2.LINE_AA)
        cv2.putText(frame1p,'Frame = {}'.format(fc2),(2,fc_y_position),
            font, fontsize2, green, 1, cv2.LINE_AA)
        
        cv2.imshow('frame1p',frame1p)
        print('\nline', line(), ', frame1p.shape = ', frame1p.shape)
        out1p.write(frame1p)
        
        key1 = cv2.waitKey(1) & 0xFF
        if key1 == ord("q"): # press 'q' key to break early
            print ('line', line(), ', pressed "q"')
            break
        print ('Face found, frame1p, fc2 = ', fc2)
        
        continue

    ### END OF 1ST LOOP ### END OF 1ST LOOP ### END OF 1ST LOOP ###    
    
    ### START OF UPDATE LOOPS ### START OF UPDATE LOOPS ### START OF UPDATE LOOPS ###

    # Note that tracker.init() was done
    # near end of FACE FINDING STAGE for frame1p
    # update the frame1p trackers at all frames after that frame
    frame1p = frame11p[sliceTop2:sliceBottom2,sliceLeft2:sliceRight2]
    frame1p0 = frame1p[sliceTop20:sliceBottom20,sliceLeft20:sliceRight20]
    frame1p2 = frame1p[sliceTop22:sliceBottom22,sliceLeft22:sliceRight22]

    (success0,box0) = tracker0.update(frame1p0)
    if not success0:
        print ('\nline', line(), ', frame1p tracker0 FAILURE')
        cv2.putText(frame1p,'Time = {:.3f} s'.format(elapsedTime),(2,time_y_position),
            font, fontsize2, red, 1, cv2.LINE_AA)
        cv2.putText(frame1p,'FAIL frame = {}'.format(fc2),
            (2,cue_y_position), font, fontsize2, red, fontBoldness2, cv2.LINE_AA)
        cv2.imshow('frame1p',frame1p)
        print('\nline', line(), ', frame1p.shape = ', frame1p.shape)
        out1p.write(frame1p)
        
        key2 = cv2.waitKey(1) & 0xFF
        if key2 == ord("q"): # press 'q' key to break early
            print ('line', line(), ', pressed "q"')
            break
        break
    x0_f0, y0_f0, w0_f0, h0_f0 = box0 # CSRT keeps track of this for each update, FEET
    x0_f, y0_f, w0_f, h0_f = x0_f0, y0_f0+sliceTop20, w0_f0, h0_f0
    x0, y0, w0, h0 = int(x0_f), int(y0_f), int(w0_f), int(h0_f)
        # these ints are used for rectangle, FOOT VIEWED ON LEFT        
    
    (success2,box2) = tracker2.update(frame1p2)
    if not success2:
        print ('\nline', line(), ', frame1p tracker2 FAILURE')
        cv2.putText(frame1p,'Time = {:.3f} s'.format(elapsedTime),(2,time_y_position),
            font, fontsize2, red, 1, cv2.LINE_AA)
        cv2.putText(frame1p,'FAIL frame = {}'.format(fc2),
            (2,cue_y_position), font, fontsize2, red, fontBoldness2, cv2.LINE_AA)
        cv2.imshow('frame1p',frame1p)
        print('\nline', line(), ', frame1p.shape = ', frame1p.shape)
        out1p.write(frame1p)
        
        key2B = cv2.waitKey(1) & 0xFF
        if key2B == ord("q"): # press 'q' key to break early
            print ('line', line(), ', pressed "q"')
            break
        break
    x2_f2, y2_f2, w2_f2, h2_f2 = box2 # CSRT keeps track of this for each update, FEET
    x2_f, y2_f, w2_f, h2_f = x2_f2+sliceLeft22, y2_f2+sliceTop22, w2_f2, h2_f2
    x2, y2, w2, h2 = int(x2_f), int(y2_f), int(w2_f), int(h2_f)
        # these ints are used for rectangle, FOOT VIEWED ON RIGHT        
    
    if useHead == True:
        (success1,box1) = tracker1.update(frame1p)
        if not success1:
            print ('\nline', line(), ', frame1p tracker1 FAILURE')
            cv2.putText(frame1p,'Time = {:.3f} s'.format(elapsedTime),(2,time_y_position),
                font, fontsize2, red, 1, cv2.LINE_AA)
            cv2.putText(frame1p,'FAIL frame = {}'.format(fc2),
                (2,cue_y_position), font, fontsize2, red, fontBoldness2, cv2.LINE_AA)
            cv2.imshow('frame1p',frame1p)
            print('\nline', line(), ', frame1p.shape = ', frame1p.shape)
            out1p.write(frame1p)
            
            key2C = cv2.waitKey(1) & 0xFF
            if key2C == ord("q"): # press 'q' key to break early
                print ('line', line(), ', pressed "q"')
                break
            break
        x1_f, y1_f, w1_f, h1_f = box1 # CSRT keeps track of this for each update, HEAD
        (x1, y1, w1, h1) = [int(a) for a in box1]
            # these ints are used for rectangle, HEAD      

    cv2.rectangle(frame1p, (sliceLeft20, sliceTop20), \
        (sliceLeft20+ sliceWidth20, sliceTop20+ sliceHeight20-1), yellow, 2)
        # int box of frame1p0, FOOT VIEWED ON LEFT
    cv2.rectangle(frame1p, (sliceLeft22, sliceTop22), \
        (sliceLeft22+ sliceWidth22-1, sliceTop22+ sliceHeight22-1), yellow, 2)
        # int box of frame1p2, FOOT VIEWED ON RIGHT

    cv2.rectangle(frame1p,(x0,y0),(x0+w0,y0+h0),red,2)
        # int hit box, FOOT VIEWED ON LEFT        
    
    cv2.rectangle(frame1p,(x2,y2),(x2+w2,y2+h2),red,2)
        # int hit box, FOOT VIEWED ON RIGHT
        
    if useHead == True:
        cv2.rectangle(frame1p,(x1,y1),(x1+w1,y1+h1),red,2)
            # int hit box, HEAD    
    
    if fc2 == faceNum+1:    
        print ('\nline', line(), 'In next loop, fc2 = ', fc2)
        print ('      int box in frame1p: x0, y0, w0, h0 = ', \
                x0, y0, w0, h0)
        print ('float box in frame1p: x0_f, y0_f, w0_f, h0_f = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x0_f, y0_f, w0_f, h0_f))
        print ('float box in frame1p0 for box0: x0_f0, y0_f0, w0_f0, h0_f0 = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x0_f0, y0_f0, w0_f0, h0_f0))
            # float box in frame1p0 for CSRT update, FOOT VIEWED ON LEFT
        print ('      box0 = ', ' '.join(format(f, '.1f') for f in box0))        

        print ('\nline', line(), ',      int box in frame1p: x2, y2, w2, h2 = ', \
                x2, y2, w2, h2)
        print ('float box in frame1p: x2_f, y2_f, w2_f, h2_f = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x2_f, y2_f, w2_f, h2_f))
        print ('float box in frame1p2 for box2: x2_f2, y2_f2, w2_f2, h2_f2 = {:.1f}, {:.1f}, {:.1f}, {:.1f}'. \
               format(x2_f2, y2_f2, w2_f2, h2_f2))
            # float box in frame1p2 for CSRT initialization, FOOT VIEWED ON RIGHT
        print ('     box2 = ', ' '.join(format(f, '.1f') for f in box2))        

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

    if x0Var > footThreshold or y0Var > footThreshold or x2Var > footThreshold or y2Var > footThreshold:
        passThreshold = True
    if useHead == True:
        if x1Var > headThreshold or y1Var > headThreshold:
            passThreshold = True        
        
    if ended == False:
        elapsedTime = t_[fc2] - startTime2
        if elapsedTime >= 10 or passThreshold:
            ended = True
            if elapsedTime >= 10 and passThreshold == False:
                elapsedTime = t_[fc2] - startTime2            
            if passThreshold == True:
                elapsedTime = t_[fc2-1] - startTime2
            
    # put text on screen
    if faceFound == False:
        cv2.putText(frame1p,'Face camera',(2,cue_y_position),
            font, fontsize2, yellow, 1, cv2.LINE_AA)
    if faceFound == True and ended == False:        
        cv2.putText(frame1p,'Stand still',(2,cue_y_position),
            font, fontsize2, yellow, 1, cv2.LINE_AA)
    if ended == True:
        cv2.putText(frame1p,'Test is done',(2,cue_y_position),
            font, fontsize2, red, 1, cv2.LINE_AA)
        if extraStartTime == None:
            extraStartTime = t_[fc2]

    cv2.putText(frame1p,'Time = {:.3f} s'.format(elapsedTime),(2,time_y_position),
        font, fontsize2, yellow, 1, cv2.LINE_AA)
    cv2.putText(frame1p,'Frame = {}'.format(fc2),(2,fc_y_position),
        font, fontsize2, yellow, 1, cv2.LINE_AA)

    cv2.imshow('frame1p',frame1p)
    out1p.write(frame1p)

    if extraStartTime:
        extraTime = t_[fc2] - extraStartTime

    key3 = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key3 == ord("q"): # press 'q' key to break loo early
        print ('pressed "q"')
        break
    """
    if ended == True:
        if extraTime > 1.3:
            print ('ended = True, extraTime, elapsedTime, fc2 = {:.1f} s, {:.3f} s, {}' \
                   .format(extraTime,elapsedTime,fc2))
            break
    """
    if t_[fc2] - t_[0] > 11.0:
        break
cap1.release()
out1p.release()
cv2.destroyAllWindows()

# (x-x1_0) is x pixel difference between initial point & present point
# 1000*mpp*(x-x1_0) is x difference between initial point & present point in mm
# see lines 60-69 for more about mpp (meters per pixel) 
t_ = [x-startTime2 for x in t_]
t_ = t_[faceNum:faceNum+len(x0_f_)]
    # because the t_ array has elements at end that are not used
print ('line', line(), ', len(t_) = ', len(t_))
print ('line', line(), ', len(x0_f_) = ', len(x0_f_))
x0_mm_ = [1000*mpp*(x-x0_0) for x in x0_f_]
print ('line', line(), ', len(x0_mm_) = ', len(x0_mm_))
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
# from matplotlib.pyplot import figure, show, grid, tight_layout
vw = 7 # vertical line width
f4 = plt.figure(figsize=(12, 12)) # inches wide, inches high
mpl.rcParams['font.size'] = 40 # 24
mpl.rcParams['axes.linewidth'] = 3
mpl.rcParams['grid.linewidth'] = 3
plt.subplot(1,1,1)
print ('line', line(), ', len(t_) = ', len(t_))
print ('line', line(), ', len(x0_mm_) = ', len(x0_mm_))
plt.plot(t_, x0_mm_, linestyle='solid', linewidth=10, color='blue', \
         label='Left foot x') # fat solid line, no markers
plt.plot(t_, x2_mm_, linestyle=(0,(3,2)), linewidth=10, color='orange', \
         label='Right foot x') # fat dashed line, no markers
if useHead == True:    
    plt.plot(t_, x1_mm_, linestyle='dotted', linewidth=10, color='black', \
             label='Head x') # fat dotted line, no markers
    
plt.plot(t_, y0_mm_, linestyle='solid', linewidth=6, color='green', \
         label='Left foot y') # thin solid line, no markers
plt.plot(t_, y2_mm_, linestyle=(0,(4,4)), linewidth=6, color='red', \
         label='Right foot y') # thin dashed line, no markers
if useHead == True:    
    plt.plot(t_, y1_mm_, linestyle='dotted', linewidth=6, color='purple', \
             label='Head y') # thin dotted line, no markers
    
    # plt.scatter([8.5,8.5], [-48,48], s=100, c='red')
    
    plt.text(12.4, -headThreshold+0.9, 'headThreshold') # -0.3
    plt.text(12.4, headThreshold-4.1, 'headThreshold')   
    plt.axhline(y=-headThreshold, linestyle='dashed', linewidth=vw)
    plt.axhline(y=headThreshold, linestyle='dashed', linewidth=vw)

plt.text(12.4, -footThreshold+0.9, 'footThreshold')
plt.text(12.4, footThreshold-4.1, 'footThreshold')
# plt.text(-0.3, 40.9, 'Time = {:.2f} s'.format(elapsedTime))
plt.text(12.4, 10.9, 'Time')
plt.text(12.4, 0.9, '{:.3f} s'.format(elapsedTime))
plt.axvline(x=elapsedTime, linestyle='dashed', linewidth=vw)
plt.axhline(y=-footThreshold, linestyle='dashed', linewidth=vw)
plt.axhline(y=footThreshold, linestyle='dashed', linewidth=vw)
plt.title("Standing Balance Test\nx and y Position Variations (mm), " \
          + "\nStart Point Normalized to 0)",pad=12) # 30
plt.xlabel('Time (s)',labelpad=1) # 10
plt.ylabel('Standing Balance Test\nLeft foot, Right Foot, and Head, ' \
        + '\nx and y Positions (mm), \nStart Point Normalized to 0)',labelpad=1) # 10
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
plt.tick_params('x', pad=10.0) # pad is space between tick labels & grid
plt.tick_params('y', pad=10.0) # pad is space between tick labels & grid
# mpl.rcParams['legend.loc'] = 'upper right'
plt.grid()
plt.legend(prop={'size':42},ncol=1,labelspacing=0.5,columnspacing=0.5,frameon=False, \
           bbox_to_anchor=(2.15,0.92))
    # sets legend font size, number of columns, row spacing, space between columns, 
    # legend box show or not (contents still there)

plt.savefig(balanceFig, bbox_inches='tight')
    # bbox_inches='tight' keeps label at edge from being trimmed out
# plt.show()
plt.close()

processTime = time() - processStart
totalTime = time() - setupStart
processFrames = fc2 + faceNum + 1 # frames in process video
print ('\nsetupTime, recordTime, processTime = {:.3f} s, {:.3f} s, {:.3f} s' \
       .format(setupTime, recordTime, processTime))
print ('recordFrames, processFrames = ', recordFrames, processFrames)
totalTimeCheck = setupTime + recordTime + processTime
print ('totalTime, totalTimeCheck = {:.3f} s, {:.3f} s'.format(totalTime, totalTimeCheck))


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
f.write('{:.3f} s\n'.format(elapsedTime))
f.close()

# WRITE TO CSV FILE
f2 = open("/home/pi/md4/TXT_CSV/balanceTest.csv", "a")
f2.write(stamp + ',{:.3f},'.format(elapsedTime) + doctor + ',' + patientID + ',,')
f2.write('{:.3f},'.format(setupTime))
f2.write('{:.3f},'.format(recordTime))
f2.write('{:.3f},'.format(processTime))
f2.write('{:.3f}\n'.format(totalTime))
f2.close()

picklePath = '/home/pi/pickle/balance' + stamp + '.pkl'
# os.mkdir(picklePath)
dataList="dataList,t_,x0_mm_,y0_mm_,x1_mm_,y1_mm_,x2_mm_,y2_mm_,elapsedTime," \
          + "headThreshold,footThreshold,useHead"
dataSet=[dataList,t_,x0_mm_,y0_mm_,x1_mm_,y1_mm_,x2_mm_,y2_mm_,elapsedTime, \
         headThreshold,footThreshold,useHead]
with open(picklePath,'wb') as f:
    pickle.dump(dataSet,f)

"""
# to read the data back into variables with pickle
with open((picklePath, 'rb') as f2:
    # picklePath is a string path ending in a .pkl file (.pickle)
    dataLoad = pickle.load(f2) # must remember order to retreive it properly
dataList,t_,x0_mm_ = dataLoad[0],dataLoad[1],dataLoad[2]
y0_mm_,x1_mm_,y1_mm_ = dataLoad[3],dataLoad[4],dataLoad[5]
x2_mm_,y2_mm_,elapsedTime = dataLoad[6],dataLoad[7],dataLoad[8]
headThreshold,footThreshold,useHead = dataLoad[9],dataLoad[10],dataLoad[11]
# now plots can be made
# if variables get mixed up, print (dataList) # dataLoad[0]
"""
print ('\nrecord_fps = {:.3f} frames/second for new fps'.format(record_fps))
print ('Set fps = {:.3f} frames/second'.format(fps))

print ('\nALL DONE\n')     
    
