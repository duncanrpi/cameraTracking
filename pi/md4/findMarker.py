# imports
from imutils.video import VideoStream
import imutils
import numpy as np
from time import sleep, time
from datetime import datetime
import cv2
from math import isnan

video = False
fps = 2
fwidth = 1280 # frame width
fheight = 960 # frame height
half_fwidth = fwidth//2
half_fheight = fheight//2
stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
findMarker = '/home/pi/md4/'+ stamp + ' findMarker.avi'
vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
if video == True:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out1 = cv2.VideoWriter(findMarker,fourcc, fps, (fwidth,fheight))

sleep(3.0)
xmarker, loc = None, None
template = cv2.imread('/home/pi/md4/images/13-0.png',0) # numpy.ndarray (13, 13)
w5, h5 = template.shape[::-1]
print ('template.shape =', template.shape, '   w5 = ', w5, '   h5 = ', h5)
deg_inc = 10.0
h_field_of_view = 63.6 # PiCamera degrees wide, original 62.2
    # Zealinno webcam left/right 60.7
pix_inc = deg_inc * fwidth / h_field_of_view
font=cv2.FONT_HERSHEY_SIMPLEX
frame_count = 0
threshold = 0.8

while True:
    frame1=vs1.read()
    frame_count += 1

    start_time = time()
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    if frame_count == 1:
        print ('frame1.shape, gray.shape =', frame1.shape, gray.shape)
    res = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED) # numpy.ndarray (351, 478)
    loc = np.where( res >= threshold) # tuple, len=2

    try: loc # draw marker box
    except NameError: loc = None
    if loc is None:
        print ('loc is None')
    else:
        # if isnan(loc)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame1, (pt[0], pt[1]), (pt[0]+w5-1, pt[1]+h5-1), (0,0,255), 1)
        # print ('type(loc), len(loc), loc =', type(loc), len(loc), loc[1].shape)

        if loc[1].all() and loc[1].size != 0:
            xmarker = loc[1].mean() + w5//2 # loc[0] y, loc[1] x, both numpy.ndarray (5,)
                # 5 overlapping rectangles, take average of x

            if isnan(xmarker):
                print ('xmarker not found')
            else:
                if frame_count % 10 == 0:
                    # print ('xmarker =', xmarker)
                    print('', end = '')
                num_L = int(xmarker / pix_inc + 1) # mark the degrees at the top of the frames & put numbers
                num_R = int(((fwidth-1) - xmarker) / pix_inc + 1)
                for ii in range(num_L):
                    cv2.line(frame1, (int(round(xmarker-ii*pix_inc)), 0), (int(round(xmarker-ii*pix_inc)), 10), (0, 0, 255), 2)
                    cv2.putText(frame1, str(10*ii), (int(round(xmarker-ii*pix_inc)), 26), font, 0.5, (0, 0, 255), 2)
                    if frame_count % 10 == 0:
                        # print ('xmarker =', xmarker, '   int(round(xmarker-ii*pix_inc)) =', int(round(xmarker-ii*pix_inc)))
                        # print ('ii =', ii, '   pix_inc =', pix_inc)
                        print('', end = '')
                for jj in range(1,num_R):
                    cv2.line(frame1, (int(round(xmarker+jj*pix_inc)), 0), (int(round(xmarker+jj*pix_inc)), 10), (0, 0, 255), 2)
                    cv2.putText(frame1, str(-10*jj), (int(round(xmarker+jj*pix_inc)), 26), font, 0.5, (0, 0, 255), 2)
                    if frame_count % 10 == 0:
                        # print ('str(-10*jj) =', str(-10*jj), '   int(round(xmarker+jj*pix_inc)) =',int(round(xmarker+jj*pix_inc)))
                        # print ('jj =', jj, '   pix_inc =', pix_inc)
                        print('', end = '')

    elapsed_time = time() - start_time
    
    cv2.line(frame1, (half_fwidth, 0), (half_fwidth, fheight-1), (0, 0, 255), 1)
    cv2.line(frame1, (0, half_fheight), (fwidth-1, half_fheight), (255, 0, 255), 1)
    if video == True:
        out1.write(frame1)    
    cv2.imshow('frame1', frame1)

    if frame_count < 6:
        # print ('elapsed time = {:.3f}'.format(elapsed_time))
        print('', end = '')
    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key == ord("q"): # press 'q' key to break loop
        break
cv2.destroyAllWindows() # begin ending code
vs1.stop() # stop() is for VideoStream object
if video == True:
    out1.release()
