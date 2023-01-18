# DO NOT SET THIS TO OPEN AT BOOT UP TIME UNLESS IT HAS BEEN TESTED FIRST.
# IT WILL RUIN THE IMAGE ON THE SD CARD SO THAT YOU CANNOT BOOT UP.
# guiSetup.py
## run various Python scripts, some with arguments ##
from tkinter import *
import tkinter as tk
import tkinter.font
from subprocess import call
from PIL import Image, ImageTk

### GUI DEFINITIONS ###
win = Tk()
win.title("Setup Menu")
myFont = tkinter.font.Font(family = 'Helvetica', size = 18, \
    weight = "bold")
myFont2 = tkinter.font.Font(family = 'Helvetica', size = 42, \
    weight = "bold")
win.geometry("+200+40")
    # case of both size & position ("1200x700+100+100")

### Event Functions ###
def findMarker():
    # command to run findMarker.py
    # Example: python3 findMarker.py
    # It displays video of center camera, rectangle for search area
    #  for marker, and rectangle around marker if marker is found.
    # It displays a horizontal angle axis at the top, where 0°
    #  is aligned with left side of the marker.
    # It shows if the camera must be turned up or down
    #  to allow marker to be found.
    print ('\nfindMarker function')
    call(["python3", "/home/pi/md4/findMarker.py"])

def recordVideos():
    # command to run make_marker_video_1cam.py
    # Example: python3 make_marker_video_1cam.py
    # This program records a video with the angle marker.
    # Afterwards an image of the marker is taken from the footage.
    # The image can be used to search for the marker by other programs
    #  and thereby know the angle of the camera platform
    print ('\nrecordVideos function')
    call(["python3", "/home/pi/md4/recordVideos1.py"])

def calibration():
    # command to run calibration.py
    # Example: python3 calibration.py
    # This program is used to check views of two cameras
    #  to align them in a parallel direction.
    # A box with a marked paper is required.
    print ('\ncalibration function')
    call(["python3", "/home/pi/md4/calibration.py"])
    
def close():
    # RPi.GPIO.cleanup()
    win.destroy()

### WIDGETS ###
# Button, triggers the connected command when it is pressed
bW = 49 # bW
a = 'w' # alignment. The 9 positions are w=left, e=right, n=upper, s=lower,
    # ne=upper right, se=lower right, nw=upper left, sw=lower left, center=center
bH = 2 # buttonHeight
bG = 'bisque2'

buttonHeading = Message(win, text="* Angle marker needed.\n"
                        "** Box with a marked paper needed.",
    font=myFont, bg="yellow", aspect=700). grid(row=0,column=1)

findMarkerButton = Button(win,
text='Find marker - Try to find angle marker *',
font=myFont, command= findMarker, anchor=a, bg=bG, height=bH, width=bW)
findMarkerButton.grid(row=1,column=1)

recordVideosButton = Button(win,
text='Record videos from a camera for development use',
font=myFont, command= recordVideos, anchor=a, bg=bG, height=bH, width=bW)
recordVideosButton.grid(row=2,column=1)

calibrationButton = Button(win,
text='Calibration - Show left, center, & right views for parallel\nor nonparallel alignment of cameras **',
font=myFont, command= calibration, anchor=a, bg=bG, height=bH, width=bW)
calibrationButton.grid(row=3,column=1)

# Row 4 is space between buttons
win.grid_rowconfigure(4, minsize=10) # minsize is minimum height of the row.


# CREATE IMAGES
# Create the PIL image objectS
image1 = Image.open("/home/pi/md4/images/diagonallyQuarteredSquare.png")
photo1 = ImageTk.PhotoImage(image1)
img_label1 = tk.Label(image=photo1)
img_label1.image = photo1
img_label1.grid(row=1, column=0)

image2 = Image.open("/home/pi/md4/images/record.png")
photo2 = ImageTk.PhotoImage(image2)
img_label2 = tk.Label(image=photo2)
img_label2.image = photo2
img_label2.grid(row=2, column=0)

image3 = Image.open("/home/pi/md4/images/calibration.png")
photo3 = ImageTk.PhotoImage(image3)
img_label3 = tk.Label(image=photo3)
img_label3.image = photo3
img_label3.grid(row=3, column=0)

exitButton = Button(win,
text='Exit',
font=myFont, command=close, anchor='center', bg='red', height=bH, width=20)
exitButton.grid(columnspan=2, row=5, column=0)

win.protocol("WM_DELETE_WINDOW", close)
win.mainloop() # Loops forever
