import os,sys  #needed to check the working directory
import numpy as np
import matplotlib.pyplot as plt
import visa
import SampleSigByClock as ssclk
import time

sys.path.append(r'C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder')
import SetupandSampleFromScope as set_samp
import LinearizationCalc as lin_cal


# NumOfChirps=10
# ScopeAdress = "TCPIP0::10.99.0.18::inst0::INSTR"
# TScale="0.000160" #  sec
# TOffset="0.000820" #sec
# Chan1Offset="1.75" #v
# TrigCh1="2.0" #V
# Chan1Scale="1.0" #V
# Chan4Offset="0.1" #v
# TrigCh4="2.0" #V
# Chan4Scale="0.05" #V
# data1,data4,TimeScope=set_samp.SetupandSampleFromScope(NumOfChirps,ScopeAdress,TScale,TOffset,Chan1Offset,TrigCh1,Chan1Scale,Chan4Offset,TrigCh4,Chan4Scale)
def lin_top():
    SampledData,time_dat,fs = set_samp.main_grab()
#     str='C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/piezo_lut_0_10000.txt'
    str='C:/lin_data/piezo_lut_0_10000Linear_a.txt'
#     SampledData=np.loadtxt("this_dat.txt")
    OldLut=np.loadtxt(str)
    target_freq=67e3
    n_inds_per_slice_vec=np.round(np.array( [280, 300, 320, 400])/2000*np.shape(SampledData)[0]).astype(int)
#    n_inds_per_slice_vec=np.round(np.array( [300])/2000*np.shape(SampledData)[0]).astype(int)
    for cur_n_inds_per_slice in n_inds_per_slice_vec:
        newLUT=lin_cal.LinearizationCalc(OldLut,SampledData,target_freq,ChirpType=0,n_inds_per_slice=cur_n_inds_per_slice,UseScope=1)
        plt.plot(newLUT)
        plt.show()
        np.savetxt(str[:-4]+"_a"+str[-4:], newLUT,fmt='%d')
        print(str[:-4]+"_a"+str[-4:])
if __name__ == "__main__":
    lin_top()
       