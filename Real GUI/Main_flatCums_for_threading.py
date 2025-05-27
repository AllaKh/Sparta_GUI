# ssh root@10.99.0.127
import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
import nidaqmx
import NI_handler as nih
import flatCums_algo_for_threading as flalg
import signal
import msvcrt
sys.path.append('C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/tests') 
import flatutil as flut
import queue_data_classes as q_cls



def call_getVCO(fu,eco_flg=0,fig_hand_tupple=[111]):
    time.sleep(.1)
    vco_vec=fu.GetVcoVector()
    # fig_hand_tupple=[111]
    if eco_flg :
        # print(vco_vec)
        fig_hand_tupple=flalg.plot_continue(np.arange(np.size(vco_vec)),vco_vec,'vco vec',fig_hand_tupple)
    return (vco_vec,fig_hand_tupple)

def call_setVCO(fu,list_vco_vec,eco_flg=0,fig_hand_tupple=[111],title_str='vco'):
    time.sleep(.1)
    # prep_vec=np.round(vco_vec+residual)
    # list_vco_vec=np.ndarray.tolist(prep_vec.astype(int))
    # residual=vco_vec-prep_vec
    fu.UpdateVCO(list_vco_vec)
    # fig_hand_tupple=[111]
    if eco_flg :
        # print(vco_vec)
        fig_hand_tupple=flalg.plot_continue(np.arange(np.size(list_vco_vec)),list_vco_vec,title_str,fig_hand_tupple)
    return (list_vco_vec,fig_hand_tupple)

