import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
from itertools import compress
from scipy import interpolate
import warnings
# import irad_stfftLinCalib as stft

def magic(n):
  n = int(n)
  if n < 3:
    raise ValueError("Size must be at least 3")
  if n % 2 == 1:
    p = np.arange(1, n+1)
    return n*np.mod(p[:, None] + p - (n+3)//2, n) + np.mod(p[:, None] + 2*p-2, n) + 1
  elif n % 4 == 0:
    J = np.mod(np.arange(1, n+1), 4) // 2
    K = J[:, None] == J
    M = np.arange(1, n*n+1, n)[:, None] + np.arange(n)
    M[K] = n*n + 1 - M[K]
  else:
    p = n//2
    M = magic(p)
    M = np.block([[M, M+2*p*p], [M+3*p*p, M+p*p]])
    i = np.arange(p)
    k = (n-2)//4
    j = np.concatenate((np.arange(k), np.arange(n-k+1, n)))
    M[np.ix_(np.concatenate((i, i+p)), j)] = M[np.ix_(np.concatenate((i+p, i)), j)]
    M[np.ix_([k, k+p], [0, k])] = M[np.ix_([k+p, k], [0, k])]
  return M 

def get_data_from_old_LUT(old_chirp_vec,add_prep_vec):
  if add_prep_vec>1:
    active_chirp_len=np.round(len(old_chirp_vec)/3).astype(int)
    old_chirp_vec_cut=np.asarray(old_chirp_vec[-active_chirp_len:])
    chirp_vec_consts=np.asarray([0,0])
  else:
    chirp_vec_consts=np.asarray(old_chirp_vec[:2])
    old_chirp_vec_cut=np.asarray(old_chirp_vec[2:])
  Vend=old_chirp_vec_cut[-1]
  Vstart=old_chirp_vec_cut[0]
  return old_chirp_vec_cut,chirp_vec_consts,Vstart,Vend

def create_new_LUT(newChirp_perChirpInd,chirp_vec_consts,Vstart,Vend,add_prep_vec=1):
  if add_prep_vec>0:
    #   Vend=old_chirp_vec_cut[-1]
    # Vstart=old_chirp_vec_cut[0]
    prep_vec=np.concatenate(( np.linspace( Vend,Vstart,len(newChirp_perChirpInd) ) , np.ones_like(newChirp_perChirpInd) * Vstart  )) 
    new_chirp_vec=np.concatenate((prep_vec ,newChirp_perChirpInd))+ chirp_vec_consts[0]
  else:
    new_chirp_vec=np.concatenate((chirp_vec_consts ,newChirp_perChirpInd))#
    new_chirp_vec=np.round(new_chirp_vec)#
  return new_chirp_vec

def get_linearization_default(str=''):
  if len(str)<4 :
    str='C:/lin_data/piezo_lut_0_10000Linear.txt'      
  old_chirp_vec=np.loadtxt(str)
  if len(old_chirp_vec)<2000:
    add_prep_vec=1
  else:
    add_prep_vec=0
  old_chirp_vec_cut,chirp_vec_consts,Vstart,Vend=get_data_from_old_LUT(old_chirp_vec,add_prep_vec)
  new_chirp_vec=create_new_LUT(old_chirp_vec_cut,chirp_vec_consts,Vstart,Vend,add_prep_vec)
  return new_chirp_vec



def chirp_analysis_from_time_domain_LinCalib(old_chirp_vec,target_freq,max_freqs_mat,chirptype,LoadFromScope,multipulse=0, DebugPlot=0, add_prep_vec=1):
  # old_chirp_vec : 1d vector
  # target_freq : integer
  # max_freqs_mat : 2D np-array a row is a single chirp, a column is the same slice 
  # chirptype : np.integer{1 for down, 0 for up}
  # LoadFromScope : np.integer{1 for scope, 0 for NI}
  # multipulse : integer number of sub pulses, not implemented yet (0 for no subpulses, 2 and up represents the number of subpulses)
  # add_prep_vec : comply with new mode for "python linearization while running", 
  #                  0 recive old vector and produce old vector
  #                  1 receive old and produce new
  #                  2 receive new and produce new
  
  old_chirp_vec_cut,chirp_vec_consts,Vstart,Vend = get_data_from_old_LUT(old_chirp_vec,add_prep_vec)    




  # if LoadFromScope:
  #   useful_slices=np.arange(2,np.shape(max_freqs_mat)[1]).astype(int)
  #   #useful_slices=1:size(max_freqs_mat,2)
  # else:
  #   useful_slices=np.arange(np.round(np.shape(max_freqs_mat)[1]*0.1),np.round(np.shape(max_freqs_mat)[1]*1)).astype(int)### values 0.1 and 1 may be changed to remove some slices
      
  
  # useful_slices= useful_slices[np.logical_not(useful_slices==0)] # row appears redunant ibn matlab code
  # overide_inds=find(~ismember(1:size(max_freqs_mat,2),useful_slices))

  SlicetoUse=np.floor(np.shape(max_freqs_mat)[1]/2).astype(int)
  if DebugPlot:
    # hold all#
    plt.plot(max_freqs_mat[:,SlicetoUse],'*')
    # title('Slice used *')
    plt.show()
  
  ##########################
  good_files= np.logical_and( max_freqs_mat[:,SlicetoUse]>target_freq*.8 , max_freqs_mat[:,SlicetoUse]<target_freq*1.2) 
  useful_slices= np.logical_and( np.mean(max_freqs_mat,axis=0)>target_freq*.5 , np.mean(max_freqs_mat,axis=0)<target_freq*2) 
  # overide_inds=np.where(np.in1d(np.arange(np.shape(max_freqs_mat)[1]),useful_slices,invert=True))
  overide_inds=np.where(np.logical_not(useful_slices))
  print("overide inds",overide_inds)
  #good_files= max_freqs_mat>target_freq*.8 & max_freqs_mat<target_freq*1.2 #

  max_freqs_mat_good=max_freqs_mat[good_files,:]#
  # figure;plot(std(stfft_good_bins)./mean(stfft_good_bins))
  # hold all
  DebugPlot= np.sum(good_files)< np.size(good_files)/2
  if DebugPlot:
    print("less than half the files grabbed are good")
  DebugPlot= 0
  if DebugPlot:
    # figure
    plt.plot(np.mean(max_freqs_mat_good,axis=0))
    plt.title('center bins')
    # hold all
    plt.plot(np.mean(max_freqs_mat_good,axis=0)+np.std(max_freqs_mat_good,axis=0))
    plt.plot(np.mean(max_freqs_mat_good,axis=0)-np.std(max_freqs_mat_good,axis=0))
    plt.show()
  
  norm_old_chirp=(old_chirp_vec_cut-np.amin(old_chirp_vec_cut))/(np.amax(old_chirp_vec_cut)-np.amin(old_chirp_vec_cut))#
  max_freqs_mat_good_useful=max_freqs_mat_good[:,useful_slices]#
  #max_freqs_mat_good_useful=max_freqs_mat_good(useful_slices)#
  target_val_mean=1/np.mean(1/max_freqs_mat_good_useful [np.nonzero(max_freqs_mat_good_useful)])## to preserve the central frequency of the entire pulse normalize corrections to the mean correction
  print('target val mean is',target_val_mean)
  masked_max_freqs_mat_good_useful=np.ma.array(max_freqs_mat_good_useful, mask=max_freqs_mat_good_useful<0.5*target_val_mean)# mask all irrelevant elements of max_freqs_mat_good_useful 
  dfdtCor=np.ones(np.shape(max_freqs_mat_good)[1])*0.9999# create default correction vector, don't waste voltage on correction in non useful slices
  dfdtCor[useful_slices]=target_val_mean/np.mean(masked_max_freqs_mat_good_useful, axis=0)## correction is inverse to the central frequency of the slice
  # dfdtCor[overide_inds]=0.9999## don't waste voltage on correction in un needed slices
  np.geterr()
  np.seterr(all='warn')
  warnings.filterwarnings('error')
  with warnings.catch_warnings():
    warnings.filterwarnings('error')
    try:
      warnings.warn(Warning())
    except:
      Warning: print ('Raised!')
  np.seterr(all='print')

  # scale the new dfdt to the number of samples required for the system chirp used 
  #(notice dfdt correction has 1 less sample than the desired length of the
  # OldChirp_perSlice since it will be differentiatied
  corPerInd_positions=(np.arange(0,len(old_chirp_vec_cut)-1)+0.5)/(len(old_chirp_vec_cut)-1)# correction positions length is the same as np.diff(old_chirp_vec_cut)
  dfdtCor_fun=interpolate.interp1d( (np.arange(len(dfdtCor))+0.5)/len(dfdtCor) , dfdtCor,fill_value='extrapolate')
  dfdtCor_perChirpInd=dfdtCor_fun( corPerInd_positions)#,'linear','extrap')#
  print(dfdtCor_perChirpInd)
  print(type(dfdtCor_perChirpInd))
  if np.sum(np.isnan(dfdtCor_perChirpInd))>0:
    print('has nans')  
  try:
    print("length of dfdtCor_perChirpInd %f; number of values in  dfdtCor_perChirpInd<0 %f  ; sum of values in dfdtCor_perChirpInd<0 %f"  % (np.size(dfdtCor_perChirpInd), np.size(dfdtCor_perChirpInd<0),np.sum(dfdtCor_perChirpInd<0)) ) 
  
    dfdtCor_perChirpInd[dfdtCor_perChirpInd<0]=0#
    print("passed dfdtCor_perChirpInd[dfdtCor_perChirpInd<0]=0")
  except:
    print("failed:length of dfdtCor_perChirpInd[dfdtCor_perChirpInd<0] %d" % dfdtCor_perChirpInd[dfdtCor_perChirpInd<0] )
    pass
  difOldChirp_perChirpInd=np.diff(old_chirp_vec_cut)#


  # 
  # # scale the old chirp to the slices used 
  # #(notice dfdt correction has 1 less sample than the desired length of the
  # # OldChirp_perSlice since it will be differentiatied
  # 
  # oldChirp_perSlice=interp1((0:(length(old_chirp_vec_cut)-1))/(length(old_chirp_vec_cut)-1),old_chirp_vec_cut,(0:length(dfdtCor))/length(dfdtCor),'pchip')#
  # difOldChirp_perSlice=diff(oldChirp_perSlice)#

  # figure#plot(new_cor)
  # new_cor=new_cor./max(new_cor)#

  # normalize the chirp
  newChirp_perChirpInd=np.concatenate( ([0] ,np.cumsum(difOldChirp_perChirpInd*dfdtCor_perChirpInd)))## new chirp vector is the integral of the corrected dfdt vector, with added zero point

  if chirptype:
    newChirp_perChirpInd=newChirp_perChirpInd/np.amin(newChirp_perChirpInd)## down
  else:
    newChirp_perChirpInd=newChirp_perChirpInd/np.amax(newChirp_perChirpInd)## up normalize the correction from 0 to 1
  
  newChirp_perChirpInd=newChirp_perChirpInd*(Vend-Vstart)+Vstart## renormalize to the previous DAC voltage range
  # overide_inds=[1,16:19]
  # for add_inds=18:19
  # new_chirp(add_inds)=new_chirp(17)+(new_chirp(17)-new_chirp(1))/18#
  # end
  # # new_chirp=[0 cumsum(new_cor)]#
  if DebugPlot:
    fig, ax = plt.subplots()
    ax.plot(np.arange(len(newChirp_perChirpInd)) /(len(newChirp_perChirpInd)-1),newChirp_perChirpInd,label='newChirp')#
    # hold all
    ax.plot( np.arange(len(old_chirp_vec_cut)) /(len(old_chirp_vec_cut)-1),old_chirp_vec_cut,label='OldChirp')#
    ax.grid (True)#
    legend = ax.legend(loc='lower right',fontsize='x-large')
    plt.show()
  
  new_chirp_vec=create_new_LUT(newChirp_perChirpInd,chirp_vec_consts,Vstart,Vend,add_prep_vec)
  print(new_chirp_vec)
  

  # old_chirp=cur_chirp#
  # cur_chirp=new_chirp#
  #  save('new_chirp_amirad4.mat','new_chirp','old_chirp')
  # [0 0.1043 0.1859 0.2515 0.3068 0.3565 0.4033 0.4507 0.4996 0.5492 0.5999 0.6528 0.7104 0.7761 0.8495 0.9235 1.0000]


  # [ 0 0.0793 0.1524 0.2158 0.2729 0.3269 0.3806 0.4347 0.4905 0.5480 0.6063 0.6663 0.7298 0.7977 0.8652 0.9318 1.0000]
  return new_chirp_vec


if __name__ == "__main__":
  old_chirp_vec=np.arange(1200)
  target_freq=50e3
  print('this function is tested via the main of irad_stfftLinCalib')
  # new_chirp_vec=chirp_analysis_from_time_domain_LinCalib(old_chirp_vec,target_freq,max_freqs_mat,chirptype,LoadFromScope,multipulse=0, DebugPlot=1, add_prep_vec=1)