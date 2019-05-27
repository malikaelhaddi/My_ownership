# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:16:58 2018

@author: kumar.shivam
"""

#2.01205352631 0.087642779428 -0.0273696173064



from scipy.optimize import fsolve
import numpy as np
import xlrd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt




beta1 =[]
beta2 =[]
beta3 =[]


xl_workbook = xlrd.open_workbook("/Desktop/25-05-2018/dataset.xlsx")
sheet = xl_workbook.sheet_by_index(1)


for i in range(1,sheet.nrows-2):
#    print(sheet.cell_value(i,1))   
#    print(sheet.cell_value(i,2))    
#    print(sheet.cell_value(i,3))
    def equations(p):
        a, b, c = p
        
        n = (sheet.cell_value(i,1)) 
        dT = (sheet.cell_value(i,2))
        wmax = (sheet.cell_value(i,3))
        wmax1 = (sheet.cell_value(i+1,3))
        n1 = (sheet.cell_value(i+1,1)) 
        dT1 = (sheet.cell_value(i+1,2))
        wmax2 = (sheet.cell_value(i+2,3))
        n2 = (sheet.cell_value(i+2,1))
        dT2 = (sheet.cell_value(i+2,2))
    
    #    return(a**2+b**3+c**2-90,a**2+b**3+c**2-12,a**2+b**3+c**2-3)
    #    try:
        return((1-(1-(1/(1+np.exp((a+b*(wmax)))))**(n**c)) - dT),(1-(1-(1/(1+np.exp((a+b*(wmax1)))))**(n1**c)) - dT1), (1-(1-(1/(1+np.exp((a+b*(wmax2)))))**(n2**c)) - dT2))
    #    except:
    #        return(float('inf'))
    
    
    a,b,c = fsolve(equations, (0.0001,0.000000000001, 0.000000001), xtol=1e-06, maxfev=100000)
    
    print(a,b,c)
    beta1.append(a)
    beta2.append(b)
    beta3.append(c)
    
    
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(beta1, beta2, beta3)


ax.set_zlim3d(-4, 2)                    # viewrange for z-axis should be [-4,4] 
ax.set_ylim3d(0, 40)                    # viewrange for y-axis should be [-2,2] 
ax.set_xlim3d(-2000, 0) 

ax.set_xlabel('beta1')
ax.set_ylabel('beta2')
ax.set_zlabel('beta3')


plt.show()







    