def fun_flatCums (cal_in_dat,my_ques,fu):
    Q_calib_out=my_ques.Q_calib_output
    # Q_calib_in=my_ques.Q_calib_in
    cums_dat=cal_in_dat.cums_dat
    cur_IP=cal_in_dat.sparta_IP
    clean_axes_after=30 #repetitions
    cal_in_dat.cums_dat.clean_axes_after=clean_axes_after
    stabiliz_reps=10 #repetitions
    cal_in_dat.cums_dat.stabiliz_reps=stabiliz_reps
    fig_hand_tupple_reset=[111]
    max_signal_ind=3135
    cal_in_dat.cums_dat.max_signal_ind=max_signal_ind
    max_vco_ind=1222
    cal_in_dat.cums_dat.max_vco_ind=max_vco_ind
    counter=0
    cont_flag=1
    
    fname_str=time.strftime("C:/flat_data/%d_%b_%Y_%H_%M_%S", time.gmtime(time.time())) #time.asctime(time.gmtime(time.time()))
    print(fname_str)
    # fu = flut.FlatUtil(cur_IP,cal_in_dat.naive_connect )
    # if not( cal_in_dat.naive_connect):
    #         fu.start()  
    pause_calibrate_flag=not(cal_in_dat.but_state.cums_but)
    # calibration by Emanuel
    # while 1
    cal_dat_out=q_cls.calib_output_data()
    
    while cont_flag :
        counter+=1
        # sample digital data with NI Barak
        sampled_1bit=nih.sample_ni (anlg_ch=["Dev1/ai0"],trig_ch=["Dev1/PFI0"],clk_timing=2e6,samp_per_chan=200000,nsamp_per_ch=4000,NumOfChirps=5,plt_flag=0) 
        sampled_1bit=sampled_1bit[:,0:max_signal_ind]
        if counter==1: #initialize several values in the 1st run of the loop
            # if not pause_calibrate_flag:  
            (vco_vec0,fig_hand_tupple_vco)=call_getVCO(fu,eco_flg=0)
            vco_vec=vco_vec0
            cal_dat_out.vco_graph.set_data(ydat=vco_vec,title='VCO_data')

            # else:         
                
            #     vco_vec=vco_vec0 ################ there is a bug here in vco_vec0 handling it is not properly initialized

            vco_vec=np.asarray(vco_vec)
            residual=np.zeros(np.shape(vco_vec))

            # signal_thold = the middle level of the 1 bit signal (assumes some parts are all 1 and some are all 0 after initial calib)

            x_dat=np.transpose (np.arange(np.shape(sampled_1bit)[1]))
            
            mean_1bit_dat=np.average(sampled_1bit,axis=0) 
            mid_sig=(np.amax(sampled_1bit)-np.amin(sampled_1bit))/2 

            # fig_hand_tupple_sig=flalg.plot_continue(x_dat,mean_1bit_dat,'sampled 1bit',fig_hand_tupple_reset)
            cal_dat_out.oneBit_graph.set_data(xdat=x_dat,ydat=mean_1bit_dat,title='sampled 1bit')
            # fig_hand_tupple_err=flalg.plot_continue(x_dat,np.zeros(np.shape(x_dat)),'sampled 1bit',fig_hand_tupple_reset)
            cal_dat_out.cums_graph.set_data(xdat=x_dat,ydat=np.zeros(np.shape(x_dat)),title='1bit error')

            # Vstart=vco_vec[0]
            newVCO_tuple=flalg.flattenLaser(mean_1bit_dat,vco_vec,residual,cums_dat,signal_thold=mid_sig)
            vco_vec=newVCO_tuple[0]
            corr=newVCO_tuple[3]
            residual=newVCO_tuple[4]
            flatness=newVCO_tuple[2][2]
            Q_calib_out.put(cal_dat_out)

        elif counter< stabiliz_reps or pause_calibrate_flag:
            print('no set')
            eco_flg=0
            if not pause_calibrate_flag:
                (vco_vec,fig_hand_tupple_vco)=call_getVCO(fu,eco_flg,fig_hand_tupple_vco)  # sample VCO (from ilia)
                cal_dat_out.vco_graph.set_data(ydat=vco_vec,title='VCO_data')# this data is erased by the data in
                vco_vec=np.asarray(vco_vec)

            # x_dat=np.arange(np.shape(sampled_1bit)[0])
            mean_1bit_dat=np.average(sampled_1bit,axis=0) 
            # fig_hand_tupple_sig=flalg.plot_continue(x_dat,mean_1bit_dat,"sampled 1bit %d; flatness= %s" % (counter,flatness),fig_hand_tupple_sig) #plot mean 1-bit
            cal_dat_out.oneBit_graph.set_data(xdat=x_dat,ydat=mean_1bit_dat,title="sampled 1bit %d; flatness= %s" % (counter,flatness))


            # fig_hand_tupple_err=flalg.plot_continue(x_dat,corr,"error %d" % counter,fig_hand_tupple_err) #plot the cumsum error
            cal_dat_out.cums_graph.set_data(xdat=x_dat,ydat=corr,title="error %d" % counter)
            # fig_hand_tupple_vco=flalg.plot_continue(np.arange(max_vco_ind),newVCO_tuple[0],'vco_vec',fig_hand_tupple_vco,':') #plot desired next vco
            cal_dat_out.vco_graph.set_data(xdat=np.arange(max_vco_ind),ydat=newVCO_tuple[0],title='VCO data')# currently this overruns old VCO_data ### fix in future addition
            
            # if (1st instance) 
            # Calculate new VCO (Cumsum) Irad
            newVCO_tuple=flalg.flattenLaser(mean_1bit_dat,vco_vec,residual,cums_dat,signal_thold=mid_sig)
            vco_vec=newVCO_tuple[0]
            corr=newVCO_tuple[3]
            flatness=newVCO_tuple[2][2]

            residual=newVCO_tuple[4]
            if not counter%2:
                Q_calib_out.put(cal_dat_out)

        else:
            eco_flg=0
            if not counter%30:
                print('      set ',counter)

            mean_1bit_dat=np.average(sampled_1bit,axis=0) 
            # fig_hand_tupple_sig=flalg.plot_continue(x_dat,mean_1bit_dat,"sampled 1bit %d; flatness= %s" % (counter,flatness) ,fig_hand_tupple_sig) #plot mean 1-bit
            cal_dat_out.oneBit_graph.set_data(xdat=x_dat,ydat=mean_1bit_dat,title="sampled 1bit %d; flatness= %s" % (counter,flatness))


            # fig_hand_tupple_err=flalg.plot_continue(x_dat,corr,"error %d" % counter, fig_hand_tupple_err) #plot the cumsum error
            cal_dat_out.cums_graph.set_data(xdat=x_dat,ydat=corr,title="error %d" % counter)
            # fig_hand_tupple_err=flalg.plot_continue(np.arange(np.size(residual)),residual,"residual %d" % counter, fig_hand_tupple_err) #plot the cumsum error

            # fig_hand_tupple_vco=flalg.plot_continue(np.arange(max_vco_ind)*np.size(x_dat)/max_vco_ind,newVCO_tuple[0], "vco active %d" % counter,fig_hand_tupple_vco,':') #plot desired next vco
            # ******cal_dat_out.vco_graph.set_data(xdat=np.arange(max_vco_ind)*np.size(x_dat)/max_vco_ind,ydat=newVCO_tuple[0],title="vco active %d" % counter)# currently this overruns VCO_data ### fix in future addition
            
            if (counter % clean_axes_after)==0:
                np.savetxt(fname_str+'test%d_kd%s_kp%s_flt%s.txt' % (counter,cal_in_dat.cums_dat.Kd,cal_in_dat.cums_dat.Kp,flatness),vco_vec, delimiter=',') 
            # Calculate new VCO (Cumsum) Irad
            newVCO_tuple=flalg.flattenLaser(mean_1bit_dat,vco_vec,residual,cums_dat,signal_thold=mid_sig)
            
            vco_vec=newVCO_tuple[0]
            corr=newVCO_tuple[3]
            residual=newVCO_tuple[4]
            flatness=newVCO_tuple[2][2]
            if counter== stabiliz_reps:### change to a dedicated flag
                loaded_vco_vec=np.loadtxt(cal_in_dat.cums_dat.file_name, delimiter=',')
                vco_vec=np.ndarray.tolist(loaded_vco_vec.astype(int))
            (vco_vec,fig_hand_tupple_vco)=call_setVCO(fu,vco_vec,eco_flg,fig_hand_tupple_vco,title_str="vco active %d" % counter)
            cal_dat_out.vco_graph.set_data(xdat=np.arange(np.size(vco_vec)),ydat=vco_vec,title="vco active %d" % counter)# currently this overruns VCO_data ### fix in future addition

            if not counter%2:
                Q_calib_out.put(cal_dat_out)        # the following code allows pausing cums flattening by pressing 'q' or restarting it by pressing ';'
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

        # the following line monitors if a GUI button was pressed- to force exiting the function
        cont_flag= my_ques.Q_calib_input.qsize()<1
    print('leaving flattening')
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

        