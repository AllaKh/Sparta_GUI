import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
from itertools import compress


def  SampleSigByClock_fun (V_dat,clk_dat,piezo_dat,time_dat,drop2data_offset,good_inds,time_inc,plot_flag):
    # [sampled_timeVector, sampled_V_dat,good_inds] = SampleSigByClock(file_path,wave_ind,drop2data_offset,good_times)
    # this function extracts a single time domain 1-bit shuttle data with its clock (with or without analog data) and
    # samples the digital data at clock drops with an offset determined by the user
    # [desc] = importAgilentBinDesc(file_path)
    # save_strs=[desc.waveformString]
    # save_strs=save_strs(1:16:end)
    n_samples=np.minimum(good_inds[-1]-good_inds[0]+1,np.size(V_dat)) #how many different samples of the 1st channel
    timeVector_V=np.arange(n_samples)*time_inc
    # channel_inds=str2num(unique(save_strs)')
    # time_tags=[desc.timeTag]
    # cur_wave_inds=find(time_tags==time_tags(wave_ind)&save_strs~=save_strs(wave_ind))
    ## get signal from file
    # n_samples=length(desc)

    ## plot signal and clock for reference
    if plot_flag:
        fig_hand = plt.figure()
        axx = fig_hand.add_subplot(111,title='Raw data')

        plt.plot(time_dat,V_dat)
        plt.plot(time_dat,clk_dat)
        plt.grid(True)
        plt.show()
    #     if length(cur_wave_inds)>1
    #         plot(timeVector_N(timeVector_inds),nlg_dat(timeVector_inds))
    #     end

    ## binarize V_dat
    sampled_V_dat_raw=V_dat>np.mean([np.amax(V_dat), np.amin(V_dat)])

    ## get clock drops
    clk_amplitude=np.amax(clk_dat).astype(float) - np.amin(clk_dat).astype(float)
    # clk_drop_inds=np.append(  (np.diff(clk_dat)>(clk_amplitude*.3))[:,np.newaxis], [[0]],axis=0)# may need to change from row to column
    clk_drop_inds=np.append(  (np.diff(clk_dat)>(clk_amplitude*.3)), [0],axis=0)# may need to change from row to column
    clk_drop_inds=np.logical_and( clk_drop_inds,np.logical_not( np.roll(clk_drop_inds,1) ) )## remove 2 consecutive ones
    test_mat=np.array((np.logical_not(clk_drop_inds), np.roll(clk_drop_inds,1), np.roll(clk_drop_inds,-1) ))# search for [1 0 1]
    close_peak_inds=np.logical_and.reduce(test_mat)  #turn [101] into [010] while keeping [010]
    for ind in list(compress(range(len(close_peak_inds)), close_peak_inds)):
        if not(ind==0) and not(ind== len(close_peak_inds)-1 ):
            clk_drop_inds[np.arange(-1,2) +ind]=[[0] [1] [0]]
    
    clk_drop_inds=np.roll(clk_drop_inds,drop2data_offset)
    timeVector_inds=np.zeros(np.shape(clk_drop_inds))
    timeVector_inds[good_inds[0]:np.minimum(good_inds[-1],len(timeVector_inds))]=1
    good_inds=np.logical_and(clk_drop_inds, timeVector_inds)

    # sampled_timeVector=timeVector_V(good_inds )
    sampled_V_dat=sampled_V_dat_raw[good_inds]
    #sampled_V_dat(sampled_V_dat==0)=[]
    if plot_flag :
        fig_hand = plt.figure()
        axx = fig_hand.add_subplot(111,title='sampled data')
        sc1, = axx.plot(np.arange(np.size(sampled_V_dat)),sampled_V_dat,'-')
        plt.grid(True)    # end
        plt.show()
    fs=1/np.mean(np.diff(time_dat[good_inds]))
    
    return sampled_V_dat,time_dat[good_inds],fs

if __name__ == "__main__":
    sim_size=100
    V_dat=np.random.rand(sim_size,1)>0.5
    piezo_dat=0
    clk_dat=np.sin(np.arange(sim_size))>0
    time_inc=3.5e-6
    
    time_dat=np.arange(sim_size)*time_inc
    drop2data_offset=2
    good_inds=np.arange(97)+1 ## numb of inxs that within the trigger

    sampled_V_dat,good_inds,fs=SampleSigByClock_fun (V_dat,clk_dat,piezo_dat,time_dat,drop2data_offset,good_inds,time_inc,plot_flag=True)
    print('after code')