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
win.title("Camera Menu")
myFont = tkinter.font.Font(family = 'Helvetica', size = 18, \
    weight = "bold")
myFont2 = tkinter.font.Font(family = 'Helvetica', size = 42, \
    weight = "bold")
win.geometry("+200+40")
    # case of both size & position ("1200x700+100+100")
var = StringVar(win)
var.set("0")
var2 = StringVar(win)
var2.set("0")
var3 = StringVar(win)
var3.set("0")
var4 = StringVar(win)
var4.set("0")

### Event Functions ###
def turnLeftRight():
    # command to run goToAngle.py with three integer arguments
    # Example 1: python3 goToAngle.py 10 1
    # It turns camera platform 10 degrees to the right (roughly).
    # Example 2: python3 goToAngle.py -10 1
    # It turns camera platform 10 degrees to the left (roughly).
    print ('turnLeftRight function')
    xangle1 = numOption.get()
    call(["python3", "/home/pi/md4/goToAngle1.py", str(xangle1), "0"])
    # call(["python3", "/home/pi/md4/goToAngle2cameras.py", str(xangle1), "0"])

def turnUpDown():
    # command to run goToAngle.py with three integer arguments
    # Example 1: python3 goToAngle.py 10 2
    # It turns camera platform 10 degrees upward (roughly).
    # Example 2: python3 goToAngle.py -10 1
    # It turns camera platform 10 degrees downward (roughly).
    print ('turnUpDown function')
    yangle2 = numOption2.get()
    call(["python3", "/home/pi/md4/goToAngle1.py", str(yangle2), "1"])
    # call(["python3", "/home/pi/md4/goToAngle2cameras.py", str(yangle2), "1"])

def goToXAngle():
    # command to run goToAngle.py with three integer arguments
    # Example 1: python3 goToAngle.py 10
    # It turns camera platform to the 10 degree position.
    # Example 2: python3 sh.py -5
    # It turns camera platform to the -5 degree position.
    print ('goToXAngle function')
    xangle = numOption3.get()
    call(["python3", "/home/pi/md4/goToAngle1.py", str(xangle), "2"])
    # call(["python3", "/home/pi/md4/goToAngle2cameras.py", str(xangle), "2"])
    
def goToYAngle():
    # command to run goToAngle.py with three integer arguments
    # Example 1: python3 goToAngle.py 0 3 10
    # It turns camera platform upward to the 10 degree position.
    # Example 2: python3 sh.py 0 3 -5
    # It turns camera platform downward to the -5 degree position.
    print ('goToYAngle function')
    yangle = numOption4.get()
    call(["python3", "/home/pi/md4/goToAngle1.py", str(yangle), "3"])
    # call(["python3", "/home/pi/md4/goToAngle2cameras.py", str(yangle), "3"])

def getFaceAngle():
    # command to run getFaceAngle.py
    # Angles will be posted in Thonny Shell at the bottom
    print ('getFaceAngle function')
    call(["python3", "/home/pi/md4/getFaceAngle.py"])

def close():
    win.destroy()

### WIDGETS ###
bW = 45 # bW
a = 'w' # alignment. The 9 positions are w=left, e=right, n=upper, s=lower,
    # ne=upper right, se=lower right, nw=upper left, sw=lower left, center=center
bH = 2 # buttonHeight
bG = 'bisque2'
w2 = 5

buttonHeading = Label(win, text="* Angle marker needed",
    font=myFont, bg="yellow"). grid(row=0,column=1)

# Spinbox - select from a range of predetermined values
numOption = Spinbox(win,
from_=-30, to = 30, increment=0.5, textvariable=var,
font=myFont2, bg=bG, width=w2)
numOption.grid(row=1,column=2)

turnLeftRightButton = Button(win,
text='Turn cameras a number of degrees left(+)/right(-)',
font=myFont, command= turnLeftRight, anchor=a, bg=bG, height=bH, width=bW)
turnLeftRightButton.grid(row=1,column=1)

# Spinbox2 - select from a range of predetermined values
numOption2 = Spinbox(win,
from_=-30, to = 30, increment=0.5, textvariable=var2,
font=myFont2, bg=bG, width=w2)
numOption2.grid(row=2,column=2)

turnUpDownButton = Button(win,
text='Turn cameras a number of degrees up(+)/down(-)',
font=myFont, command= turnUpDown, anchor=a, bg=bG, height=bH, width=bW)
turnUpDownButton.grid(row=2,column=1)

# Spinbox3 - select from a range of predetermined values
numOption3 = Spinbox(win,
from_=-20, to = 20, increment=0.5, textvariable=var3,
font=myFont2, bg=bG, width=w2)
numOption3.grid(row=3,column=2)

goToXAngleButton = Button(win,
text='Go to left(+)/right(-) angle position *',
font=myFont, command= goToXAngle, anchor=a, bg=bG, height=bH, width=bW)
goToXAngleButton.grid(row=3,column=1)

# Spinbox4 - select from a range of predetermined values
numOption4 = Spinbox(win,
from_=-20, to = 20, increment=0.5, textvariable=var4,
font=myFont2, bg=bG, width=w2)
numOption4.grid(row=4,column=2)

goToYAngleButton = Button(win,
text='Go to up(+)/down(-) angle position *',
font=myFont, command= goToYAngle, anchor=a, bg=bG, height=bH, width=bW)
goToYAngleButton.grid(row=4,column=1)

getFaceAngleButton = Button(win,
text='Get face angles to adjust camera direction to face *\n(See Xangle & Yangle in Shell)',
font=myFont, command= getFaceAngle, anchor=a, bg=bG, height=bH, width=bW)
getFaceAngleButton.grid(row=5,column=1)

# Row 6 is space between buttons
win.grid_rowconfigure(6, minsize=10) # minsize is minimum height of the row.


# CREATE IMAGES
# Create the PIL image objects
image1 = Image.open("/home/pi/md4/images/turnLeftRight.png")
photo1 = ImageTk.PhotoImage(image1)
img_label1 = tk.Label(image=photo1)
img_label1.image = photo1
img_label1.grid(row=1, column=0)

image2 = Image.open("/home/pi/md4/images/turnUpDown.png")
photo2 = ImageTk.PhotoImage(image2)
img_label2 = tk.Label(image=photo2)
img_label2.image = photo2
img_label2.grid(row=2, column=0)

image3 = Image.open("/home/pi/md4/images/goToXAngle.png")
photo3 = ImageTk.PhotoImage(image3)
img_label3 = tk.Label(image=photo3)
img_label3.image = photo3
img_label3.grid(row=3, column=0)

image4 = Image.open("/home/pi/md4/images/goToYAngle.png")
photo4 = ImageTk.PhotoImage(image4)
img_label4 = tk.Label(image=photo4)
img_label4.image = photo4
img_label4.grid(row=4, column=0)

image5 = Image.open("/home/pi/md4/images/findFaceAngles2.png")
photo5 = ImageTk.PhotoImage(image5)
img_label5 = tk.Label(image=photo5)
img_label5.image = photo5
img_label5.grid(row=5, column=0)

exitButton = Button(win,
text='Exit',
font=myFont, command=close, anchor='center', bg='red', height=bH, width=20)
exitButton.grid(columnspan=3, row=7, column=0)

win.protocol("WM_DELETE_WINDOW", close)
win.mainloop() # Loops forever
