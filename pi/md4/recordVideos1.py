# imports
from imutils.video import VideoStream
import imutils
import numpy as np
from time import sleep, time
from datetime import datetime
import cv2

video = False
# Possible resolutions (Resol), frames per second (FPS), and
#     Horizontal Field of View in degrees (FoV) for PiCamera V2.1
# Resolution   FPS     FoV
#  640 x  480  15      63.6
#  976 x  736   7      63.6
# 1296 x  976   4.7    63.5
# 1680 x  480   7.4
# 1920 x  544   5.4
# 1952 x 1472   1.63   
# 2592 x 1952  FAILED  

fwidth = 1280
fheight = 960

# fwidth = 1680
# fheight = 960
# fheight = 1264
# fheight = 368
# fwidth = 1920
# fheight = 544
frame_count = 0
videoDuration = 0.0 # the elapsed time until starting
fps = 23 # show only 100; show & record 23
stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
recordVideos1 = '/home/pi/md4/'+ stamp + ' recordVideos1.avi'

vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
# src=1 is reserved for PiCamera, it seems
if video == True:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out1 = cv2.VideoWriter(recordVideos1,fourcc, fps, (fwidth,fheight))

sleep(6.0)
while True:
    frame1=vs1.read()
    frame_count += 1
    if frame_count == 1:
        videoStart = time()
        print('frame1.shape =', frame1.shape)
    if video == True:
        out1.write(frame1)    
    cv2.imshow('frame1', frame1)
    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if key == ord("q"): # press 'q' key to break loop
        break
videoDuration = time() - videoStart
totalFrames = frame_count
calculated_fps = totalFrames/videoDuration
print ('videoDuration = {:.3f} s'.format(videoDuration))
print ('totalFrames = ', totalFrames)
print ('calculated_fps = {:.3f} frames/second'.format(calculated_fps))
print ('Set fps = {:.3f} frames/second'.format(fps))
print ('New fps after correction = {:.3f} frames/second'.format(calculated_fps))

cv2.destroyAllWindows() # begin ending code
vs1.stop() # stop() is for VideoStream object
if video == True:
    out1.release()

