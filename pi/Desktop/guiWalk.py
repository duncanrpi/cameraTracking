# DO NOT SET THIS TO OPEN AT BOOT UP TIME UNLESS IT HAS BEEN TESTED FIRST.
# IT WILL RUIN THE IMAGE ON THE SD CARD SO THAT YOU CANNOT BOOT UP.
## run various Python scripts, some with arguments ##
from tkinter import *
import tkinter as tk
from tkinter import ttk
from time import sleep
import tkinter.font
from subprocess import call
from PIL import Image, ImageTk
import csv
from datetime import datetime, timedelta

### GUI DEFINITIONS ###
win = Tk()
win.title("Walk/Sit/Stand Menu")
myFont = tkinter.font.Font(family = 'Helvetica', size = 18, \
    weight = "bold")
myFont2 = tkinter.font.Font(family = 'Helvetica', size = 42, \
    weight = "bold")
myFont9 = tkinter.font.Font(family = 'Helvetica', size = 9, \
    weight = "bold")
myFont12 = tkinter.font.Font(family = 'Helvetica', size = 12, \
    weight = "bold")

win.geometry("+350+40") # setting position only (x=200, y=40, for position of upper left of gui window)
    # case of setting both size & position ("1200x700+200+40") where 1200x700 is size
    
### Variable Definitions for widgets ###
out1 = StringVar()
out1.set("")
out2 = StringVar()
out2.set("")
out3 = StringVar()
out3.set("")
out4 = StringVar()
out4.set("")
out5 = StringVar()
out5.set("")
out6 = StringVar()
out6.set("")
out7 = StringVar()
out7.set("")
out8 = StringVar()
out8.set("")
out10 = StringVar()
out10.set("")
out12 = StringVar()
out12.set("")
out14 = StringVar()
out14.set("")
checkVal1 = IntVar()
# checkVal1.set(0)
checkVal2 = IntVar()
# checkVal2.set(0)

# FIX
global select1, select2, defaultbg, defaultTimeLimit, timeFactor
global fast, timeLimit, estTime, display, display2
select1, select2 = 0, 0
fast = "0"
if fast == "1":
    timeFactor = 19.0 # output 2 figures. timeFactor * recording time = overall time
else:
    timeFactor = 26.0 # output 4 figures
defaultbg = win.cget("bg") # a light gray background color

    
### GAITSPEED Functions ###

def recordRadial0():    
    print ('\nrecordRadial0 function')
    timeLimit = timeLimitEntryBox.get()
    estTime = int(timeLimit) * timeFactor / 60.0
    finishTime = datetime.now() + timedelta(minutes=estTime)
    estimatedFinishTime = finishTime.strftime("%H:%M")
    print ('defaultTimeLimit, estTime =', defaultTimeLimit, estTime)
    print ('finishTime, estimatedFinishTime =', finishTime, estimatedFinishTime)
    display.config(text='STATUS: PROCESSING ...',bg='yellow',font=myFont, \
                   height=2,borderwidth=5,relief="solid")
    display2.config(text='Estimated duration: {:.2f} min'.format(estTime) \
                     + '\nEstimated finishing time: ' + estimatedFinishTime, \
                     bg='yellow',font=myFont,height=2,borderwidth=5,relief="solid")    
    win.config(bg='#d1a4ff') # a light purple
    win.after(5, recordRadial)
