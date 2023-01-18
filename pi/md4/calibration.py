# calibration.py
# This calibrates for an adjustable (fwidth, fheight) shape image for each of 3 cameras
# imports
from imutils.video import VideoStream
from datetime import datetime
import numpy as np
import imutils
from time import sleep
import cv2

video = False
fps = 5
x_adjust = 0
fwidth = 640 # 608
fheight = 480 # 464
half_fwidth = fwidth//2
half_fheight = fheight//2
stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
calibration012 = "/home/pi/md4/" + stamp + " calibration012.avi"

vs0 = VideoStream(usePiCamera=False,src=0).start() # left Zealinno webcam
vs1 = VideoStream(usePiCamera=True,src=1,resolution=(fwidth,fheight)).start()
vs2 = VideoStream(usePiCamera=False,src=2).start() # right Zealinno webcam
if video == True:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out012 = cv2.VideoWriter(calibration012,fourcc, fps, (3*fwidth,fheight))
frame_count = 0
sleep(10.0)

# loop over the frames of the video
while True:
    # grab the current frame
    frame0 = vs0.read()
    frame1 = vs1.read()
    frame2 = vs2.read()
    if frame0 is None or frame2 is None:
        break
    frame_count += 1    
    if frame_count == 1:
        print('frame shapes = ', frame0.shape, frame1.shape, frame2.shape)

    # Horizontal pixel x range = 0:fwidth-1
    # Vertical pixel y range = 0:fheight-1
    cv2.line(frame0, (half_fwidth, 0), (half_fwidth, fheight-1), (0, 0, 255), 1)
    cv2.line(frame0, (0, half_fheight), (fwidth-1, half_fheight), (255, 0, 255), 1)
        
    cv2.line(frame1, (half_fwidth, 0), (half_fwidth, fheight-1), (0, 0, 255), 1)
    cv2.line(frame1, (0, half_fheight), (fwidth-1, half_fheight), (255, 0, 255), 1)

    cv2.line(frame2, (half_fwidth+x_adjust, 0), (half_fwidth+x_adjust, fheight-1), (0, 0, 255), 1)
    cv2.line(frame2, (0, half_fheight), (fwidth-1, half_fheight), (255, 0, 255), 1)
    
    frame012 = np.hstack((frame0,frame1,frame2))
    cv2.imshow('frame012', frame012)    
    if video == True:
        out012.write(frame012)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the loop
    if key == ord("q"): # otherwise go to next loop iteration
        break

if video == True:
    out012.release()
# cleanup the camera and close any open windows
vs0.stop()
vs1.stop()
vs2.stop()
cv2.destroyAllWindows()
