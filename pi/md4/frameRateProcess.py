# frameRateProcess.py
# It changes the frame rate of a video to a new frame rate

# imports
from time import sleep, time
import cv2
import argparse
print (__file__)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('fileName', type=str, nargs="?", default="", \
    help="1st: name of video file for processing")
ap.add_argument('record_fps', type=float, nargs="?", default="", \
    help="2nd: record_fps is true fps for new video file")
args = ap.parse_args()
fileName = args.fileName
record_fps = args.record_fps
print ('\nfileName, record_fps =', fileName, record_fps)
file_path = '/home/pi/process/oldFrameRate/' + fileName

fc2 = -1 # It counts each frame of PROCESSING STAGE output video
cap0 = cv2.VideoCapture(file_path)
height = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
print ('width, height = ', width, height)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
frameRateVideo = '/home/pi/process/frameRateProcessed/f '+fileName
out = cv2.VideoWriter(frameRateVideo,fourcc,record_fps, (width,height))

capSleep = 1.0
sleep(capSleep)
while 1:
    ret0, frame0 = cap0.read()
    if frame0 is None:
        print ('End of video, frame0 is None')
        break
    fc2 += 1
    out.write(frame0)    
    keyC = cv2.waitKey(1) & 0xFF
    if keyC == ord("q"): # press 'q' key to break early
        print ('line', line(), ', pressed "q"')
        break
    
cap0.release()
out.release()
cv2.destroyAllWindows()
  
print ('Frame rate has been changed to {:.3f} frames/second,'.format(record_fps))
print ('   a true frame rate based on record_fps = recordFrames/recordTime')
print ('\nALL DONE\n')
