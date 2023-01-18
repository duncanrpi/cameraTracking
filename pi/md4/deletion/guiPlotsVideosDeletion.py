# guiPlotsVideosDeletion.py
from tkinter import *
import tkinter as tk
import tkinter.font
from subprocess import call
from PIL import Image, ImageTk
from pathlib import Path

### GUI DEFINITIONS ###
win = Tk()
win.title("Plot & Video Files Deletion")
myFont = tkinter.font.Font(family = 'Helvetica', size = 18, \
    weight = "bold")
myFont2 = tkinter.font.Font(family = 'Helvetica', size = 42, \
    weight = "bold")
win.geometry("+200+40")
    # case of both size & position ("1200x700+100+100")

### Event Functions ###
def deleteFiles():
    print ('deleteFiles function')
    [f.unlink() for f in Path("/home/pi/runs").glob("*") if f.is_file()]
    [f.unlink() for f in Path("/home/pi/runsBalance").glob("*") if f.is_file()]
    [f.unlink() for f in Path("/home/pi/runsSitStand").glob("*") if f.is_file()]
    [f.unlink() for f in Path("/home/pi/runsTUG").glob("*") if f.is_file()]
    print ('Plot and video files at /home/pi/runs have been deleted.')
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
        + "plot and video files from all the previous runs?\n\n" \
        + "All the files in /home/pi/runs will be deleted.",
    font=myFont, bg="yellow", aspect=268). grid(row=0,columnspan=2,column=0)

noButton = Button(win,
text='No.\nDo not delete anything.',
font=myFont, command= noDeleteClose, bg='lightblue', height=bH, width=bW)
noButton.grid(row=1,column=0)

yesButton = Button(win,
text='Yes.\nDo the deletions.',
font=myFont, command= deleteFiles, bg='orange', height=bH, width=bW)
yesButton.grid(row=1,column=1)

# Row 2 is space between buttons
win.grid_rowconfigure(2, minsize=10) # minsize is minimum height of the row.

exitButton = Button(win,
text='Exit',
font=myFont, command=close, anchor='center', bg='red', height=bH, width=20)
exitButton.grid(columnspan=2, row=3, column=0)

win.protocol("WM_DELETE_WINDOW", close)
win.mainloop() # Loops forever
