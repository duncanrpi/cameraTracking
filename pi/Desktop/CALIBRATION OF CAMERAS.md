CALIBRATION OF CAMERAS

For calibration of a particular set of cameras the following was done:
The problem is that using triangulation with the cameras to get the depth or distance may not be so accurate.
The following was necessary for this project:

    1. An area of interest is set up with rectangular (x, y)  grid points. The area must be wide enough to go outside of any possible incorrect detected distances. For example, a square area with 64 points, x = 1 to 8, y = 1 to 8. All in meters.
    2. An object (face or marker) is placed at a grid point and the camera system gets an angle (theta) and detected distance (ddep) for the (x, y).
    3. We want ddep = sqrt(x**2 + y**2). Suppose ddep is too high.
    4. Move object inward along the same angle to so that the new detected distance ddep is the original r = sqrt(x**2 + y**2), the grid point. 
    5. Get the new distance z of the object from the new position (xx, yy).
          z = sqrt(xx**2 + yy**2)
    6. When the camera detects depth ddep = r = sqrt(x**2 + y**2), the correct output depth is z.
    7. Add z to list Z.
    8. Repeat the process for all the grid points.

    9. There will be 3 lists, X, Y, and Z, for the 64 values of x, y, and r, respectively.
    10. interp2d is a Python function for 2D interpolation.
    11. Install scipy on Raspberry Pi
          sudo apt-get install python3-scipy
    12. There is an import statement, 
          from scipy.interpolate import interp2d
    13. Create the function using the 3 lists,
          depth_f = interp2d(X, Y, Z, 'cubic')
(Note that the word depth means distance from cameras.)
    14. To get a corrected depth dep from polar coordinates, convert a (theta, ddep) to (x, y) rectangular coordinates.
Convert degrees to radians if theta is in degrees.
          x = ddep*cos(radians(theta))
          y = ddep*sin(radians(theta))
    15. Use this formula,
          dep = depth_f(x, y)
where dep should be the correct depth from the cameras for a particular (x, y). 
Note that a 2D interpolation is done so that the correct depth dep for any point (x, y) within the grid area can be calculated.
