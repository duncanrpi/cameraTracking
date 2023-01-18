# This program reads in pairs of video files from the folder, /home/pi/process/gaitSpeedRecorded.
# For each pair, it outputs a processed video file and 2 or 4 plot files.
# Output files go to the foolder, /home/pi/process/gaitSpeedProcessed.
# Each group of files has the same date & time stamp.
from time import sleep, time
loopStart = time()
import os
from subprocess import call
import pickle
print (__file__)
entries = sorted(os.listdir('/home/pi/process/gaitSpeedRecorded'))
print('entries = \n', entries)
print('type(entries) = ', type(entries))
entriesLength = len(entries)
print('entriesLength = ', entriesLength)
triples = entriesLength//3
print('triples = ', triples)
TotalRecordTime = 0.0

if entriesLength % 3 == 0:
    for i in range(0, entriesLength, 3):
        picklePath = '/home/pi/process/gaitSpeedRecorded/' + entries[i]
        leftVideo = '/home/pi/process/gaitSpeedRecorded/' + entries[i+1]
        rightVideo = '/home/pi/process/gaitSpeedRecorded/' + entries[i+2]
        print('FILES: ', picklePath, ', ', leftVideo, ', ', rightVideo)
        
        # to read the data back into variables with pickle
        with open(picklePath, 'rb') as f2:
            # picklePath is a string path ending in a .pkl file (.pickle)
            dataLoad = pickle.load(f2) # must remember order to retreive it properly
            
        recordTime = dataLoad[12]
        TotalRecordTime = TotalRecordTime + recordTime

        call(["python3", "/home/pi/md4/gaitSpeed_2D (36)process.py", picklePath, leftVideo, rightVideo])
        print("\n", i//3+1, " completed of ", triples, " loops.\n")
        
    loopTime = time() - loopStart
    print("Total processing time = {:.3f} s for {} loops or runs.".format(loopTime, triples))
    print("Time Per Run = {:.3f} s.".format(loopTime/triples))
    print("TotalRecordTime = {:.3f} s.".format(TotalRecordTime))
    print("There is {:.3f} s of processing time for each second of recording time.".format(loopTime/TotalRecordTime))
else:
    print("Check the files in gaitSpeedRecorded folder because entriesLength is not a multiple of 3")
print("\nALL DONE")
