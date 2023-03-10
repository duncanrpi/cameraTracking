A camera system has a Raspberry Pi computer, 3 cameras, and 2 DC motors. It performs the Short Physical Performance Battery (SPPB, Gait Speed, Standing Balance, 5 Times Sit Stand) and Timed Up and Go tests. There are graphical user interfaces and programs, all in Python.

Reproducing this depends on having a similar hardware set up. Use RPi 3B+, not RPi 4 because RPi 4 takes only 1 USB webcam. You need to know horizontal field of view (degrees) and resolution (width, height) in pixels for left and right cameras which connect with USB. In the center is a PiCamera. A needed camera calibration for left and right cameras is described in 

    pi/Desktop/CALIBRATION OF CAMERAS.txt.  

Some code would have to be adapted to particular hardwares. A few programs can run without hardware. Also, some software needs to be installed such as 1) Python3 programming language (version 3.7.3), 2) OpenCV (cv2) library of programming functions primarily for computer vision (version 3.4.6), 3) Imutils image processing functions (version 0.5.3), 4) VNC Server and Viewer in the RPi and cell phone, respectively, and 5) Rclone command line program.

Most important operations are accessible through graphical user interface (GUI) programs (.py) on the Desktop.
There are help files accessible with buttons in the GUIs.
Many programs are in md4 folder. There are some programs which are extra.

The folders and files are in the relative locations where they were used in a Raspberry Pi computer, but empty folders do not copy to GitHub. To be able to use this code, in a Raspberry Pi, you must create any folders and get any files that are missing on GitHub. Please see the file,  

    pi/Desktop/FOLDERS TO CREATE.txt. 