def recordRadial():    
    correctDist = distanceEntryBox.get() # float (meters) there
    d = open("/home/pi/md4/TXT_CSV/distance.txt", "a")
    d.write(correctDist+'\n')
    d.close()
    
    timeLimit = timeLimitEntryBox.get()
    g = open("/home/pi/md4/TXT_CSV/timeLimit.txt", "a")
    g.write(timeLimit+'\n')
    g.close()

    pattern = "0" #  for path, 0='homeRad', 1='home4m', 2='home3m', 3='Mom', " \
                  # + "4='UAB', 5='hosp'
    height = "144"
    width = "640" # "512"
    
    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    doctor = doctorEntryBox.get()
    f.write(doctor+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    patientID = patientIDEntryBox.get()
    h.write(patientID+'\n')
    h.close()

    call(["python3", "/home/pi/md4/gaitSpeed_2D (36)record.py", correctDist, \
          timeLimit, fast, pattern, height, width, doctor, patientID])   
    
def step1Radial0():    
    print ('\nstep1Radial0 function')
    timeLimit = timeLimitEntryBox.get()
    estTime = int(timeLimit) * timeFactor / 60.0
    finishTime = datetime.now() + timedelta(minutes=estTime)
    estimatedFinishTime = finishTime.strftime("%H:%M")
    print ('defaultTimeLimit, estTime =', defaultTimeLimit, estTime)
    print ('finishTime, estimatedFinishTime =', finishTime, estimatedFinishTime)
    display.config(text='STATUS: PROCESSING ...',bg='yellow',font=myFont, \
                   height=2,borderwidth=5,relief="solid")
    display2.config(text='Estimated duration: {:.2f} min'.format(estTime) \
                     + '\nEstimated finishing time: ' + estimatedFinishTime, \
                     bg='yellow',font=myFont,height=2,borderwidth=5,relief="solid")    
    win.config(bg='#d1a4ff') # a light purple
    win.after(5, step1Radial)
def step1Radial():    
    correctDist = distanceEntryBox.get() # float (meters) there
    d = open("/home/pi/md4/TXT_CSV/distance.txt", "a")
    d.write(correctDist+'\n')
    d.close()
 
    timeLimit = timeLimitEntryBox.get()
    g = open("/home/pi/md4/TXT_CSV/timeLimit.txt", "a")
    g.write(timeLimit+'\n')
    g.close()

    pattern = "0" #  for path, 0='homeRad', 1='home4m', 2='home3m', 3='Mom', " \
                  # + "4='UAB', 5='hosp'
    height = "144"
    width = "640" # "512"
    
    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    doctor = doctorEntryBox.get()
    f.write(doctor+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    patientID = patientIDEntryBox.get()
    h.write(patientID+'\n')
    h.close()

    call(["python3", "/home/pi/md4/gaitSpeed_2D (36).py", correctDist, \
          timeLimit, fast, pattern, height, width, doctor, patientID])
    
    # This block must be commented out when the gaitSpeed program only does recording    
    with open("/home/pi/md4/TXT_CSV/gaitSpeedError.csv", 'r') as f:
        mycsv = csv.reader(f)
        lines = list(mycsv)
        out1.set(lines[-1][0])
        out2.set(lines[-1][1])
        out3.set(lines[-1][2]+' m')
        out4.set(lines[-1][3]+' m')
        out5.set(lines[-1][4][0:-1]+'%')
        out6.set(lines[-1][5][0:-1]+'%')
        out7.set(lines[-1][6]+' s')
        out8.set(lines[-1][7]+' m/s')        
        out10.set("")
        out12.set("")
        out14.set("")
    display.config(text='STATUS: PROCESS DONE, READY',bg='lightgreen', \
                   font=myFont,height=2,borderwidth=5,relief="solid")
    display2.config(text='Estimated duration: \nEstimated finishing time: ', \
                     bg='lightgreen',font=myFont,height=2,borderwidth=5,relief="solid")    
    win.config(bg=defaultbg)
    
def processGaitSpeed():
        call(["python3", "/home/pi/md4/PROCESSGaitSpeed.py"])
        
def recordCrosswise0(): 
    print ('\nrecordCrosswise0 function')
    timeLimit = timeLimitEntryBox.get()
    estTime = int(timeLimit) * timeFactor / 60.0
    finishTime = datetime.now() + timedelta(minutes=estTime)
    estimatedFinishTime = finishTime.strftime("%H:%M")
    print ('defaultTimeLimit, estTime =', defaultTimeLimit, estTime)
    print ('finishTime, estimatedFinishTime =', finishTime, estimatedFinishTime)
    display.config(text='STATUS: PROCESSING ...',bg='yellow',font=myFont, \
                   height=2,borderwidth=5,relief="solid")
    display2.config(text='Estimated duration: {:.2f} min'.format(estTime) \
                     + '\nEstimated finishing time: ' + estimatedFinishTime, \
                     bg='yellow',font=myFont,height=2,borderwidth=5,relief="solid")     
    win.config(bg='#d1a4ff') # a light purple
    win.after(5, recordCrosswise)
def recordCrosswise():
    correctDist = distanceEntryBox.get() # float (meters) there
    d = open("/home/pi/md4/TXT_CSV/distance.txt", "a")
    d.write(correctDist+'\n')
    d.close()
    
    timeLimit = timeLimitEntryBox.get()
    g = open("/home/pi/md4/TXT_CSV/timeLimit.txt", "a")
    g.write(timeLimit+'\n')
    g.close()

    pattern = "1" #  for path, 0='homeRad', 1='home4m', 2='home3m', 3='Mom', " \
                  # + "4='UAB', 5='hosp'
    height = "96"
    width = "640"

    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    doctor = doctorEntryBox.get()
    f.write(doctor+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    patientID = patientIDEntryBox.get()
    h.write(patientID+'\n')
    h.close()

    call(["python3", "/home/pi/md4/gaitSpeed_2D (36)record.py", correctDist, \
          timeLimit, fast, pattern, height, width, doctor, patientID])    
    
def step1Crosswise0():    
    print ('\nstep1Crosswise0 function')
    timeLimit = timeLimitEntryBox.get()
    estTime = int(timeLimit) * timeFactor / 60.0
    finishTime = datetime.now() + timedelta(minutes=estTime)
    estimatedFinishTime = finishTime.strftime("%H:%M")
    print ('defaultTimeLimit, estTime =', defaultTimeLimit, estTime)
    print ('finishTime, estimatedFinishTime =', finishTime, estimatedFinishTime)
    display.config(text='STATUS: PROCESSING ...',bg='yellow',font=myFont, \
                   height=2,borderwidth=5,relief="solid")
    display2.config(text='Estimated duration: {:.2f} min'.format(estTime) \
                     + '\nEstimated finishing time: ' + estimatedFinishTime, \
                     bg='yellow',font=myFont,height=2,borderwidth=5,relief="solid")     
    win.config(bg='#d1a4ff') # a light purple
    win.after(5, step1Crosswise)
def step1Crosswise():
    correctDist = distanceEntryBox.get() # float (meters) there
    d = open("/home/pi/md4/TXT_CSV/distance.txt", "a")
    d.write(correctDist+'\n')
    d.close()
   
    timeLimit = timeLimitEntryBox.get()
    g = open("/home/pi/md4/TXT_CSV/timeLimit.txt", "a")
    g.write(timeLimit+'\n')
    g.close()

    pattern = "1" #  for path, 0='homeRad', 1='home4m', 2='home3m', 3='Mom', " \
                  # + "4='UAB', 5='hosp'
    height = "96"
    width = "640"

    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    doctor = doctorEntryBox.get()
    f.write(doctor+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    patientID = patientIDEntryBox.get()
    h.write(patientID+'\n')
    h.close()

    call(["python3", "/home/pi/md4/gaitSpeed_2D (36).py", correctDist, \
          timeLimit, fast, pattern, height, width, doctor, patientID])
    
    # This block must be commented out when the gaitSpeed program only does recording
    with open("/home/pi/md4/TXT_CSV/gaitSpeedError.csv", 'r') as f:
        mycsv = csv.reader(f)
        lines = list(mycsv)
        out1.set(lines[-1][0])
        out2.set(lines[-1][1])
        out3.set(lines[-1][2]+' m')
        out4.set(lines[-1][3]+' m')
        out5.set(lines[-1][4]+'%')
        out6.set(lines[-1][5]+'%')
        out7.set(lines[-1][6]+' s')
        out8.set(lines[-1][7]+' m/s')        
        out10.set("")
        out12.set("")
        out14.set("")
    display.config(text='STATUS: PROCESS DONE, READY',bg='lightgreen', \
                   font=myFont,height=2,borderwidth=5,relief="solid")    
    display2.config(text='Estimated duration: \nEstimated finishing time: ', \
                     bg='lightgreen',font=myFont,height=2,borderwidth=5,relief="solid")    
    win.config(bg=defaultbg)
    
    
### STANDING BALANCE Functions ###
def recordStandingBalance():
    print ('\nrecordStandingBalance function')
    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    f.write(doctorEntryBox.get()+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    h.write(patientIDEntryBox.get()+'\n')
    h.close()
    
    call(["python3", "/home/pi/md4/balanceTest_record.py"])
    
def processStandingBalance():
    call(["python3", "/home/pi/md4/PROCESSBalance.py"])
    
    
def step1StandingBalance():
    print ('\nstep1StandingBalance function')
    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    f.write(doctorEntryBox.get()+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    h.write(patientIDEntryBox.get()+'\n')
    h.close()
    
    call(["python3", "/home/pi/md4/balanceTest_recordProcess.py"])
    
    a_file = open("/home/pi/md4/TXT_CSV/balanceTest.txt", "r")
    lines = a_file. readlines()
    out1.set(lines[-2][0:-1])
    out2.set("")
    out3.set("")
    out4.set("")
    out5.set("")
    out6.set("")    
    out7.set("")
    out8.set("")    
    out10.set(lines[-1][0:-1])
    out12.set("")
    out14.set("")
    a_file. close()
    
    
### SITSTAND, TUG, and SYNC Functions ###
def sitStand():
    print ('\nsitStand function')    
    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    f.write(doctorEntryBox.get()+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    h.write(patientIDEntryBox.get()+'\n')
    h.close()
    
    call(["python3", "/home/pi/md4/sitStand.py"])
    a_file = open("/home/pi/md4/TXT_CSV/sitStand.txt", "r")
    lines = a_file. readlines()
    out1.set(lines[-2][0:-1])
    out2.set("")
    out3.set("")
    out4.set("")
    out5.set("")
    out6.set("")
    out7.set("")
    out8.set("")
    out10.set("")
    out12.set(lines[-1][0:-1])
    out14.set("")
    a_file. close()    

def tugTest():
    print ('\ntugTest function')
    f = open("/home/pi/md4/TXT_CSV/doctor.txt", "a")
    f.write(doctorEntryBox.get()+'\n')
    f.close()
    
    h = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "a")
    h.write(patientIDEntryBox.get()+'\n')
    h.close()
    
    call(["python3", "/home/pi/md4/tugTest.py"])    
    a_file = open("/home/pi/md4/TXT_CSV/tugTest.txt", "r")
    lines = a_file. readlines()
    out1.set(lines[-2][0:-1])
    out2.set("")
    out3.set("")
    out4.set("")
    out5.set("")
    out6.set("")    
    out7.set("")
    out8.set("")    
    out10.set("")
    out12.set("")
    out14.set(lines[-1][0:-1])
    a_file. close()        
    
def sync():
    # This copies a Raspberry Pi folder contents to a folder in Google Drive
    # and in Dropbox, by overwriting.
    # Changes made to those folders do not come back to the Raspberry Pi folder.
    print ('\nsync function')
    # Google Drive
    call(["rclone","sync","-v","/home/pi/md4/TXT_CSV","gdrive:piTXT_CSV"])
    # Dropbox Drive
    call(["rclone","sync","-v","/home/pi/md4/TXT_CSV","dbdrive:Gait Speed Camera_Larry/piTXT_CSV"])   


### OPTIONS and HELP Functions ###
def newPatient():
    nums = []
    a_file = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "r")
    lines = a_file. readlines()
    for line in lines:
        num = int(line)
        nums.append(num)
    patientID = max(nums) + 1
    patientIDEntryBox.delete(0,END)
    patientIDEntryBox.insert(0,patientID) # str(patientID) ?
    a_file. close()

def helpWalk():
    print ('\nhelpWalk function')
    call(["lowriter","/home/pi/md4/help/helpWalk.odt"])
    
def helpBalance():
    print ('\nhelpBalance function')
    call(["lowriter","/home/pi/md4/help/helpBalance.odt"])

def helpStand():
    print ('helpStand function')
    call(["lowriter","/home/pi/md4/help/helpStand.odt"])
    
def helpDoctorPatient():
    print ('\nhelpDoctorPatient function')
    call(["lowriter","/home/pi/md4/help/helpDoctorPatient.odt"])

def helpTUG():
    print ('\nhelpTUG function')
    call(["lowriter","/home/pi/md4/help/helpTUG.odt"])
    
def helpSync():
    print ('\nhelpSync function')
    call(["lowriter","/home/pi/md4/help/helpSync.odt"])
    
def helpDelete():
    print ('\nhelpDelete function')
    call(["lowriter","/home/pi/md4/help/helpDelete.odt"])

def deleteData():
    print ('\ndeleteData function')
    call(["python3", "/home/pi/md4/deletion/guiDataDeletion.py"])

def deleteFiles():
    print ('\ndeleteFiles function')
    call(["python3", "/home/pi/md4/deletion/guiPlotsVideosDeletion.py"])

def close():
    # RPi.GPIO.cleanup()
    win.destroy()

### WIDGETS ###
# Button, triggers the connected command when it is pressed
W1 = 7
W2 = 6
W3 = 3
W4 = 6
W14 = W1+W2+W3+W4+5
W5 = 12
W6 = 6
bW = 25 # width of column 1
bW2,bW2b = 15,16 # width of column 2 and its entry boxes
bW3 = 6 # width of column 3
bW45 = 32 # width of 2-column labels, columns 4 & 5
a = 'w' # alignment. The 9 positions are w=left, e=right, n=upper, s=lower,
    # ne=upper right, se=lower right, nw=upper left, sw=lower left, center=center
bH = 2 # buttonHeight
bG = 'bisque2'
spaceheight = 8


# Column 0, IMAGES

# Create the PIL image objectS
image1 = Image.open("/home/pi/md4/images/walkToCamera2.png")
    # type(image)= <class 'PIL.PngImagePlugin.PngImageFile'>
photo1 = ImageTk.PhotoImage(image1)
    # type(photo)= <class 'PIL.ImageTk.PhotoImage'>
# Create an image label
img_label1 = tk.Label(image=photo1)
# Store a reference to a PhotoImage object, to avoid it
# being garbage collected! This is necesary to display the image!
img_label1.image = photo1
img_label1.grid(rowspan=2,row=1, column=0)

image2 = Image.open("/home/pi/md4/images/walkCrosswise.png")
photo2 = ImageTk.PhotoImage(image2)
img_label2 = tk.Label(image=photo2)
img_label2.image = photo2
img_label2.grid(rowspan=2,row=3, column=0)

image4 = Image.open("/home/pi/md4/images/standingBalance.png")
photo4 = ImageTk.PhotoImage(image4)
img_label4 = tk.Label(image=photo4)
img_label4.image = photo4
img_label4.grid(rowspan=2,row=5, column=0)

image5 = Image.open("/home/pi/md4/images/sitStand.png")
photo5 = ImageTk.PhotoImage(image5)
img_label5 = tk.Label(image=photo5)
img_label5.image = photo5
img_label5.grid(rowspan=2,row=7, column=0)

# Row 13 is a space

image6 = Image.open("/home/pi/md4/images/tugTest.png")
photo6 = ImageTk.PhotoImage(image6)
img_label6 = tk.Label(image=photo6)
img_label6.image = photo6
img_label6.grid(rowspan=2,row=11, column=0)

image7 = Image.open("/home/pi/md4/images/sync.png")
photo7 = ImageTk.PhotoImage(image7)
img_label7 = tk.Label(image=photo7)
img_label7.image = photo7
img_label7.grid(rowspan=2,row=13, column=0)


# Columns 1-4, TASKS

buttonHeading = Label(win, text="SPPB TASKS",
    font=myFont, bg="lightgreen", height=1, width=W14). grid(columnspan=4,row=0,column=1)

# Columns 1-2, TASK LABELS

gsLabel = Label(win, text="Gait\nSpeed\nTest", borderwidth=1,relief="solid",
    font=myFont, bg="lightgreen", height=5, width=W1). grid(rowspan=4,row=1,column=1)

recordRadialButton = Button(win, text='Record\nRadial',
font=myFont, command= recordRadial0, anchor="center", bg=bG, height=2, width=W2)
recordRadialButton.grid(rowspan=2,row=1,column=2)

recordCrosswiseButton = Button(win, text='Record\nCross\nwise',
font=myFont, command= recordCrosswise0, anchor="center", bg=bG, height=3, width=W2)
recordCrosswiseButton.grid(rowspan=2,row=3,column=2)

step1RadialButton = Button(win, text='In 1\nStep',
font=myFont, command= step1Radial0, anchor="center", bg=bG, height=2, width=W3)
step1RadialButton.grid(rowspan=2,row=1,column=3)

step1CrosswiseButton = Button(win, text='In 1\nStep',
font=myFont, command= step1Crosswise0, anchor="center", bg=bG, height=3, width=W3)
step1CrosswiseButton.grid(rowspan=2,row=3,column=3)

processGaitSpeedButton = Button(win, text='Process\nGait\nSpeed',
font=myFont, command= processGaitSpeed, anchor="center", bg=bG, height=5, width=W4)
processGaitSpeedButton.grid(rowspan=4,row=1,column=4)


standingBalanceLabel = Label(win, text="Balance\nTest", font=myFont, borderwidth=1,relief="solid",
bg="lightgreen", height=2, width=W1).grid(rowspan=2,row=5,column=1)

recordStandingBalanceButton = Button(win, text='Record\nBalance',
font=myFont, command= recordStandingBalance, anchor="center", bg=bG, height=2, width=W2)
recordStandingBalanceButton.grid(rowspan=2,row=5,column=2)

step1StandingBalanceButton = Button(win, text='In 1\nStep',
font=myFont, command= step1StandingBalance, anchor="center", bg=bG, height=2, width=W3)
step1StandingBalanceButton.grid(rowspan=2,row=5,column=3)

processStandingBalanceButton = Button(win, text='Process\nBalance',
font=myFont, command= processStandingBalance, anchor="center", bg=bG, height=2, width=W4)
processStandingBalanceButton.grid(rowspan=2,row=5,column=4)


sitStandButton = Button(win, text='Sit Stand Test',
font=myFont, command= sitStand, anchor="center", bg=bG, height=bH, width=W14)
sitStandButton.grid(columnspan=4,rowspan=2,row=7,column=1)

# Row 13 is a space between buttons
win.grid_rowconfigure(9, minsize=spaceheight) # minsize is minimum height of the row.

buttonHeading2 = Label(win, text="OTHER TASKS", font=myFont,
bg="lightgreen", height=1, width=W14). grid(columnspan=4,row=10,column=1)

tugTestButton = Button(win, text='TUG Test',
font=myFont, command= tugTest, anchor="center", bg=bG, height=bH, width=W14)
tugTestButton.grid(columnspan=4,rowspan=2,row=11,column=1)

syncButton = Button(win, text='Sync data to Google\n Drive & Dropbox',
font=myFont, command= sync, anchor="center", bg=bG, height=bH, width=W14)
syncButton.grid(columnspan=4,rowspan=2,row=13,column=1)


# Column 5, OPTIONS

OptionsTitle = Label(win, text="OPTIONS", font=myFont, bg="lightgreen", \
                     width=W5, height=1). grid(row=0,column=5)

distanceLabel = Label(win, text="Distance (m)", font=myFont). grid(row=1,column=5)
distanceEntryBox = Entry(win, width=W5, font=myFont)
distanceEntryBox. grid(row=2,column=5)

timeLimitLabel = Label(win, text="Record time (s)", font=myFont). grid(row=3,column=5)
timeLimitEntryBox = Entry(win, width=W5, font=myFont)
timeLimitEntryBox. grid(row=4,column=5)

doctorLabel = Label(win, text="Doctor", font=myFont). grid(row=5,column=5)
doctorEntryBox = Entry(win, width=W5, font=myFont)
doctorEntryBox. grid(row=6,column=5)

patientIDLabel = Label(win, text="Patient ID #", font=myFont). grid(row=7,column=5)
patientIDEntryBox = Entry(win, width=W5, font=myFont)
patientIDEntryBox. grid(row=8,column=5)

d_file = open("/home/pi/md4/TXT_CSV/distance.txt", "r")
lines = d_file. readlines()
defaultDistance = lines[-1][0:-1]
distanceEntryBox.insert(0,defaultDistance)
d_file. close()

c_file = open("/home/pi/md4/TXT_CSV/timeLimit.txt", "r")
lines = c_file. readlines()
defaultTimeLimit = lines[-1][0:-1]
timeLimitEntryBox.insert(0,defaultTimeLimit)
c_file. close()

a_file = open("/home/pi/md4/TXT_CSV/doctor.txt", "r")
lines = a_file. readlines()
defaultDoctor = lines[-1][0:-1]
doctorEntryBox.insert(0,defaultDoctor)
a_file. close()

nums = []
a_file = open("/home/pi/md4/TXT_CSV/patientIDNumber.txt", "r")
lines = a_file. readlines()
for line in lines:
    num = int(line)
    nums.append(num)
patientID = max(nums) + 1
patientIDEntryBox.insert(0,patientID) # str(patientID) ?
a_file. close()


newPatientButton = Button(win, text='New Patient\n ID Number',
font=myFont, command= newPatient, anchor='center', bg='lightblue', height=bH, width=W5)
newPatientButton.grid(rowspan=2,row=11,column=5)

# Row 13 is a space

deleteDataButton = Button(win, text='Delete old data\nReset runs to 0',
font=myFont, command= deleteData, anchor='center', bg='orange', height=bH, width=W5)
deleteDataButton.grid(rowspan=2,row=13,column=5)

deleteFilesButton = Button(win, text='Delete old\nplots & videos',
font=myFont, command= deleteFiles, anchor='center', bg='orange', height=bH, width=W5)
deleteFilesButton.grid(rowspan=2,row=15,column=5)


# Column 6, HELP BUTTONS

HelpTitle = Label(win, text="HELP", font=myFont, bg="lightgreen", \
                     width=W6, height=1). grid(row=0,column=6)

helpWalkButton = Button(win, text='Help\nWalk',
font=myFont, command=helpWalk, anchor='center', bg='yellow', height=5, width=W6)
helpWalkButton.grid(rowspan=4,row=1, column=6)

helpBalanceButton = Button(win, text='Help\nBalance',
font=myFont, command=helpBalance, anchor='center', bg='yellow', height=2, width=W6)
helpBalanceButton.grid(rowspan=2,row=5, column=6)

helpStandButton = Button(win, text='Help\nStand',
font=myFont, command=helpStand, anchor='center', bg='yellow', height=2, width=W6)
helpStandButton.grid(rowspan=2,row=7, column=6)

helpDoctorPatientButton = Button(win, text='Help Doctor Patient',
font=myFont, command=helpDoctorPatient, anchor='center', bg='yellow', height=1, width=W5+W6+2)
helpDoctorPatientButton.grid(columnspan=2,rowspan=2,row=9, column=5)

helpTUGButton = Button(win, text='Help\nTUG',
font=myFont, command=helpTUG, anchor='center', bg='yellow', height=2, width=W6)
helpTUGButton.grid(rowspan=2,row=11, column=6)

helpSyncButton = Button(win, text='Help\nSync',
font=myFont, command=helpSync, anchor='center', bg='yellow', height=2, width=W6)
helpSyncButton.grid(rowspan=2,row=13, column=6)

helpDeleteButton = Button(win, text='Help\nDelete',
font=myFont, command=helpDelete, anchor='center', bg='yellow', height=2, width=W6)
helpDeleteButton.grid(rowspan=2,row=15, column=6)

# Column 7, CREATE OUTPUT LABELS
label00 = Label(win, text="RESULTS", font=myFont, bg="lightgreen", \
               width=bW45, height=1). grid(columnspan=2,row=0,column=7)
label0 = Label(win, text="Run = ", font=myFont). grid(row=1,column=7,sticky=E)
label1 = Label(win, text="Time stamp = ", font=myFont). grid(row=2,column=7,sticky=E)
label2 = Label(win, text="Correct distance = ", font=myFont). grid(row=3,column=7,sticky=E)
label3 = Label(win, text="Detected distance = ", font=myFont). grid(row=4,column=7,sticky=E)
label4 = Label(win, text="Distance error = ", font=myFont). grid(row=5,column=7,sticky=E)
label5 = Label(win, text="Mean abs error = ", font=myFont). grid(row=6,column=7,sticky=E)
label6 = Label(win, text="Elapsed time = ", font=myFont). grid(row=7,column=7,sticky=E)
label7 = Label(win, text="Average speed = ", font=myFont). grid(row=8,column=7,sticky=E)

label10 = Label(win, text="Balance Elapsed time = ", font=myFont). grid(row=10,column=7,sticky=E)
label12 = Label(win, text="SitStand Elapsed time = ", font=myFont). grid(row=11,column=7,sticky=E)

# Row 13 is a space

label14 = Label(win, text="TUG Elapsed time = ", font=myFont). grid(row=12,column=7,sticky=E)

display = Label(win, text='STATUS:\nREADY',bg='lightgreen',font=myFont,height=2, \
                width=bW45,borderwidth=5,relief="solid")
display.grid(rowspan=2,columnspan=2,row=13,column=7)
display2 = Label(win, text='Estimated duration: \nEstimated finishing time: ', \
        bg='lightgreen',font=myFont,height=2,width=bW45,borderwidth=5,relief="solid") 
display2.grid(rowspan=2,columnspan=2,row=15,column=7)


# Column 8, CREATE OUTPUT BOXES
output1 = Label(win, textvariable=out1, font=myFont). grid(row=1,column=8,sticky=W)
output2 = Label(win, textvariable=out2, font=myFont). grid(row=2,column=8,sticky=W)
output3 = Label(win, textvariable=out3, font=myFont). grid(row=3,column=8,sticky=W)
output4 = Label(win, textvariable=out4, font=myFont). grid(row=4,column=8,sticky=W)
output5 = Label(win, textvariable=out5, font=myFont). grid(row=5,column=8,sticky=W)
output6 = Label(win, textvariable=out6, font=myFont). grid(row=6,column=8,sticky=W)
output7 = Label(win, textvariable=out7, font=myFont). grid(row=7,column=8,sticky=W)
output8 = Label(win, textvariable=out8, font=myFont). grid(row=8,column=8,sticky=W)

output10 = Label(win, textvariable=out10, font=myFont). grid(row=10,column=8,sticky=W)
output12 = Label(win, textvariable=out12, font=myFont). grid(row=11,column=8,sticky=W)

# Row 13 is a space

output14 = Label(win, textvariable=out14, font=myFont). grid(row=12,column=8,sticky=W)

exitButton = Button(win, text='Exit',
font=myFont, command=close, anchor='center', bg='red', height=bH, width=30)
exitButton.grid(columnspan=5, rowspan=2, row=15, column=0)

win.protocol("WM_DELETE_WINDOW", close)
win.mainloop() # Loops forever
