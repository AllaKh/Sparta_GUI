import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
# test_plot_spec = impl.spec_from_file_location("test_plot", "C:/Users/User/irad_try/sparta.app/tests/test_plot.py")
# test_plot = impl.module_from_spec(test_plot_spec)
# test_plot_spec.loader.exec_module(test_plot)

def smooth (data,smooth_win):
    # smooth_win must be an odd number
    if np.size(smooth_win)==1:
        conv_mat= data
        iters=(smooth_win-1)/2
        iters=np.round(iters).astype(int)
        for iter in range(1,iters+1):
            n_fill= np.empty(iter)
            n_fill.fill(np.nan)
            top_vec=np.r_[n_fill, np.roll(data,iter)[iter:-iter],n_fill]
            bot_vec=np.r_[n_fill, np.roll(data,-iter)[iter:-iter],n_fill]
            conv_mat=np.r_['0,2',top_vec,conv_mat,bot_vec] 
        smoothed_vec=np.nanmean(conv_mat, axis=0)
    else: 
        print('implement complicated windows')

    return smoothed_vec

def read_external_vco(vco_file_name):
    vco_data= np.array( [] )
    with open(vco_file_name) as csvfile:


        vco_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        # f = open(vco_file_name, "r")
        for cur_row in vco_reader:
            print(cur_row)
            print(type(cur_row))
            ttt=np.asarray(cur_row, dtype=int)
            print(ttt)
            if vco_data.size ==0: ########################################
                vco_data=ttt
            else:
                vco_data=np.vstack ((vco_data,ttt) )    
    return vco_data

def read_NI_vec(vco_file_name):

    f = open(vco_file_name, "r")
    print(f.readline())
    print(f.readline())

def plot_continue(x_dat,y_dat,title_str,fig_hand_tuple,line_spec='-'):
    if len(fig_hand_tuple)==1:
        plt.ion()
        fig_hand = plt.figure()
        axx = fig_hand.add_subplot(fig_hand_tuple[0],title=title_str)
        sc1, = axx.plot(x_dat,y_dat,line_spec)
        plt.grid(True)

    else:
        fig_hand=fig_hand_tuple[0]
        axx=fig_hand_tuple[1]
        plt.sca(axx)
        plt.title(title_str)
        a= fig_hand.canvas.draw()
        sc1, = axx.plot(x_dat,y_dat,line_spec)
        plt.grid(True)
        plt.pause(0.01) 
    return fig_hand,axx

def generate_signal_dat(true_signal,oldVCO,dynamic_range,noise_amp):
    signal_dat=true_signal+noise_amp*np.random.randn(np.size(true_signal))
    # signal_dat[(true_signal-oldVCO)>dynamic_range]=1
    # signal_dat[(oldVCO-true_signal)>dynamic_range]=0
    # signal_dat=signal_dat>np.median(signal_dat)
    signal_dat[true_signal>oldVCO]=1
    signal_dat[true_signal<oldVCO]=0

    return signal_dat

# def smooth_data (data,smooth_win)

    

def flattenLaser(signal_dat,list_vco_vec,residual,Vstart,Kp,Ki,Kd,errMin,smooth_win,flat_window,signal_thold=0.15):
# this function generates a new VCO vector whose application to the laser will bring its amplitude closer to the chip calibration point,
# by making the digital signal output closer to 50% "1"s at any given time interval
# the error to be minimzed is defined as the distance of the the cumulative sum of the signal (after converting all "0" to "-1" for matematical convenience) 
# from 0 at any point in time.
## inputs
# signal_dat - the data arriving from the MCT (after waiting Tos seconds)
# oldVCO - the vector applied on the VCO on the previous pulse
# Vstart - The initial voltage applied on the VCO
# Kp,Ki,Kd - gains of the PID controller
# errMin - minimal error allowed
# s - Relative size of the window used for smoothing (s must be odd)
# flat_window- 0 for cumsum, any other value is the window size to sum
# signal_thold- the voltage level in middle between the the "1" level and "0" level of the 1-bit digital signal

## outputs
# newVCO - the vector that will be applied on the VCO in the next pulse
# meanPower - the average power of the laser (for logging issues)
# flatness - the degree of flatness of the power (for logging issues)

