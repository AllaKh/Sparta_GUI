import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
from itertools import compress
from chirp_analysis_from_time_domain_LinCalib import chirp_analysis_from_time_domain_LinCalib as ch_an

def irad_stfftLinCalib(sensorTdata,target_freq,plot_flag,LoadFromScope,n_inds_per_slice):
    ##31/10 noise estimation is calculated from the signal, no need to inject
    ##the noise figure
    # n_inds_per_slice=10000# number of bins
    tdat_length=np.shape(sensorTdata)[0] # assume each column is one time domain vector
    #n_inds_per_slice=floor(tdat_length/3)# number of bins

    if LoadFromScope:
        #slice_Tlen=n_inds_per_slice/66e4
        slice_Tlen=1.55e-3 * n_inds_per_slice/tdat_length
        # slice_Tlen=5e-7*n_inds_per_slice### for testing only
        min_slice=13000
    else:
        slice_Tlen=n_inds_per_slice/2e6
        min_slice=500
    df=1/slice_Tlen
    fvec_full=np.arange(np.round(tdat_length/2)) *df
    fvec=np.arange(np.round(n_inds_per_slice/2)) *df
    f_target_ind=np.argmin(abs(fvec-target_freq))
    # f_target_ind=f_target_ind[0]# good_inds=200:1650
    fft_relevant_target_range=np.arange(np.floor(f_target_ind/2),np.ceil(f_target_ind*2),dtype=int)

    slice_jump= np.minimum(min_slice,np.floor (n_inds_per_slice/2)).astype(int)

    slice_start_ind_vec=np.arange(0,tdat_length-n_inds_per_slice-1,slice_jump)
    max_bins=np.zeros(len(slice_start_ind_vec))
    max_vals=np.copy(max_bins)
    max_freqs=np.copy(max_bins)
    widths=np.copy(max_bins)
    counter=0
    # max_mean_bin_mat=[]
    # max_mean_vals_mat=[]
    # width_mat=[]
    # if plot_flag>1:
        
    #     h=figure
    fft_dat_full=np.fft.fft( sensorTdata,axis=0)
    cur_mean_fft_full=np.mean (np.abs(fft_dat_full),axis=1)
    try:
        noise_now_pp=np.polyfit(np.log(fvec_full[1:]),np.log(cur_mean_fft_full[1:]),1)# index is intentionally "1"  to discard DC bin. this is not an error in transfer from matlab...
        cur_mean_fft_cor_full=cur_mean_fft_full[0:len(fvec_full)]-np.exp(noise_now_pp[1])*fvec_full**noise_now_pp[0] 

    except:
        print("slice %d has no std" %counter)
        cur_mean_fft_cor_full=cur_mean_fft_full[0:len(fvec_full)]
    if plot_flag:    
        plt.plot(cur_mean_fft_cor)
        plt.show()

    for ind in slice_start_ind_vec :
        cur_dat=sensorTdata[ind:(ind+n_inds_per_slice),:]
        mean_cur_Tdat= np.mean(cur_dat,axis=1)
        remove_ind1= np.mean(mean_cur_Tdat)<0.05 or np.mean(mean_cur_Tdat)>0.95 # if the slice is close to one of the rails- remove it

        # if the slice has a long stretch of ones or zeros (1/4 of the data)
        cums_cur_Tdat=np.cumsum(2*mean_cur_Tdat-1) #convert 0 to -1
        remove_ind2= np.amax(np.abs(cums_cur_Tdat)) > np.size(mean_cur_Tdat)/4 

        # remove_ind2= np.cumsum(mean_cur_Tdat)<0.05 or np.mean(mean_cur_Tdat)>0.95
        if remove_ind2 or remove_ind1:
            max_bins[counter]=0
            max_freqs[counter]=0
            max_vals[counter]=0
            widths[counter]=0
        else:
            fft_dat=np.fft.fft( cur_dat,axis=0)
            cur_mean_fft=np.mean (np.abs(fft_dat),axis=1)
            cur_std_fft=(np.std (np.imag(fft_dat),axis=1)**2+np.std (np.real(fft_dat),axis=1)**2)**0.5
            std_fit_inds=np.squeeze(np.asarray(np.nonzero(cur_mean_fft[1:len(fvec)]>0))+1)# index is intentionally "1"  to discard DC bin. this is not an error in transfer from matlab...
            try:
                noise_now_pp=np.polyfit(np.log(fvec[std_fit_inds]),np.log(cur_mean_fft[std_fit_inds]),1)
                cur_mean_fft_cor=cur_mean_fft[0:len(fvec)]-np.exp(noise_now_pp[1])*fvec**noise_now_pp[0] 

            except:
                print("slice %d has no std" %counter)
                cur_mean_fft_cor=cur_mean_fft[0:len(fvec)]
            # cur_mean_fft_cor=cur_mean_fft[0:len(fvec)]
            # if plot_flag>1:
                # figure(h)
            
                # plot(fvec,cur_mean_fft_cor)
                # title([num2str( ind),' to ',num2str(ind+n_inds_per_slice)])
            
                # hold all
                # #         xlim ([0 30])
                # #         ylim ([0 5])
                # grid
                #         pause(1)
                #         xlim auto
                #         ylim auto
            
            #     cur_fft_cor=cur_fft.*(0:(length(cur_fft)-1))'
            max_val=np.amax(cur_mean_fft_cor[fft_relevant_target_range])
            max_bin= np.round(np.mean(np.where(cur_mean_fft_cor[fft_relevant_target_range] == max_val))).astype(int)
            #     max_bin
            max_bins[counter]=max_bin+fft_relevant_target_range[0]#*round(2000/n_inds_per_slice)+1# find the relevant bin
            
            max_freqs[counter]=fvec[max_bins[counter].astype(int)]
            
            #     max_mean_bin(counter)=(cur_max_bin)
            max_vals[counter]=max_val
            
            
            widths[counter]=np.mean(np.sum(cur_mean_fft_cor[fft_relevant_target_range]>max_val/2))
        counter=counter+1
            #     width1=sum(irad_up_clean(120:150)>(max(irad_up_clean(51:200))/2))
        
        # if plot_flag>0:
        #     figure(99)
        #     plot(max_freqs,max_vals,'o--')
        #     hold all
        #     plot(max_freqs(1),max_vals(1),'*')
        
        
    return max_bins,max_freqs,max_vals,widths,cur_mean_fft_cor_full,fvec_full

if __name__ == "__main__":
    n_samp=4000
    n_vecs=20
    t_tot=1.55e-3
    dt=t_tot/n_samp
    t_vec=np.arange(n_samp)*dt
    fi=150e3
    ff=180e3
    f_target=(ff+fi)/2

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

    max_bins,max_freqs,max_vals,widths=irad_stfftLinCalib(sig_mat,f_target,0,1,n_inds_per_slice)
    fig_hand = plt.figure()
    axx = fig_hand.add_subplot(111,title='max_freqs')
    sc1 = axx.plot(np.arange(np.size(max_freqs)),max_freqs,'-')
    plt.grid(True)    # end
    plt.show()
    max_freqs_mat=np.concatenate((max_freqs[None,:],max_freqs[None,:]),axis=0)
    old_chirp_vec=np.arange(1200)
    target_freq=50e3
    new_chirp_vec=ch_an(old_chirp_vec,f_target,max_freqs_mat,0,1,multipulse=0, DebugPlot=1, add_prep_vec=1)





