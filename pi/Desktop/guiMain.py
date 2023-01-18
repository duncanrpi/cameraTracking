# DO NOT SET THIS TO OPEN AT BOOT UP TIME UNLESS IT HAS BEEN TESTED FIRST.
# IT WILL RUIN THE IMAGE ON THE SD CARD SO THAT YOU CANNOT BOOT UP.
# guiMain.py
## run various Python scripts, some with arguments ##
from tkinter import *
import tkinter as tk
import tkinter.font
from subprocess import call
from PIL import Image, ImageTk


### GUI DEFINITIONS ###
win = Tk()
win.title("Main Menu")
myFont = tkinter.font.Font(family = 'Helvetica', size = 18, \
    weight = "bold")
myFont2 = tkinter.font.Font(family = 'Helvetica', size = 42, \
    weight = "bold")
myFont12 = tkinter.font.Font(family = 'Helvetica', size = 12, \
    weight = "bold")
win.geometry("+100+40")
    # case of both size & position ("1200x700+100+100")
var = StringVar(win)
var.set("0")
var2 = StringVar(win)
var2.set("0")
var3 = StringVar(win)
var3.set("0")


### Event Functions ###
def walk():
    # command to run guiWalk.py
    print ('walk gui')
    call(["python3", "/home/pi/Desktop/guiWalk.py"])

def camera():
    # command to run guiCamera.py
    print ('camera gui')
    call(["python3", "/home/pi/Desktop/guiCamera.py"])

def setup():
    # command to run guiSetup.py
    print ('setup gui')
    call(["python3", "/home/pi/Desktop/guiSetup.py"])

def close():
    # RPi.GPIO.cleanup()
    win.destroy()

### WIDGETS ###
# Button, triggers the connected command when it is pressed
bW = 18 # bW
bW2 = 54
a = 'w' # alignment. The 9 positions are w=left, e=right, n=upper, s=lower,
    # ne=upper right, se=lower right, nw=upper left, sw=lower left, center=center
bH = 2 # buttonHeight
bG = 'bisque2'

# column 1 buttons
walkButton = Button(win,
text='Walk/Sit/Stand Menu',
font=myFont, command= walk, anchor=a, bg=bG, height=bH, width=bW)
walkButton.grid(row=1,column=1)

cameraButton = Button(win,
text='Camera Menu',
font=myFont, command= camera, anchor=a, bg=bG, height=bH, width=bW)
cameraButton.grid(row=2,column=1)

setupButton = Button(win,
text='Setup Menu',
font=myFont, command= setup, anchor=a, bg=bG, height=bH, width=bW)
setupButton.grid(row=3,column=1)

# Row 4 is space between buttons
win.grid_rowconfigure(4, minsize=15) # minsize is minimum height of the row.


# column 0 CREATE IMAGES
# Create the PIL image objects
image1 = Image.open("/home/pi/md4/images/walkAnywhere.png")
    # type(image)= <class 'PIL.PngImagePlugin.PngImageFile'>
photo1 = ImageTk.PhotoImage(image1)
    # type(photo)= <class 'PIL.ImageTk.PhotoImage'>
# Create an image label
img_label1 = tk.Label(image=photo1)
# Store a reference to a PhotoImage object, to avoid it
# being garbage collected! This is necesary to display the image!
img_label1.image = photo1
img_label1.grid(row=1, column=0)

image2 = Image.open("/home/pi/md4/images/goToYAngle.png")
photo2 = ImageTk.PhotoImage(image2)
img_label2 = tk.Label(image=photo2)
img_label2.image = photo2
img_label2.grid(row=2, column=0)

image3 = Image.open("/home/pi/md4/images/setup.png")
photo3 = ImageTk.PhotoImage(image3)
img_label3 = tk.Label(image=photo3)
img_label3.image = photo3
img_label3.grid(row=3, column=0)


# column 2 HELP
help0 = Label(win, text="Explanation", font=myFont, bg="yellow", width=bW2). grid(row=0,column=2)
help1 = Label(win, text="Track a person walking left, right, or toward the cameras.\n "
    +"Run a TUG Test or Sit-Stand Test. Upload data. Clear data.",
    font=myFont, bg="yellow", width=bW2). grid(row=1,column=2)
help2 = Label(win, text="Move the cameras left, right, up, or down.\n "
    +"Find angle position of face.",
    font=myFont, bg="yellow", width=bW2). grid(row=2,column=2)
help3 = Label(win, text="Find markers. Record videos.\n "
    +"Calibrate cameras to be parallel or nonparallel.",
    font=myFont, bg="yellow", width=bW2). grid(row=3,column=2)

exitButton = Button(win,
text='Exit',
font=myFont, command=close, anchor='center', bg='red', height=bH, width=20)
exitButton.grid(columnspan=3, row=5, column=0)

win.protocol("WM_DELETE_WINDOW", close)
win.mainloop() # Loops forever
