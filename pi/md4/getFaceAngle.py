# getFaceAngle.py

# imports
from imutils.video import VideoStream
import numpy as np
from time import sleep, time
import cv2
from math import isnan


offset, rr = 0, 4
timeLimit = 200 # time to end loop
fwidth = 1280 # frame width
fheight = 960 # frame height
xmarker, ymarker, loc = None, None, None
template = cv2.imread('/home/pi/md4/images/31-0.png',0) # numpy.ndarray (13, 13)
w5, h5 = template.shape[::-1]
print ('template.shape =', template.shape, '   w5 = ', w5, '   h5 = ', h5)
deg_inc = 10.0
h_field_of_view = 63.6 # PiCamera degrees wide, original 62.2
    # Zealinno webcam left/right 60.7
pix_inc = deg_inc * fwidth / h_field_of_view
R = h_field_of_view / fwidth # degrees/pixel
font=cv2.FONT_HERSHEY_SIMPLEX
yellow, blue = (0,255,255), (0,0,255)
fontsize = 2
fontBoldness = 2
Xangle, Yangle = 0, 0

cue02 = int(950.0*fheight/960.0)
frame_count = 0
threshold = 0.8

face_cascade = cv2.CascadeClassifier('/home/pi/md4/haarcascades/haarcascade_frontalface_default.xml')
vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
sleep(3.0)
startTime = time()
found = False

while True:
    frame1=vs1.read()
    frame_count += 1

    start_time = time()

    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) # numpy.ndarray (480, 640)
    if frame_count == 7:
        print ('gray.shape =', gray.shape)
        # print ('roi.shape =', roi.shape)
    res = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED) # numpy.ndarray (351, 478)
    loc = np.where( res >= threshold) # tuple, len=2

    try: loc # draw marker box
    except NameError: loc = None
    if loc is None:
        print ('loc is None')
    else:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame1, (pt[0], pt[1]), (pt[0]+w5-1, pt[1]+h5-1), (0,0,255), 1)
        print ('type(loc), len(loc), loc =', type(loc), len(loc), loc[1].shape)

        if loc[1].all() and loc[1].size != 0:
            xmarker = loc[1].mean() + w5//2 # loc[0] y, loc[1] x, both numpy.ndarray (5,)
                # 5 overlapping rectangles, take average of x
            ymarker = loc[0].mean() + h5//2

            if isnan(xmarker):
                print ('xmarker not found')
            else:                
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)                    
                if len(faces) == 0:
                    cv2.putText(frame1,'No face, frame_count = {}'.format(frame_count),
                            (0,cue02), font, fontsize, yellow, fontBoldness, cv2.LINE_AA)
                    cv2.imshow('frame1',frame1)

                    key0 = cv2.waitKey(1) & 0xFF
                    if key0 == ord("q"): # press 'q' key to break early
                        print ('pressed "q"')
                        break
                    print ('No face, frame_count = ', frame_count)
                    found = False
                    continue # go to next while loop
                else:
                    x,y,w,h = int(faces[0][0]), int(faces[0][1]), int(faces[0][2]), int(faces[0][3])
                    print ('x,y,w,h = ', x,y,w,h)
                    xsubject = x + w//2
                    ysubject = y + h//2
                    # DRAW FACE RECTANGLES & TEXTS
                    cv2.rectangle(frame1,(x,y),(x+w,y+h),blue,2)
                    cv2.putText(frame1,'Face found, frame_count = {}'.format(frame_count),
                            (0,cue02-100), font, fontsize, blue, fontBoldness, cv2.LINE_AA)
                    cv2.putText(frame1,'xsubject = {}, ysubject = {}'.format(xsubject, ysubject),
                            (0,cue02), font, fontsize, blue, fontBoldness, cv2.LINE_AA)
                    found = True
                
                    Xangle = (xmarker-xsubject)*R
                    Yangle = (ymarker-ysubject)*R
                    print ('\nframe_count = ', frame_count)
                    print ('xmarker = {:.1f}, xsubject = {}, Xangle = {:.1f}'.format(xmarker,xsubject,Xangle))
                    print ('ymarker = {:.1f}, ysubject = {}, Yangle = {:.1f}'.format(ymarker,ysubject,Yangle))                 
                
                # x-axis labels
                num_L = int(xmarker / pix_inc + 1) # mark the degrees at the top of the frames & put numbers
                num_R = int(((fwidth-1) - xmarker) / pix_inc + 1)
                for ii in range(num_L):
                    cv2.line(frame1, (int(round(xmarker-ii*pix_inc)), 0), (int(round(xmarker-ii*pix_inc)), 10), (0, 0, 255), 2)
                    cv2.putText(frame1, str(10*ii), (int(round(xmarker-ii*pix_inc)), 26), font, 0.5, (0, 0, 255), 2)
                    
                for jj in range(1,num_R):
                    cv2.line(frame1, (int(round(xmarker+jj*pix_inc)), 0), (int(round(xmarker+jj*pix_inc)), 10), (0, 0, 255), 2)
                    cv2.putText(frame1, str(-10*jj), (int(round(xmarker+jj*pix_inc)), 26), font, 0.5, (0, 0, 255), 2)
               
                # y-axis labels
                ymarker2 = ymarker - offset
                num_L2 = int(ymarker2 / pix_inc + 1) # mark the degrees at the left of the frames & put numbers
                num_R2 = int(((fheight-1) - ymarker2) / pix_inc + 1)
                for kk in range(num_L2):
                    cv2.line(frame1, (0, int(round(ymarker2-kk*pix_inc))), (10, int(round(ymarker2-kk*pix_inc))), (0, 0, 255), 2)
                    cv2.putText(frame1, str(10*kk), (15, int(round(ymarker2-kk*pix_inc))+rr), font, 0.5, (0, 0, 255), 2)
                    
                for mm in range(1,num_R2):
                    cv2.line(frame1, (0, int(round(ymarker2+mm*pix_inc))), (10, int(round(ymarker2+mm*pix_inc))), (0, 0, 255), 2)
                    cv2.putText(frame1, str(-10*mm), (15, int(round(ymarker2+mm*pix_inc))+rr), font, 0.5, (0, 0, 255), 2)                
        
    elapsed_time = time() - start_time
    cv2.line(frame1, (249, 11), (249, 173), (0, 255, 255), 1) # VERT main
    cv2.line(frame1, (250, 11), (250, 173), (0, 255, 255), 1) # VERT main

    cv2.line(frame1, (249, 201), (249, 373), (0, 255, 255), 1) # VERT main
    cv2.line(frame1, (250, 201), (250, 373), (0, 255, 255), 1) # VERT main
    cv2.line(frame1, (0, 187), (235, 187), (0, 255, 255), 1) # HORIZ main
    
    cv2.imshow('frame1', frame1)
    
    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key == ord("q") or found == True or time()-startTime > timeLimit: # press 'q' key to break loop
        break
    if found == True:
        print ('found = True')
        break

print ('time = {:.1f}'.format(time() - startTime))
cv2.destroyAllWindows() # begin ending code
vs1.stop() # stop() is for VideoStream object
print ('xmarker = {:.1f}, xsubject = {}, Xangle = {:.1f}'.format(xmarker,xsubject,Xangle))
print ('ymarker = {:.1f}, ysubject = {}, Yangle = {:.1f}'.format(ymarker,ysubject,Yangle))

# WRITE TO TXT FILE
f = open("/home/pi/md4/TXT_CSV/angle.txt", "a")
f.write('\n{:.1f}\n'.format(Xangle))
f.write('{:.1f}\n'.format(Yangle))
f.close()




