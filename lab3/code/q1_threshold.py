# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:18:51 2018

@author: William James Ngana
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

## gives you the curve of best fit for a set of data x,y
def LOBF(x,y,fit):
    z = np.polyfit(x,y,fit)
    f = np.poly1d(z)
    new_x = np.linspace(0,max(x)+1,50)
    new_y = f(new_x)
    return new_x, new_y

## Equation 2 in the lab manual
def voltage_thers(VBS):
    return 0.867 + 2*(np.sqrt(4 - VBS) - np.sqrt(4))

## The Data

#VBB = 0
IDS0 = [1.0108,2.0041,3.0031,4.0049,5.0176]
SQRT_IDS0 = np.sqrt(IDS0)
VGS0 = [2.86,3.60,4.22,4.76,5.27]
LBF0x,LBF0y = LOBF(SQRT_IDS0,VGS0,1)
#VBB = -2
IDS2 = [1.0062,2.0049,3.0004,4.0233,5.0190]
SQRT_IDS2 = np.sqrt(IDS2)
VGS2 = [4.48,5.18,5.75,6.27,6.75]
LBF2x,LBF2y = LOBF(SQRT_IDS2,VGS2,1)
#VBB = -6
IDS6 = [1.0014,2.0131,3.0064,4.0219,5.0171]
SQRT_IDS6 = np.sqrt(IDS6)
VGS6 = [6.64,7.31,7.86,8.36,8.81]
LBF6x, LBF6y = LOBF(SQRT_IDS6,VGS6,1)
#VBB = -10
IDS10 = [1.0019,2.0046,3.0200,4.0268,5.0133]
SQRT_IDS10 = np.sqrt(IDS10)
VGS10 = [8.28,8.93,9.48,9.96,10.41]
LBF10x,LBF10y = LOBF(SQRT_IDS10,VGS10,1)

#Plotting 
plt.scatter(SQRT_IDS0,VGS0, color = 'red')
plt.scatter(SQRT_IDS2,VGS2, color = 'blue')
plt.scatter(SQRT_IDS6,VGS6, color = 'green')
plt.scatter(SQRT_IDS10,VGS10, color = 'orange')
##Line of best fit and extrapolation
plt.plot(LBF0x,LBF0y,color = 'black' )
plt.plot(LBF2x,LBF2y,color = 'black' )
plt.plot(LBF6x,LBF6y,color = 'black' )
plt.plot(LBF10x,LBF10y,color = 'black' )
#plot mechanics 
plt.xlabel('SQRT(IDS)')
plt.ylabel('V_GS' )
plt.title('Plot of the Squareroot of IDS vs V_GS')
red_patch = mpatches.Patch(color='red', label='Data points for VBB = 0')
blue_patch = mpatches.Patch(color='blue', label='Data points for VBB = -2')
green_patch = mpatches.Patch(color='green', label='Data points for VBB = -6')
orange_patch = mpatches.Patch(color='orange', label='Data points for VBB = -10')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,handles=[red_patch,blue_patch,green_patch,orange_patch])
plt.show()
## New plot
VB = [0,-2,-6,-10]
VT = [LBF0y[0],LBF2y[0],LBF6y[0],LBF10y[0]]
Curvex,Curvey = LOBF(VT,VB,2)
plt.scatter(VT,VB, color = 'blue')
plt.plot(Curvex,Curvey, color = 'blue')
#plot mechanics 
plt.xlabel('VBB (V)')
plt.ylabel('VT (V)' )
plt.title('Plot of the Squareroot of IDS vs V_GS')
plt.show()
## Equation
new_vt = [voltage_thers(x) for x in VB]
plt.plot(new_vt,VB, color = 'blue')
#plot mechanics 
plt.xlabel('VBB (V)')
plt.ylabel('VT (V)' )
plt.title('Plot of the Squareroot of IDS vs V_GS using Equaion 2')
