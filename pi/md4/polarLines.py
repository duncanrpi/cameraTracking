# polar lines

# A walking path with polar coordinates is set. (r1,theta1), (r2,theta2)
# New path endpoints are made by moving inward, but staying on same line. (r1_new,theta1_new), (r2_new,theta2_new)
# This results in a shorter path going from start to end.

# If you want to begin with the start to end distance, then use negative values here:
#     threshPixels1,threshPixels2=-10,-10
# Then the new points will be outward. The subject will walk between the new points,
# but the start to end will be the inner points that you started with.

# The amount on each side inward or outward is in pixels, and it is converted to angles in degrees.
from math import sin, cos, degrees, radians, sqrt, pi
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

path = "home4m"

if path == "home4m":
    r1,r2,theta1,theta2 = 7.2111,6,16.845,-16.845
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -15,15,-20,20,7,7.5
elif path == "homeRad":
    r1,r2,theta1,theta2 = 2.4037,6,16.845,-16.845
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -15,15,-20,20,6,6.5
elif path == "home3m":
    r1,r2,theta1,theta2 = 5,4,18.4349,-18.4349
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -15,15,-20,20,5,5.5
elif path == "Mom":
    r1,r2,theta1,theta2 = 4.4721,4.4721,26.5651,-26.5651
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -25,25,-27,27,4,5
elif path == "UAB":
    r1,r2,theta1,theta2 = 5.14467,5.14467,22.877,-22.877
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -20,20,-24,24,5,5.5
elif path == "hosp":
    r1,r2,theta1,theta2 = 6.324555,6.324555,18.435,-18.435
    xticksmin,xticksmax,thetamin,thetamax,yticksmax,rmax= -20,20,-20,20,6,6.5

threshPixels1,threshPixels2=-10,-10
dpp=60.7/640; print ('dpp = ', dpp)
theta1_new=theta1-dpp*threshPixels1; print(theta1_new) # theta1 > theta1_new > theta2_new > theta2
theta2_new=theta2+dpp*threshPixels2; print(theta2_new)


# (r1,theta1), (r2,theta2) are 2 points defining a line
# (r,theta) is a 3rd point on the line. r is output
def depthOfPointOnLine(r1,r2,theta1,theta2,theta):
    rnum=r1*r2*sin(radians(theta1-theta2))
    rden=r1*sin(radians(theta1-theta))+r2*sin(radians(theta-theta2))
    r=rnum/rden
    return r

# (r1,theta1), (r2,theta2) are 2 points. Returns distance between them
def polar_dist_moved(r1,r2,theta1,theta2):
    return sqrt(r1**2 + r2**2 - 2*r1*r2*cos(radians(theta2-theta1)))


r1_new=depthOfPointOnLine(r1,r2,theta1,theta2,theta1_new); print(r1_new)
r2_new=depthOfPointOnLine(r1,r2,theta1,theta2,theta2_new); print(r2_new)


distance_new=polar_dist_moved(r1_new,r2_new,theta1_new,theta2_new); print(distance_new)


# (r1,theta1), (r2,theta2) are 2 points defining a line
# threshPixels1,threshPixels2 are the pixels inward from (r1,theta1), (r2,theta2), respectively.
# (r1_new,theta1_new), (r2_new,theta2_new) are 2 new inward points on same line that are defined.
# returns distance between 2 new points.
def innerDistance(r1,r2,theta1,theta2,threshPixels1,threshPixels2):    
    theta1_new=theta1-dpp*threshPixels1
    theta2_new=theta2+dpp*threshPixels2
    r1_new=depthOfPointOnLine(r1,r2,theta1,theta2,theta1_new)
    r2_new=depthOfPointOnLine(r1,r2,theta1,theta2,theta2_new)    
    return polar_dist_moved(r1_new,r2_new,theta1_new,theta2_new)


distance_new=innerDistance(r1,r2,theta1,theta2,threshPixels1,threshPixels2); 
print(distance_new)


print ('INPUT: path,r1,r2,theta1,theta2,threshPixels1,threshPixels2,dpp = ' \
       '{}, {:.4f}, {:.4f}, {:.4f}, {:.4f}, {}, {}, {:.4f}' \
      .format(path,r1,r2,theta1,theta2,threshPixels1,threshPixels2,dpp))
