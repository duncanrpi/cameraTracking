# This program reads in video files from the folder, /home/pi/process/oldFrameRate.
# The file, _frameRateData.txt, is in csv format. Each line is stamp, record_fps.
# record_fps will be the new frame rate for each video file.
# For each video it calls frameRateProcess.py with arguments stamp, record_fps.
# Output files go to /home/pi/process/frameRateProcessed folder.
from time import sleep, time
loopStart = time()
import os
from subprocess import call
import csv
import operator

print (__file__)
dataPath = '/home/pi/process/frameRateData.txt'
sample = open(dataPath,'r') # txt or csv works
print ('type(sample) = ',type(sample))
csv1 = csv.reader(sample,delimiter=',')
print ('type(csv1) = ',type(csv1))
stampFps = sorted(csv1,key=operator.itemgetter(0)) # sort by stamp (0 column)

entries = sorted(os.listdir('/home/pi/process/oldFrameRate'))
pathPart = '/home/pi/process/oldFrameRate'
print('entries = \n', entries)
print('type(entries) = ', type(entries))
entriesLength = len(entries)
print('entriesLength = ', entriesLength)
totalTime = 0.0

if entriesLength > 0:
    for i in range(entriesLength):
        fileName = entries[i]
        # filePath = '' + pathPart + entries[i]
        print('\n', fileName)
        # stamp = stampFps[i][0]
        record_fps = stampFps[i][1]

        call(["python3", "/home/pi/md4/frameRateProcess.py", fileName, record_fps])
        print(i+1, " completed of ", entriesLength, " loops.")
        
    loopTime = time() - loopStart
    totalTime = totalTime + loopTime
    print("\nTotal processing time = {:.3f} s for {} loops or runs.".format(loopTime, entriesLength))
    print("Time Per Run = {:.3f} s.".format(loopTime/entriesLength))
else:
    print("Check if there are any video files in oldFrameRate folder.")
print("\nALL DONE")
