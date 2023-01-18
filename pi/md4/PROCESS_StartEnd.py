# startAndEndLines.py

# This program reads in video files from the folder, /home/pi/process/videosNoLines.
# The file, startEndData.txt, is in csv format. Each line is stamp, start_i+1, end_i+1.
# Output files go to /home/pi/process/videosLines folder.
from time import sleep, time
loopStart = time()
import os
from subprocess import call
import csv
import operator

print (__file__)
dataPath = '/home/pi/process/startEndData.txt'
sample = open(dataPath,'r') # txt or csv works
print ('type(sample) = ',type(sample))
csv1 = csv.reader(sample,delimiter=',')
print ('type(csv1) = ',type(csv1))
stampStartEnd = sorted(csv1,key=operator.itemgetter(0)) # sort by stamp (0 column)

entries = sorted(os.listdir('/home/pi/process/videosNoLines'))
pathPart = '/home/pi/process/videosNoLines'
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
        # stamp = stampStartEnd[i][0]
        startPixels = stampStartEnd[i][1]
        endPixels = stampStartEnd[i][2]

        call(["python3", "/home/pi/md4/startEndProcess.py", fileName, startPixels, endPixels])
        print(i+1, " completed of ", entriesLength, " loops.")
        
    loopTime = time() - loopStart
    totalTime = totalTime + loopTime
    print("\nTotal processing time = {:.3f} s for {} loops or runs.".format(loopTime, entriesLength))
    print("Time Per Run = {:.3f} s.".format(loopTime/entriesLength))
else:
    print("Check if there are any video files in oldFrameRate folder.")
print("\nALL DONE")

