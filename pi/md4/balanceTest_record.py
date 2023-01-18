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
import pickle

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

timeLimit = 11.0
t_ = []

stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
balanceRecord = '/home/pi/process/balanceRecorded/'+ stamp + ' balanceRecord.avi'
vs1 = VideoStream(usePiCamera=True,resolution=(fwidth,fheight)).start()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out1 = cv2.VideoWriter(balanceRecord,fourcc, fps, (sliceWidth,sliceHeight))
fc1 = 0

sleep(1.0) # Self testing: sleep(6.0). Testing others: sleep(1.0)
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
recordFrames = fc1
record_fps = recordFrames/recordTime
print ('recordTime = {:.3f} s'.format(recordTime))
print ('recordFrames = ', recordFrames)
print ('record_fps = {:.3f} frames/second for new fps'.format(record_fps))
print ('Set fps = {:.3f} frames/second'.format(fps))

cv2.destroyAllWindows() # begin ending code
vs1.stop() # stop() is for VideoStream object
out1.release()

picklePath = '/home/pi/process/balanceRecorded/' + stamp + ' balance.pkl'
# os.mkdir(picklePath)
dataList = "dataList, fps, fwidth, " \
         + "sliceWidth, sliceHeight, t_, " \
         + "stamp, setupTime, recordTime" \
         + "recordFrames, record_fps"
dataSet=[dataList, fps, fwidth, \
         sliceWidth, sliceHeight, t_, \
         stamp, setupTime, recordTime, \
         recordFrames, record_fps]
with open(picklePath,'wb') as f:
    pickle.dump(dataSet,f)

print ('\nALL DONE\n')     
    
