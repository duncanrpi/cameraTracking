from math import sqrt

def getGrid(x1,y1,x2,y2):
    m21=(y2-y1)/(x2-x1)
    m43=(y4-y3)/(x4-x3)
    x=(y3-y1+m21*x1-m43*x3)/(m21-m43)
    y=y1+m21*(x-x1)
    r=round(sqrt(x**2+y**2),4)
    return r

# x1,y1=0,0
# x2,y2=2,-1
x1,y1=2.2,0
x2,y2=1.75,1.65
x1_ = [1.1,2.2,3.41,4.66,6.183,6.343,9.0]
y1_ = [0,0,0,0,0,1.816,0]
x2_ = [0.8,1.75,2.533,3.225,4.355,5.57,6.7]
y2_ = [1.65,1.65,2.30,3.00,3.00,3.00,3.00]


rrr_ = []

lenx = 7
leny = 7
"""
lengrid = lenx*leny
gridx_ = [] # x coordinates for input
gridy_ = [] # y coordinates for input
gridr_ = []
gridang_ = []
"""
for i in range(2,lenx+2): # x values
    x1,y1,x2,y2 = x1_[i-2],y1_[i-2],x2_[i-2],y2_[i-2]
    for j in range(-1,leny-1): # y values
        x3,y3,x4,y4=0,0,i,j
        r=getGrid(x1,y1,x2,y2)
        rrr_.append(r)
print ('rrr_ =', rrr_)        
        
"""
        gridx_.append(i)
        gridy_.append(j)
        gridr = round(sqrt(i**2+j**2),4)
        gridr_.append(gridr)
        gridang = round(atan2(j,i)-angHalf,5) # radians
        gridang_.append(gridang)
print ('gridx_ = ', gridx_)
print ('\ngridy_ = ', gridy_)
print ('\ngridr_ = ', gridr_)
print ('\ngridang_ = ', gridang_)
"""
