import sys,time


import numpy as np
from scipy import interpolate

import re,sys
regex = r"(\S*)\s*(0x[0-9a-fA-F]+)\s*(0x[0-9a-fA-F]+)[\s\n$]"


def readregfile(name):
    f = open(name,"r")
    list ={}
    for line in f:
        if line[0] == '/' :
            #print("Skip",line)
            continue
        match = re.search(regex, line)
        if match == None:
            continue
        
        list[match.group(1)] = int(match.group(3),16)
        #print (match.group(1),match.group(2),match.group(1))
    f.close()

    

    #sensor_prot_len = list["SEN_PROTECT_LEN_OFFSET"]
    return list

def extend_vec(v, tm):
    
    t = np.linspace(0, 1,len(v) )
    f = interpolate.interp1d(t, v)

    t2=np.linspace(0, 1,tm )
    tt=f(t2)
    return tt

it=[0,0.04,0.09,0.13,0.18,0.22,0.27,0.31,0.35,0.39,0.43,0.47,0.51,0.54,0.58,0.61,0.64,0.67,0.70,0.72,0.75,0.77,0.79,0.81,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.00]



def generate_piezzo_lut(name, sp_len,sp_height,lenx,starty,height,vec):
    f = open(name, 'w')
    print("0",file=f)
    print(str(sp_len),file=f)
    
    if sp_len != 0:
        t=np.arange(0,sp_len)
        y=starty-sp_height + t*sp_height/(sp_len-1)
       
        for v in y:
            vv = int(round(v))
            print(vv,file=f)
    
    tt=np.arange(0,lenx)

  
    
    if vec is not None:
       y=starty + height*vec
    else:    
       y=starty + tt*height/(lenx-1)
    
    for v in y[1:]:
        print(int(round(v)),file=f)
    
    f.close()

    





def GeneratePiezoFiles(fft_in_len):    
    clock = 200/256
    samplingfr=48


    if len(sys.argv) != 2:
        print("Usage "+ sys.argv[0] + " register-file.txt")

    regs= readregfile(sys.argv[1])
    
    laser_wakeup_length =     regs['TD4_LEN']
    print("laser wakeup  " + str(laser_wakeup_length//samplingfr))
    
    
    ic_wakeup_length =     regs['TD5_LEN']
    print("ic wakeup  " + str(ic_wakeup_length//samplingfr))


    startx = int ( 0 * clock)
    
    #fft_in_len = regs['FFT_IN_LEN_OFFSET']
    print("fft in  " + str(fft_in_len))

    lenx = int((fft_in_len + ic_wakeup_length + laser_wakeup_length)*clock/samplingfr)
    print("pulse lenght in LUT samples  " + str(lenx))
    
    #Why 152
    # 51 laser stabilization
    # 101 SP
    sp_len    = 0#int( (ic_wakeup_length+152)*clock)  TODO


    sp_height = 150


    #Generate UP
    starty = 638
    height = 1147
    
    generate_piezzo_lut('piezo_lut_0_{:x}.txt'.format(fft_in_len),sp_len,sp_height,lenx,starty,height,None)
    
    
   
    #Generate FLAT
    starty = 1993
    height= -929

    generate_piezzo_lut('piezo_lut_1_{:x}.txt'.format(fft_in_len),sp_len,sp_height,lenx,starty,height,None)

    #Generate DOWN
    
    starty = 2412
    height = -2184

    down_coefs = extend_vec(it,lenx)
    generate_piezzo_lut('piezo_lut_2_{:x}.txt'.format(fft_in_len),sp_len,sp_height,lenx,starty,height,down_coefs)


if __name__ == "__main__":

        GeneratePiezoFiles(0x10000)
        GeneratePiezoFiles(0x8000)
        GeneratePiezoFiles(0x4000)