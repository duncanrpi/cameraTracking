# startEndProcess.py (adapted from frameRateProcess.py)
# It outputs a new gait speed video with start and end vertical lines.

# imports
from time import sleep, time
import cv2
import argparse
print (__file__)

pixAdj = 21 # 20.6449
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('fileName', type=str, nargs="?", default="", \
    help="1st: name of video file for processing")
ap.add_argument('startPixels', type=int, nargs="?", default="", \
    help="2nd: startPixels is the start pixel position in frame for gait speed walk")
ap.add_argument('endPixels', type=int, nargs="?", default="", \
    help="3rd: endPixels is the end pixel position in frame for gait speed walk")
args = ap.parse_args()
fileName = args.fileName
startPixels = args.startPixels - pixAdj
endPixels = args.endPixels - pixAdj
print ('\nfileName, startPixels, endPixels =', fileName, startPixels, endPixels)
file_path = '/home/pi/process/videosNoLines/' + fileName

fc2 = -1 # It counts each frame of PROCESSING STAGE output video
cap0 = cv2.VideoCapture(file_path)
height = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
print ('width, height = ', width, height)
blue, green, yellow, orange, white = (255,0,0),(0,255,0),(0,255,255),(0,125,255),(255,255,255)

record_fps = 50

fourcc = cv2.VideoWriter_fourcc(*'XVID')
outVideo = '/home/pi/process/videosLines/f '+fileName
out = cv2.VideoWriter(outVideo,fourcc,record_fps, (width,height))

capSleep = 1.0
sleep(capSleep)
while 1:
    ret0, frame0 = cap0.read()
    if frame0 is None:
        print ('End of video, frame0 is None')
        break
    fc2 += 1 # There is a frame 0 that often shows green boxes for face found,
             # but no data yet in lower area    
    cv2.line(frame0, (startPixels, 0), (startPixels, 95), white, 2) # green
    cv2.line(frame0, (endPixels, 0), (endPixels, 95), white, 2) # orange
    # cv2.line(frame0, (startPixels, 0), (startPixels, height-1), green, 1) # green
    # cv2.line(frame0, (endPixels, 0), (endPixels, height-1), orange, 1) # orange        
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
