# gaitSpeed_2D (36)record.py
# Get the subject to stand at the central location of walking pattern and
#    hold the big marker over the center of the face.
#    Set vertical & horizontal angles at 0 degrees relative to the marker.
# This version: CROSSWISE = 4 m. RADIAL = 4.2164 m.

# imports
# timeLimits, radial: 37, 25, 17, crosswise: 20, 13, 11
from time import sleep, time
setupStart = time()
from imutils.video import VideoStream
from datetime import datetime
import cv2
import argparse
import pickle

print ('\n'+__file__)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('correctDist', type=float, nargs="?", default=0.0, \
    help="1st: correct distance in meters")
ap.add_argument('timeLimit', type=float, nargs="?", default=30, \
    help="3rd: recording time limit (s)")
ap.add_argument('fast', type=int, nargs="?", default=1, \
    help="4th: 0=output of 4 figures, 1=output of 2 figures (faster)")
ap.add_argument('pattern', type=int, nargs="?", default=0, \
    help="5th: 0=4m radial line, 1=1.8m crosswise line, 2=4.606m circle, 3=no pattern")
ap.add_argument('height', type=int, nargs="?", default=320, \
    help="6th: pixel height of frame")
ap.add_argument('width', type=int, nargs="?", default=640, \
    help="7th: pixel width of frame")
ap.add_argument('doctor', type=str, nargs="?", default="", \
    help="8th: doctor's name")
ap.add_argument('patientID', type=str, nargs="?", default="", \
    help="9th: patient ID")
args = ap.parse_args()
correctDist = args.correctDist # (m) measured distance to be walked <class 'float'>
timeLimit = args.timeLimit # timeLimit, totalTime = 3,82
fast = args.fast # see above. Also used in guiWalk.py to calculate time for processing.
pattern = args.pattern
height = args.height
width = args.width
doctor = args.doctor
patientID = args.patientID
print ('\ncorrectDist, timeLimit, fast, pattern =', correctDist, timeLimit, fast, pattern)
print ('height, width, doctor, patientID =', height, width, doctor, patientID)

pixels = width * height
fps = round(3730000 / pixels,1) # pattern = 2
if pattern == 0:
    fps = round(2890000 / pixels,1)
elif pattern == 1:
    fps = round(3050000 / pixels,1)
elif pattern == 3:
    fps = round(3730000 / pixels,1)
t_raw_ = [] # time array for all recording time including face finding time 
                     # and before trimming start & end (1st)

# LEFT & RIGHT CAMERAS
fwidth02 = 640
half_fwidth02 = fwidth02//2 # 320
fheight02 = 480
sliceHeight02 = height # 200 for 4 to 6m, 320 for all-round height
sliceTop02 = (fheight02 - sliceHeight02) // 2
if pattern == 1 or pattern == 2:
    sliceTop02 = sliceTop02 - 0
elif pattern == 0:
    sliceTop02 = sliceTop02 - 25    
sliceBottom02 = sliceHeight02 + sliceTop02
sliceWidth02 = width # 640 or 480
sliceLeft02 = (fwidth02 - sliceWidth02) // 2
sliceRight02 = sliceWidth02 + sliceLeft02

stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
recordVideos0of2 = '/home/pi/process/gaitSpeedRecorded/' + stamp + ' recordVideos0of2.avi'
recordVideos2of2 = '/home/pi/process/gaitSpeedRecorded/' + stamp + ' recordVideos2of2.avi'
fc1 = 0

vs0 = VideoStream(usePiCamera=False,src=0).start() # left Zealinno webcam
vs2 = VideoStream(usePiCamera=False,src=2).start() # right Zealinno webcam
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out0 = cv2.VideoWriter(recordVideos0of2,fourcc, fps, (sliceWidth02,sliceHeight02))
out2 = cv2.VideoWriter(recordVideos2of2,fourcc, fps, (sliceWidth02,sliceHeight02))

sleep(2.0) # Self testing: sleep(7.0). Testing others: sleep(2.0)
setupTime = time() - setupStart
recordStart = time()
while True:
    if fc1 % 2 == 0: # odd frame_count
                             # because += 1 right after read()
        frame00=vs0.read()
        frame22=vs2.read()
    else: # even frame_count
        frame22=vs2.read()
        frame00=vs0.read()        
    fc1 += 1
    if fc1 == 1:
        timeStart = time()
        # print('frame00.shape, frame22.shape =', frame00.shape, frame22.shape)
    t_raw_.append(time() - timeStart)
    # print ('fc1, t_raw = {}, {:.3f}'.format(fc1, time() - timeStart))
    
    frame0 = frame00[sliceTop02:sliceBottom02,sliceLeft02:sliceRight02]
    frame2 = frame22[sliceTop02:sliceBottom02,sliceLeft02:sliceRight02]
    out0.write(frame0)
    out2.write(frame2)
    cv2.imshow('frame0', frame0)
    cv2.imshow('frame2', frame2)
    key = cv2.waitKey(1) & 0xFF # Put waitKey code here to end
    if time() - timeStart > timeLimit or key == ord("q"): # press 'q' key to break loop
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
vs0.stop() # stop() is for VideoStream object
vs2.stop() # stop() is for VideoStream object
out0.release()
out2.release()

picklePath = '/home/pi/process/gaitSpeedRecorded/' + stamp + ' gaitSpeed.pkl'
# os.mkdir(picklePath)
dataList = "dataList, correctDist, timeLimit, fast, " \
           + "pattern, height, width, doctor, patientID, " \
           + "fps, t_raw_, recordTime, recordFrames, record_fps, " \
           + "stamp, setupTime"
dataSet=[dataList, correctDist, timeLimit, fast, \
         pattern, height, width, doctor, patientID, \
         fps, t_raw_, recordTime, recordFrames, record_fps, \
         stamp, setupTime]
with open(picklePath,'wb') as f:
    pickle.dump(dataSet,f)

print ('ALL DONE\n\n')