## parameters of the whole system
    Fs=2e6 # sampling frequency of the Msignal (units of Hz). will be probably will be different in the real system
    Tos=222e-6 #100e-6; # the time delay between ignition and sampling (units of sec)

    ##
    # taking out the first samples from the MCT, sent during the Tos seconds of
    # the pulse
    oldVCO=np.asarray(list_vco_vec)
    signal_time_base=np.arange(0,np.size(signal_dat))/Fs
    VCO_time_base=np.linspace(0,np.size(signal_dat)/Fs,num=np.size(oldVCO))
    choppedVCO=oldVCO[VCO_time_base>=Tos]
    choppedVCO_time_base=VCO_time_base[VCO_time_base>=Tos]
    # choppedVCO=oldVCO(end-length(signal_dat)+1:end)###############################################unexplained line

    # calculate mean power (also relevant for the log file, telemetry)
    signal_dat=(signal_dat/signal_thold)-1 # linearly transform a signal span from [0:2*signal_thold] to [-1:1]
    # plot_continue(signal_time_base,signal_dat,'sig')
    first_live_ind=np.argmax(signal_time_base>Tos).astype(int) # assuming the first live ind is "1"
    # first_live_ind=500 # assuming the first live ind is "1"
    first_min_ind=1000 #np.argmin(signal_dat[first_live_ind:])+first_live_ind # assuming the first min ind is "-1"
    # first_correction_ind=np.argmin(np.abs(signal_dat[first_live_ind:first_min_ind]))+first_live_ind # looking for the first "0" in the live zone
    # first_correction_ind=first_live_ind
    first_correction_ind=200
    # print([first_live_ind, first_correction_ind,first_min_ind ])
    cumsum_dat=np.cumsum(signal_dat)#.astype(int)
    meanPower=np.average(signal_dat)
    # print(type(flat_window))
    if  not(type(flat_window) is int):
        flat_window=flat_window.astype(int)
    # calculate the error used for the PID controller
    if flat_window==0:#if flat_window is 0 use cumsum of the data as the dependent variable  
        cumsum_offset=cumsum_dat[first_correction_ind]
        cumsum_dat=cumsum_dat-cumsum_offset # pull the error to 0 at the first "0"
        err=cumsum_dat
    else:
        flat_window=np.asarray(flat_window,dtype=int)
        err=cumsum_dat-np.append(np.zeros([1,flat_window]),cumsum_dat[0:-flat_window])
    err[np.abs(err)<errMin]=0
    # plot_continue(signal_time_base,err,'err')
    # calculate the degree of flatness (relevant for the log file, telemetry)
    # flatness=np.average(err**2)
    flatness=np.sum (np.abs(signal_dat)<.6 )
    chopped_err=np.interp(choppedVCO_time_base,signal_time_base,err)
    # calculate the new VCO waveform for the next pulse
    corr=err*Kp+np.cumsum(err)*Ki+np.append(0, np.diff(err))*Kd #corr is used only for display, it must be the same as chopped_corr with different time domain
    chopped_corr=chopped_err*Kp+np.cumsum(chopped_err)*Ki +np.append( np.diff(chopped_err)[0], np.diff(chopped_err))*Kd
    # corr=np.append(np.zeros(np.size(err)-np.size(chopped_err)), corr)
    # choppedNewVCO=choppedVCO-chopped_err*Kp-np.cumsum(chopped_err)*Ki- np.append( np.diff(chopped_err)[0], np.diff(chopped_err))*Kd
    choppedNewVCO=choppedVCO-chopped_corr
    # linear intepolation from Vstart to the initial calculated value
    # plot_continue(choppedVCO_time_base,choppedNewVCO,"chopped new vco")
    if (oldVCO[-np.size(choppedNewVCO)-1]==0) or (oldVCO[-np.size(choppedNewVCO)]> 254):
        print('bpoint')
    # keep the shape of the VCO vector where it is not flattened
    # old_vco_converted=(oldVCO[VCO_time_base<Tos] -Vstart)*(choppedNewVCO[0]-Vstart)/(oldVCO[-np.size(choppedNewVCO)-1]-Vstart) +Vstart 
    old_vco_converted=np.linspace(Vstart,choppedNewVCO[0],np.sum([VCO_time_base<Tos]))
    newVCO=np.concatenate((old_vco_converted, choppedNewVCO),axis=0)
    # figure;hold on;plot(choppedVCO);plot(choppedNewVCO-mean(choppedNewVCO)+mean(choppedVCO))
    # figure;hold on;plot(signal_dat-meanPower);plot(err)

    # the VCO voltage cannot be above 5 or below 0 volts
    # newVCO[newVCO>255]=255
    # newVCO[newVCO<0]=0

    smooth_new_vco=smooth (newVCO+residual,smooth_win) 
    round_new_vco=np.round(smooth_new_vco)
    # round_new     _vco[smooth_new_vco>254 and smooth_new_vco<255]=254

    round_new_vco[round_new_vco>255]=255
    round_new_vco[round_new_vco<0]=0

    list_vco_vec=np.ndarray.tolist(round_new_vco.astype(int))
    residual=smooth_new_vco-round_new_vco
    residual[round_new_vco+residual>255]=0
    residual[round_new_vco+residual<0]=0
    newVCO=np.round(newVCO)

    # smooth the VCO waveform
    # newVCO=smooth(newVCO,round(length(newVCO)*s))################################  add smoothing later

    # turn the VCO vector to 8bits
    a=0
    if a==1 :
        fig_hand_tuple1=plot_continue(np.arange( np.size(cumsum_dat) ),cumsum_dat,'cumsum_dat',fig_hand_tuple=[111])
        fig_hand_tuple1=plot_continue(np.arange( np.size(err) ),err,'cumsum_dat',fig_hand_tuple1)

    return list_vco_vec,meanPower,(cumsum_dat,err,flatness),corr,residual

