# plotGrid.py
# imports
import numpy as np
from math import sin,cos,pi,tan,atan2,radians,degrees,sqrt,floor,ceil,asin
from numpy import median
from scipy.interpolate import interp2d
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
angHalf = atan2(4.0,6.0)/2 # 0.2940013018, radians. In degrees, angHalf = 16.84503376 
lenx = 8
leny = 8
lengrid = lenx*leny
gridx_ = [] # x input coordinates
gridy_ = [] # y input coordinates
gridr_ = [] # radius input coordinates
gridang_ = [] # angle (0 center) input coordinates
for i in range(1,lenx+1):
    for j in range(-1,leny-1):
        gridx_.append(i)
        gridy_.append(j)
        gridr = round(sqrt(i**2+j**2),4)
        gridr_.append(gridr)
        gridang = round(atan2(j,i)-angHalf,6) # radians
        gridang_.append(gridang)

print ('x input coordinates, len(gridx_) = ', len(gridx_))
print ('gridx_ = ', gridx_)
print ('\ny input coordinates, len(gridy_) = ', len(gridy_))
print ('gridy_ = ', gridy_)
"""
print ('\nradius input coordinates, len(gridr_) = ', len(gridr_))
print ('gridr_[0:8] = ', gridr_[0:8])
print ('gridr_[8:16] = ', gridr_[8:16])
print ('gridr_[16:24] = ', gridr_[16:24])
print ('gridr_[24:32] = ', gridr_[24:32])
print ('gridr_[32:40] = ', gridr_[32:40])
print ('gridr_[40:48] = ', gridr_[40:48])
print ('gridr_[48:56] = ', gridr_[48:56])
print ('gridr_[56:64] = ', gridr_[56:64])
print ('\nangle (0 center) input coordinates, len(gridang_) = ', len(gridang_))
print ('gridang_[0:8] = ', gridang_[0:8])
print ('gridang_[8:16] = ', gridang_[8:16])
print ('gridang_[16:24] = ', gridang_[16:24])
print ('gridang_[24:32] = ', gridang_[24:32])
print ('gridang_[32:40] = ', gridang_[32:40])
print ('gridang_[40:48] = ', gridang_[40:48])
print ('gridang_[48:56] = ', gridang_[48:56])
print ('gridang_[56:64] = ', gridang_[56:64])
"""
gridout_ = [1.9013, 1.1, 1.3163, 1.8037, 2.2508, 2.6257, 2.938, 3.2, \
2.848, 2.2, 2.1645, 2.4446, 2.8147, 3.1831, 3.5222, 3.8264, \
4.1178, 3.41, 3.1891, 3.2677, 3.4913, 3.7678, 4.0525, 4.326, \
5.4558, 4.66, 4.2904, 4.2045, 4.287, 4.4579, 4.6684, 4.8914, \
7.1805, 6.183, 5.6205, 5.3543, 5.2802, 5.3232, 5.4334, 5.5789, \
8.5644, 7.5286, 6.8834, 6.5175, 6.3457, 6.3043, 6.3469, 6.4415, \
10.2096, 9.0, 8.1939, 7.6782, 7.3701, 7.208, 7.1465, 7.1531, \
11.8812, 10.5, 9.5384, 8.8805, 8.4435, 8.1665, 8.0046, 7.9245]
print ('\nradius output coordinates, len(gridout_) = ', len(gridout_))
print ('gridout_ = ', gridout_)

rrr_f = interp2d(gridx_, gridy_, gridout_, 'cubic')

# POLAR PLOTS OF PATHS
mpl.rcParams['font.size'] = 60
mpl.rcParams['axes.linewidth'] = 5.0
mpl.rcParams['grid.linewidth'] = 5.0
f2 = plt.figure(figsize=(50, 40))
ax2 = f2.add_subplot(111, polar=True)
LW = 5
MS = 30
GRC = 'blue' # grid r color
GOC = 'red' # grid out color
legend_entries = ['grid r', 'grid out']

