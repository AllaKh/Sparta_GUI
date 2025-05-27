# ssh root@10.99.0.127
import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
import nidaqmx
import NI_handler as nih
import flatCums_algo as flalg
import signal
import msvcrt
sys.path.append('C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/tests') 
import flatutil_old as flut
import chirp_analysis_from_time_domain_LinCalib as linearize


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    global cont_flag
    cont_flag=0
    # sys.exit(0)
    # return 0

def call_getVCO(fu,eco_flg=0,fig_hand_tupple=[111]):
    time.sleep(.1)
    vco_vec=fu.GetVcoVector()
    MCT_vec=np.asarray(fu.GetMctVector())/100
    # fig_hand_tupple=[111]
    if eco_flg :
        # print(vco_vec)
        fig_hand_tupple=flalg.plot_continue(np.arange(np.size(vco_vec)),vco_vec,'vco vec',fig_hand_tupple)
        fig_hand_tupple=flalg.plot_continue(np.arange(np.size(MCT_vec)),MCT_vec,'VCO & MCT vec',fig_hand_tupple)
        
    return (vco_vec,fig_hand_tupple,MCT_vec)


def call_setVCO(fu,list_vco_vec,eco_flg=0,fig_hand_tupple=[111],title_str='vco'):
    time.sleep(.1)
    # prep_vec=np.round(vco_vec+residual)
    # list_vco_vec=np.ndarray.tolist(prep_vec.astype(int))
    # residual=vco_vec-prep_vec
    fu.UpdateVCO(list_vco_vec)
    MCT_vec=np.asarray(fu.GetMctVector())/100
    # fig_hand_tupple=[111]
    if eco_flg :
        # print(vco_vec)
        fig_hand_tupple=flalg.plot_continue(np.arange(np.size(list_vco_vec)),list_vco_vec,title_str,fig_hand_tupple)
        fig_hand_tupple=flalg.plot_continue(np.arange(np.size(MCT_vec)),MCT_vec,title_str,fig_hand_tupple)
    return (list_vco_vec,fig_hand_tupple,MCT_vec)

