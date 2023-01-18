# DO NOT SET THIS TO OPEN AT BOOT UP TIME UNLESS IT HAS BEEN TESTED FIRST.
# IT WILL RUIN THE IMAGE ON THE SD CARD SO THAT YOU CANNOT BOOT UP.
# guiAll.py
## run various Python scripts, some with arguments ##
from tkinter import *
import tkinter as tk
import tkinter.font
from subprocess import call
from PIL import Image, ImageTk


### GUI DEFINITIONS ###
win = Tk()
win.title("Frame Rate Menu")
myFont = tkinter.font.Font(family = 'Helvetica', size = 18, \
    weight = "bold")
myFont2 = tkinter.font.Font(family = 'Helvetica', size = 42, \
    weight = "bold")
win.geometry("+200+40")
    # case of both size & position ("1200x700+100+100")

### Event Functions ###
def frameRate():
    print ('frameRate function')
    call(["python3", "/home/pi/md4/PROCESSFrameRate.py"])
    
def helpFrameRate():
    print ('helpFrameRate function')
    call(["lowriter","/home/pi/md4/help/helpFrameRate.odt"])
    
    
def startEnd():
    print ('startEnd function')
    call(["python3", "/home/pi/md4/PROCESS_StartEnd.py"])
    
def helpStartEnd():
    print ('helpStartEnd function')
    call(["lowriter","/home/pi/md4/help/helpStartEnd.odt"])  

def close():
    win.destroy()

### WIDGETS ###
W1 = 23
W2 = 15
W12 = W1+W2
a = 'w' # alignment. The 9 positions are w=left, e=right, n=upper, s=lower,
    # ne=upper right, se=lower right, nw=upper left, sw=lower left, center=center
bG = 'bisque2'

buttonHeading = Label(win, text="TASKS", font=myFont, bg="lightgreen", \
        height=1, width=W1). grid(row=0,column=1)

frameRateButton = Button(win, text='Video frame rate change',
font=myFont, command= frameRate, anchor="center", bg=bG, height=2, width=W1)
frameRateButton.grid(row=1,column=1)

startEndButton = Button(win, text='Gait speed start end lines',
font=myFont, command= startEnd, anchor="center", bg=bG, height=2, width=W1)
startEndButton.grid(row=2,column=1)

HelpTitle = Label(win, text="HELP", font=myFont, bg="lightgreen", \
        width=W2, height=1). grid(row=0,column=2)

helpFrameRateButton = Button(win, text='Help Frame Rate',
font=myFont, command=helpFrameRate, anchor='center', bg='yellow', height=2, width=W2)
helpFrameRateButton.grid(row=1, column=2)

helpStartEndButton = Button(win, text='Help Start End',
font=myFont, command=helpStartEnd, anchor='center', bg='yellow', height=2, width=W2)
helpStartEndButton.grid(row=2, column=2)

# Row 6 is space between buttons
win.grid_rowconfigure(2, minsize=10) # minsize is minimum height of the row.
"""
# CREATE IMAGES
# Create the PIL image objects
image1 = Image.open("/home/pi/md4/images/turnLeftRight.png")
photo1 = ImageTk.PhotoImage(image1)
img_label1 = tk.Label(image=photo1)
img_label1.image = photo1
img_label1.grid(row=1, column=0)
"""
exitButton = Button(win,
text='Exit',
font=myFont, command=close, anchor='center', bg='red', height=2, width=W12)
exitButton.grid(columnspan=2, row=3, column=1)

win.protocol("WM_DELETE_WINDOW", close)
win.mainloop() # Loops forever