ax2.plot(gridang_[0:8], gridr_[0:8], '.-', linewidth=LW, markersize=MS, color=GRC, label='grid input')
ax2.plot(gridang_[8:16], gridr_[8:16], '.-', linewidth=LW, markersize=MS, color=GRC)
ax2.plot(gridang_[16:24], gridr_[16:24], '.-', linewidth=LW, markersize=MS, color=GRC)
ax2.plot(gridang_[24:32], gridr_[24:32], '.-', linewidth=LW, markersize=MS, color=GRC)
ax2.plot(gridang_[32:40], gridr_[32:40], '.-', linewidth=LW, markersize=MS, color=GRC)
ax2.plot(gridang_[40:48], gridr_[40:48], '.-', linewidth=LW, markersize=MS, color=GRC)
ax2.plot(gridang_[48:56], gridr_[48:56], '.-', linewidth=LW, markersize=MS, color=GRC)
ax2.plot(gridang_[56:64], gridr_[56:64], '.-', linewidth=LW, markersize=MS, color=GRC)

ax2.plot(gridang_[0:8], gridout_[0:8], '.-', linewidth=LW, markersize=MS, color=GOC, label='grid output')
ax2.plot(gridang_[8:16], gridout_[8:16], '.-', linewidth=LW, markersize=MS, color=GOC)
ax2.plot(gridang_[16:24], gridout_[16:24], '.-', linewidth=LW, markersize=MS, color=GOC)
ax2.plot(gridang_[24:32], gridout_[24:32], '.-', linewidth=LW, markersize=MS, color=GOC)
ax2.plot(gridang_[32:40], gridout_[32:40], '.-', linewidth=LW, markersize=MS, color=GOC)
ax2.plot(gridang_[40:48], gridout_[40:48], '.-', linewidth=LW, markersize=MS, color=GOC)
ax2.plot(gridang_[48:56], gridout_[48:56], '.-', linewidth=LW, markersize=MS, color=GOC)
ax2.plot(gridang_[56:64], gridout_[56:64], '.-', linewidth=LW, markersize=MS, color=GOC)

yticksmax = 11
yticks = yticksmax+1
rmax = yticks
ax2.set_yticks(np.linspace(0,yticksmax,yticks))
ax2.set_rmax(rmax)    
ax2.set_rmin(0)

xticksmax = 65
xticksmin = -xticksmax
xticks = int((xticksmax-xticksmin)/5+1)
thetamin = xticksmin-2
thetamax = xticksmax+2
ax2.set_xticks(pi/180 * np.linspace(xticksmin,xticksmax,xticks))
ax2.set_thetamin(thetamin)
ax2.set_thetamax(thetamax)

ax2.tick_params('x', pad=60.0) # x is angles. pad is space between tick labels & grid
ax2.tick_params('y', pad=25.0) # y is radii. pad is space between tick labels & grid

ax2.set_xlabel('Angle Theta',rotation=90)
ax2.xaxis.set_label_coords(0.84,0.55)
ax2.text(0.27,0.42,'Distance from Center Camera, r (m)',rotation=360+thetamin, \
         transform=ax2.transAxes,ha='center',va='top')
ax2.text(0.10,0.48,'Camera\nPlatform',transform=ax2.transAxes)
ax2.set_axisbelow(True)
plt.legend(loc='lower left',bbox_to_anchor=(0.1,0.75),frameon=False)

runStr2 = '/home/pi/Desktop/' + stamp + ' ' + 'grid plot.png'
plt.tight_layout(pad=0.0)
plt.savefig(runStr2, bbox_inches='tight')
plt.close()

theta_in = 20 # degrees
r_in = 5
xxx = r_in*cos(radians(theta_in)+angHalf) # radians(theta_in) & angHalf=0.2940013 are in radians
yyy = r_in*sin(radians(theta_in)+angHalf) # angHalf=0.2940013 is a shift so that angle0 = 0

r_out = rrr_f(xxx, yyy)[0]
print ('xxx, yyy, r_out = ', xxx, yyy, r_out)
# Example: theta_in=20, r_in=5, xxx=4.001301493184352,
# yyy=2.9982638910944237, r_out=4.287981688243897
