# This program reads in pairs of video files from the folder, /home/pi/process/gaitSpeedRecorded.
# For each pair, it outputs a processed video file and 2 or 4 plot files.
# Output files go to the foolder, /home/pi/process/gaitSpeedProcessed.
# Each group of files has the same date & time stamp.
from time import sleep, time
loopStart = time()
print (__file__)
import os
from subprocess import call
import pickle
entries = sorted(os.listdir('/home/pi/process/balanceRecorded'))
print('entries = \n', entries)
print('type(entries) = ', type(entries))
entriesLength = len(entries)
print('entriesLength = ', entriesLength)
pairs = entriesLength//2
print('pairs = ', pairs)
TotalRecordTime = 0.0

if entriesLength % 2 == 0:
    for i in range(0, entriesLength, 2):
        picklePath = '/home/pi/process/balanceRecorded/' + entries[i]
        centerVideo = '/home/pi/process/balanceRecorded/' + entries[i+1]
        print('FILES: ', picklePath, ', ', centerVideo)
        
        # to read the data back into variables with pickle
        with open(picklePath, 'rb') as f2:
            # picklePath is a string path ending in a .pkl file (.pickle)
            dataLoad = pickle.load(f2) # must remember order to retreive it properly
            
        recordTime = dataLoad[8]
        TotalRecordTime = TotalRecordTime + recordTime

        call(["python3", "/home/pi/md4/balanceTest_process.py", picklePath, centerVideo])
        print("\n", i//2+1, " completed of ", pairs, " loops.\n")
        
    loopTime = time() - loopStart
    print("Total processing time = {:.3f} s for {} loops or runs.".format(loopTime, pairs))
    print("Time Per Run = {:.3f} s.".format(loopTime/pairs))
    print("TotalRecordTime = {:.3f} s.".format(TotalRecordTime))
    print("There is {:.3f} s of processing time for each second of recording time.".format(loopTime/TotalRecordTime))
else:
    print("Check the files in balanceRecorded folder because entriesLength is not a multiple of 2")
print("\nALL DONE")