def fun_flatCums ():
    cur_IP='10.99.0.127'
    clean_axes_after=30 #repetitions
    stabiliz_reps=5 #repetitions
    fig_hand_tupple_reset=[111]
    max_signal_ind=3135
    max_vco_ind=1222
    counter=0
    cont_flag=1
    Kp=.0001 #0.0001
    Ki=.00000
    Kd=.1 #0.1 
    flat_window=0
    s=11# s must be odd
    fname_str=time.strftime("%d_%b_%Y_%H_%M_%S", time.gmtime(time.time())) #time.asctime(time.gmtime(time.time()))
    print(fname_str)

    naive_connect=0

    OldLut=linearize.get_linearization_default()
    # plt.plot(OldLut)
    # plt.show()
    
    fu = flut.FlatUtil(cur_IP,naive_connect)
    if not( naive_connect):
    
        fu.start()
        # fu.UpdatePiezo(OldLut.astype(int))


    pause_calibrate_flag=False
    # calibration by Emanuel
    # while 1
    
    while cont_flag :
        counter+=1
        # sample digital data with NI Barak
        sampled_1bit=nih.sample_ni (anlg_ch=["Dev1/ai0"],trig_ch=["Dev1/PFI0"],clk_timing=2e6,samp_per_chan=200000,nsamp_per_ch=4000,NumOfChirps=5,plt_flag=0) 
        sampled_1bit=sampled_1bit[:,0:max_signal_ind]
        if counter==1: #initialize several values in the 1st run of the loop
            if not pause_calibrate_flag:  
                (   0,fig_hand_tupple_vco,MCT_vec)=call_getVCO(fu,eco_flg=1)
                vco_vec=vco_vec0
            else:
                vco_vec=vco_vec0 ################ there is a bug here in vco_vec0 handling it is not properly initialized

            vco_vec=np.asarray(vco_vec)
            residual=np.zeros(np.shape(vco_vec))

            # signal_thold = the middle level of the 1 bit signal (assumes some parts are all 1 and some are all 0 after initial calib)

            x_dat=np.transpose (np.arange(np.shape(sampled_1bit)[1]))
            
            mean_1bit_dat=np.average(sampled_1bit,axis=0) 
            mid_sig=(np.amax(sampled_1bit)-np.amin(sampled_1bit))/2 

            fig_hand_tupple_sig=flalg.plot_continue(x_dat,mean_1bit_dat,'sampled 1bit',fig_hand_tupple_reset)
            fig_hand_tupple_err=flalg.plot_continue(x_dat,np.zeros(np.shape(x_dat)),'sampled 1bit',fig_hand_tupple_reset)
            # Vstart=vco_vec[0]
            Vstart=160
            newVCO_tuple=flalg.flattenLaser(mean_1bit_dat,vco_vec,residual,Vstart,Kp,Ki,Kd,errMin=0.01,s=s,flat_window=flat_window,signal_thold=mid_sig)
            vco_vec=newVCO_tuple[0]
            corr=newVCO_tuple[3]
            residual=newVCO_tuple[4]
            flatness=newVCO_tuple[2][2]


        elif counter< stabiliz_reps or pause_calibrate_flag:
            print('no set')
            eco_flg=1
            if not pause_calibrate_flag:
                (vco_vec,fig_hand_tupple_vco,MCT_vec)=call_getVCO(fu,eco_flg,fig_hand_tupple_vco)  # sample VCO (from ilia)
                vco_vec=np.asarray(vco_vec)

            # x_dat=np.arange(np.shape(sampled_1bit)[0])
            mean_1bit_dat=np.average(sampled_1bit,axis=0) 
            fig_hand_tupple_sig=flalg.plot_continue(x_dat,mean_1bit_dat,"sampled 1bit %d; flatness= %s" % (counter,flatness),fig_hand_tupple_sig) #plot mean 1-bit
            if (counter % clean_axes_after)==0:
                plt.cla()
            fig_hand_tupple_err=flalg.plot_continue(x_dat,corr,"error %d" % counter,fig_hand_tupple_err) #plot the cumsum error
            if (counter % clean_axes_after)==0:
                plt.cla()
            fig_hand_tupple_vco=flalg.plot_continue(np.arange(max_vco_ind),newVCO_tuple[0],'vco_vec',fig_hand_tupple_vco,':') #plot desired next vco
            fig_hand_tupple_vco=flalg.plot_continue(np.arange(len(MCT_vec)),MCT_vec,'vco_vec',fig_hand_tupple_vco,':') #plot desired next vco
            if (counter % clean_axes_after)==0:
                plt.cla()
            # if (1st instance) 
            # Calculate new VCO (Cumsum) Irad
            newVCO_tuple=flalg.flattenLaser(mean_1bit_dat,vco_vec,residual,Vstart,Kp,Ki,Kd,errMin=0.01,s=s,flat_window=flat_window,signal_thold=mid_sig)
            vco_vec=newVCO_tuple[0]
            corr=newVCO_tuple[3]
            flatness=newVCO_tuple[2][2]

            residual=newVCO_tuple[4]

        else:
            eco_flg=1
            print('set')

            mean_1bit_dat=np.average(sampled_1bit,axis=0) 
            fig_hand_tupple_sig=flalg.plot_continue(x_dat,mean_1bit_dat,"sampled 1bit %d; flatness= %s" % (counter,flatness) ,fig_hand_tupple_sig) #plot mean 1-bit
            if (counter % clean_axes_after)==0:
                plt.cla()
            fig_hand_tupple_err=flalg.plot_continue(x_dat,corr,"error %d" % counter, fig_hand_tupple_err) #plot the cumsum error
            # fig_hand_tupple_err=flalg.plot_continue(np.arange(np.size(residual)),residual,"residual %d" % counter, fig_hand_tupple_err) #plot the cumsum error
            if (counter % clean_axes_after)==0:
                plt.cla()
            fig_hand_tupple_vco=flalg.plot_continue(np.arange(max_vco_ind)*np.size(x_dat)/max_vco_ind,newVCO_tuple[0], "vco active %d" % counter,fig_hand_tupple_vco,':') #plot desired next vco
            if (counter % clean_axes_after)==0:
                plt.cla()
                np.savetxt(fname_str+'test%d_kd%s_kp%s_flt%s.txt' % (counter,Kd,Kp,flatness),vco_vec, delimiter=',') 
            # Calculate new VCO (Cumsum) Irad
            newVCO_tuple=flalg.flattenLaser(mean_1bit_dat,vco_vec,residual,Vstart,Kp,Ki,Kd,errMin=0.01,s=s,flat_window=flat_window,signal_thold=mid_sig)
            
            vco_vec=newVCO_tuple[0]
            corr=newVCO_tuple[3]
            residual=newVCO_tuple[4]
            flatness=newVCO_tuple[2][2]
            if counter== stabiliz_reps:### change to a dedicated flag
                loaded_vco_vec=np.loadtxt('C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/24_Jun_2019_08_27_49test840_kd0.1_kp0.0001_flt1951.txt', delimiter=',')
                vco_vec=np.ndarray.tolist(loaded_vco_vec.astype(int))
            (vco_vec,fig_hand_tupple_vco,MCT_vec)=call_setVCO(fu,vco_vec,eco_flg,fig_hand_tupple_vco,title_str="vco active %d" % counter)
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print(key)   # just to show the result
            print('Pause')
            if pause_calibrate_flag:
                pause_calibrate_flag= not(key == b';') 
                print(pause_calibrate_flag)
            else:
                pause_calibrate_flag= key == b'q' 
                print(pause_calibrate_flag)
    return newVCO_tuple
    

if __name__ == "__main__":
    fun_flatCums()
            # if stabiliz_reps 
            # Freeze VCO (Ilya)
        # Update VCO (Ilya)

    #     signal.signal(signal.SIGINT, signal_handler)
    #     print('Press Ctrl+C')
    # plt.show
    # forever = threading.Event()
    # forever.wait()
        # try:
        #     print("1")
        # except KeyboardInterrupt:
        #     sys.exit(0)
        #     print ('All done')
        #     # If you  want the loop to finish
        # cont_flag=0

        