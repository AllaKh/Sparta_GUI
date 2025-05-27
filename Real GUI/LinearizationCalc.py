import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
from itertools import compress
from scipy import interpolate
from chirp_analysis_from_time_domain_LinCalib import chirp_analysis_from_time_domain_LinCalib as ch_an
from irad_stfftLinCalib import irad_stfftLinCalib as stft


def LinearizationCalc(OldLut,RawData,TargetFreq,ChirpType,n_inds_per_slice=0,UseScope=1):
    if UseScope:
        RawDataforAnalysis=RawData#
    else:
        RawDataforAnalysis=RawData[199:-349,:]# 
    

    n_inds_per_slice= n_inds_per_slice if n_inds_per_slice else np.floor(np.shape(RawDataforAnalysis)[2]/3)##number of bins
    
    if UseScope:
        NumOfChirpsInFile=5#
    else:
        NumOfChirpsInFile=20#
    
    NumOfFiles=np.floor(np.shape(RawData)[1]/NumOfChirpsInFile)#
    Chirptype=0# #1 down 0 up
    plot_flag=0#
    max_bins_mat=[]#
    max_freqs_mat=[]#
    max_vals_mat=[]#
    widths_mat=[]#
    # figure(99)# 
    # hold off#
    for i in np.arange(0,np.shape(RawData)[1],NumOfChirpsInFile):
        [max_bins,max_freqs,max_vals,widths]=stft(RawDataforAnalysis[:,i+ np.arange( NumOfChirpsInFile)],TargetFreq,plot_flag,UseScope,n_inds_per_slice)#
        max_bins_mat.append(max_bins)
        max_freqs_mat.append(max_freqs)
        max_vals_mat.append(max_vals)
        widths_mat.append(widths)
        plot_flag
    max_bins_mat=np.asarray(max_bins_mat)
    max_freqs_mat=np.asarray(max_freqs_mat)
    max_vals_mat=np.asarray(max_vals_mat)
    widths_mat=np.asarray(widths_mat)
    add_prep_vec=2      
    NewLut=ch_an(OldLut,TargetFreq,max_freqs_mat,ChirpType,UseScope,0,0,add_prep_vec)                                                                                                                                                

    return NewLut

if __name__ == "__main__":
    str='C:/lin_data/flat_by_cums_folder/piezo_lut_0_10000.txt'
    OldLut=np.loadtxt(str)
    n_samp=4000
    n_vecs=20
    t_tot=1.55e-3
    dt=t_tot/n_samp
    t_vec=np.arange(n_samp)*dt
    fi=150e3
    ff=180e3
    TargetFreq=(ff+fi)/2

    slope=(ff-fi)/(n_samp*dt)
    f_err=1*slope/(n_samp*dt)

    f_in_vec=fi+ slope* t_vec/2+f_err*((t_vec-t_vec[-1]/2)**2)/3
    sig_mat=np.zeros((n_samp,n_vecs))
    noise_size=0.0
    n_inds_per_slice=800
    speckle_amplitude=10
    for ind in range(n_vecs):
        sig_mat[:,ind]=np.sin(2*np.pi*f_in_vec*t_vec)*np.random.randn(1)*speckle_amplitude +np.random.rand(np.shape(t_vec)[0])*noise_size
    fig_hand = plt.figure()
    axx = fig_hand.add_subplot(111,title='sampled data')
    sc1 = axx.plot(t_vec,sig_mat,'-')
    plt.grid(True)    # end
    plt.show()
    newLUT=LinearizationCalc(OldLut,sig_mat,TargetFreq,ChirpType=0,n_inds_per_slice=n_inds_per_slice,UseScope=1)
    new_str=str[:-4]+'a'+str[-4:]
    # max_bins,max_freqs,max_vals,widths=irad_stfftLinCalib(sig_mat,f_target,0,1,n_inds_per_slice)
    # fig_hand = plt.figure()
    # axx = fig_hand.add_subplot(111,title='max_freqs')
    # sc1 = axx.plot(np.arange(np.size(max_freqs)),max_freqs,'-')
    # plt.grid(True)    # end
    # plt.show()
    # max_freqs_mat=np.concatenate((max_freqs[None,:],max_freqs[None,:]),axis=0)
    # old_chirp_vec=np.arange(1200)
    # target_freq=50e3
    
    # new_chirp_vec=ch_an(old_chirp_vec,f_target,max_freqs_mat,0,1,multipulse=0, DebugPlot=1, add_prep_vec=1)