if __name__ == "__main__":

    print(sys.argv)
    with open('eggs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        spamwriter.writerow(range(-1,8))
        spamwriter.writerow(range(-2,7))
        spamwriter.writerow(range(-3,6))
    # vco_data = read_external_vco("eggs.csv")
    # true_signal= np.sin(np.linspace(-30,30,10000))*64+64
    true_signal= np.linspace(0,30,10000)+64
    fig_hand_tuple1=plot_continue(np.arange( np.size(true_signal) ),true_signal,'sig',fig_hand_tuple=[111])

    Vstart=128
    dynamic_range=5
    oldVCO=np.ones(10000)*Vstart
    fig_hand_tuple=plot_continue(np.arange( np.size(oldVCO) ),oldVCO,'sig',fig_hand_tuple1)
    counter=0
    while True:
        signal_dat=generate_signal_dat(true_signal,oldVCO,dynamic_range,noise_amp=3)
        # if counter==1:
        #     fig_hand_tuple2=plot_continue(np.arange( np.size(signal_dat) ),signal_dat,"SIGNAL %d" % counter,fig_hand_tuple=[111])
        newVCO_tuple=flattenLaser(signal_dat,oldVCO,Vstart,Kp=-.01,Ki=0,Kd=0,errMin=0.01,s=10,flat_window=0)
        oldVCO=newVCO_tuple[0]
        err=newVCO_tuple[3]
        if counter==1:
            fig_hand_tuple2=plot_continue(np.arange( np.size(err) ),err,"SIGNAL CUMSUM %d" % counter,fig_hand_tuple=[111])
        counter+=1
        if (counter % 10)==0:
            plot_continue(np.arange( np.size(oldVCO) ),oldVCO,"VCO %d" % counter,fig_hand_tuple1)
            plot_continue(np.arange( np.size(true_signal) ),true_signal,"VCO %d" % counter,fig_hand_tuple1)
            if (counter % 150)==0:
                plt.cla()
            plot_continue(np.arange( np.size(err) ),err,"SIGNAL CUMSUM %d" % counter,fig_hand_tuple2)
            if (counter % 150)==0:
                plt.cla()
    print(vco_data)
    # read_external_vco(sys.argv[1])

    # rpc_client(sys.argv[1] )