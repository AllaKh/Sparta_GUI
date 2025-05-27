import sys,time
import numpy as np

it=[0,0.04,0.09,0.13,0.18,0.22,0.27,0.31,0.35,0.39,0.43,0.47,0.51,0.54,0.58,0.61,0.64,0.67,0.70,0.72,0.75,0.77,0.79,0.81,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.00]


for i in range(0,len(it)-1):
    aa= np.linspace(it[i], it[i+1], num=37)
    for a in aa:
        print(a)

#for i in range(1600,7273):
#    print(1)