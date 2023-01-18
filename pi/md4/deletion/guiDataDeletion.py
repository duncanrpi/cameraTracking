# guiDataDeletion.py
from tkinter import *
import tkinter as tk
import tkinter.font
from subprocess import call
from PIL import Image, ImageTk

### GUI DEFINITIONS ###
win = Tk()
win.title("Data Deletion")
myFont = tkinter.font.Font(family = 'Helvetica', size = 18, \
    weight = "bold")
myFont2 = tkinter.font.Font(family = 'Helvetica', size = 42, \
    weight = "bold")
win.geometry("+200+40")
    # case of both size & position ("1200x700+100+100")

### Event Functions ###
def deleteData():
    print ('deleteData function')
    
    b_file = open("/home/pi/md4/TXT_CSV/balanceTest.csv", "w")
    b_file.truncate()
    b_file.write('Time stamp,Time,Doctor,Patient ID,,setupTime,recordTime,' \
        + 'processTime,totalTime\n')
    b_file.write('(y-m-d h:m:s),(s),,,,(s),(s),(s),(s)\n')
    b_file.close()
    
    b_file = open("/home/pi/md4/TXT_CSV/balanceTest.txt", "w")
    b_file.truncate()
    b_file.close()    
    
        
    b_file = open("/home/pi/md4/TXT_CSV/dataPoints.csv", "w")
    b_file.truncate()
    b_file.close()
    

    b_file = open("/home/pi/md4/TXT_CSV/gaitSpeed.csv", "w")
    b_file.truncate()
    b_file.close()
    
    a_file = open("/home/pi/md4/TXT_CSV/gaitSpeedError.csv", "w")
    a_file.truncate()
    a_file.write('0\n')
    a_file.close()
    
    
    b_file = open("/home/pi/md4/TXT_CSV/sitStand.csv", "w")
    b_file.truncate()
    b_file.write('Time stamp,Time,Doctor,Patient ID\n')
    b_file.write(',(s),,( )\n')
    b_file.close()

    b_file = open("/home/pi/md4/TXT_CSV/sitStand.txt", "w")
    b_file.truncate()
    b_file.close()


    b_file = open("/home/pi/md4/TXT_CSV/tugTest.csv", "w")
    b_file.truncate()
    b_file.write('Time stamp,Time,Doctor,Patient ID\n')
    b_file.write(',(s),,( )\n')
    b_file.close()
    
    b_file = open("/home/pi/md4/TXT_CSV/tugTest.txt", "w")
    b_file.truncate()
    b_file.close()
    

    print ('Contents of data-related files have been deleted.\n' \
           + 'A new set of runs will be started.')
    close()

def noDeleteClose():
    print ('Nothing was deleted')
    win.destroy()
    
def close():
    win.destroy()

### WIDGETS ###
# Button, triggers the connected command when it is pressed
bW = 21 # bW
a = 'w' # alignment. The 9 positions are w=left, e=right, n=upper, s=lower,
    # ne=upper right, se=lower right, nw=upper left, sw=lower left, center=center
bH = 2 # buttonHeight
bG = 'bisque2'

buttonHeading = Message(win, text="Are you sure that you want to delete all the " \
        + "data information from all the previous runs?\n\nThe contents of the two following files " \
        + "will be deleted to prepare for a new set of runs.\n\n/home/pi/md4/TXT_CSV/gaitSpeed.csv\n" \
        + "/home/pi/md4/TXT_CSV/gaitSpeedError.csv",
    font=myFont, bg="yellow", aspect=268). grid(row=0,columnspan=2,column=0)

noButton = Button(win,
text='No.\nDo not delete anything.',
font=myFont, command= noDeleteClose, bg='lightblue', height=bH, width=bW)
noButton.grid(row=1,column=0)

yesButton = Button(win,
text='Yes.\nDo the deletions.',
font=myFont, command= deleteData, bg='orange', height=bH, width=bW)
yesButton.grid(row=1,column=1)

# Row 2 is space between buttons
win.grid_rowconfigure(2, minsize=10) # minsize is minimum height of the row.

exitButton = Button(win,
text='Exit',
font=myFont, command=close, anchor='center', bg='red', height=bH, width=20)
exitButton.grid(columnspan=2, row=3, column=0)

win.protocol("WM_DELETE_WINDOW", close)
win.mainloop() # Loops forever