print ('OUTPUT: path,theta1_new,theta2_new,r1_new,r2_new,distance_new = {}, {:.4f}, {:.4f}, {:.4f}, {:.4f}, {:.4f}' \
      .format(path,theta1_new,theta2_new,r1_new,r2_new,distance_new))
total_distance = polar_dist_moved(r1,r2,theta1,theta2)
distance_new1 = polar_dist_moved(r1,r1_new,theta1,theta1_new)
distance_new2 = polar_dist_moved(r2_new,r2,theta2_new,theta2)
print ('PATH LENGTHS: path,total_distance,distance_new1,distance_new,distance_new2 = {}, {:.4f}, {:.4f}, {:.4f}, {:.4f}' \
      .format(path,total_distance,distance_new1,distance_new,distance_new2))


# POLAR PLOT
mpl.rcParams['font.size'] = 20
theta_line = [theta1,theta1_new,theta2_new,theta2] # degrees from high to low
theta_line_rad = [radians(x) for x in theta_line]
r_line = [r1,r1_new,r2_new,r2] # distances from origin corresponding to degrees from high to low
thetaA,rA=[0,radians(theta1)],[0,r1]
thetaB,rB=[0,radians(theta1_new)],[0,r1_new]
thetaC,rC=[0,radians(theta2_new)],[0,r2_new]
thetaD,rD=[0,radians(theta2)],[0,r2]

f1 = plt.figure(figsize=(50, 40)) # inches wide, inches high
ax1 = f1.add_subplot(111, polar=True)
ax1.plot(theta_line_rad, r_line, '.-', linewidth=3, markersize=15, color='purple', label='Walk Pattern')
ax1.plot(thetaA,rA, '.-', linewidth=3, markersize=15, color='red')
ax1.plot(thetaB,rB, '.-', linewidth=3, markersize=15, color='orange')
ax1.plot(thetaC,rC, '.-', linewidth=3, markersize=15, color='green')
ax1.plot(thetaD,rD, '.-', linewidth=3, markersize=15, color='blue')

# ax1.text('')
yticks = yticksmax+1
ax1.set_yticks(np.linspace(0,yticksmax,yticks)) # set radius tick labels with interval = 1.0
ax1.set_rmin(0) # minimum of radius range
ax1.set_rmax(rmax) # maximum of radius range

xticks=1+int((xticksmax-xticksmin)/5)
ax1.set_xticks(pi/180 * np.linspace(xticksmin,xticksmax,xticks)) # set angle tick labels with interval = 5 degrees

ax1.tick_params('x', pad=20.0) # x is angles. pad is space between tick labels & grid
ax1.set_thetamin(thetamin) # minimum of degree range
ax1.set_thetamax(thetamax) # maximum of degree range

ax1.set_xlabel('Angle Theta',rotation=90) # ,labelpad=5,ha='right',va='center'
ax1.xaxis.set_label_coords(1.10,0.56)
# ax1.text(-24.0,0.5,'Distance from Center Camera, r (m)',ha='center',va='top',transform=ax1.transData) # 336 deg = -24 deg
ax1.text(0.2,0.35,'Distance from Center Camera, r (m)',rotation=360+thetamin, \
         transform=ax1.transAxes,ha='center',va='top') # 336 deg = -24 deg
# ax1.text(0.36,0.26,'Distance from Center Camera, r (m)',rotation=336,transform=f1.transFigure) # 336 deg = -24 deg

# ax1.text(90.0,0.2,'Camera\nPlatform',transform=ax1.transData,ha='center',va='bottom')
ax1.text(0,0.6,'Camera\nPlatform',transform=ax1.transAxes)
# ax1.text(0.08 ,0.53,'Camera\nPlatform',transform=f1.transFigure)

# ax1.text(0.48,0.5,'Camera\nPlatform\nDirections',transform=ax1.transAxes,ha='center',va='center')

plt.legend(loc='upper left',bbox_to_anchor=(0.0,0.8),frameon=False)
plt.tight_layout(pad=0.1)
plt.show()

