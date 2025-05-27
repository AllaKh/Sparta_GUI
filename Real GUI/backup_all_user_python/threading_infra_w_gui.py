import threading
import time 
from queue import Queue
import os, sys
import time,threading,sys
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt
import csv
import importlib.util as impl
from itertools import compress
from scipy import interpolate
from chirp_analysis_from_time_domain_LinCalib import chirp_analysis_from_time_domain_LinCalib as ch_an
import chirp_analysis_from_time_domain_LinCalib as linearize
from irad_stfftLinCalib_for_threading import irad_stfftLinCalib as stft
sys.path.append('C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/tests') 
import flatutil as flut
sys.path.append('C:/Users/Oryx/Documents/python3sv/PFE_Shutle/Automation_Optics')
import MAIN_PFE_SHUTTLE as shtl_cal
import CHANGE_REG_SHUTTLE as shtl_reg
import visa 
import SampleSigByClock as ssclk
import Main_flatCums_for_threading as cums
from collections import namedtuple as nmd
import LinearizationCalc_for_threading as lin_cal
import SetupandSampleFromScope as set_samp
import SetupFromScope as set_samp
import main_GUI
import queue_data_classes as q_cls
import SetupFromScope as set_scop
import FftFromTimeDomain_for_threading as fft_mod



print_lock = threading.Lock()
cur_IP = '10.99.0.127'
class MyThread(threading.Thread):
    def __init__(self, queues, top_function, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queues
        self.daemon = True
        self.receive_messages = args[0]
        self.main_fun=top_function
        self.args=args[0]

    def run(self):
        print ("start",threading.currentThread().getName(), self.receive_messages)

        try:
            # task=ques.Q_calib_input.get(False)
            # task[1]
            task = self.queue.Q_calib_input.get(False)
            self.do_thing_with_message(task)

            #Opt 1: Handle task here and call q.task_done()
        except:
            #Handle empty queue here
            print("queue size before get",self.queue.Q_calib_input.qsize())
            pass
        print("queue size after get",self.queue.Q_calib_input.qsize())

        print("get msg")
        self.main_fun(self.queue,self.args)

    def do_thing_with_message(self, message):
        print("in do_thing_with_message",self.receive_messages)
        if self.receive_messages:
            print("self.receive_messages")
            time.sleep(0.5)

            with print_lock:
                print (threading.currentThread().getName(), "Received {}".format(message))
        print("bye")
    # def run_provided_method

def old_thread_try(my_ques):
    threads = []
    for t in range(10):
        q = Queue()
        threads.append(MyThread(my_ques,len, args=(t+1,)))
        threads[t].start()
        time.sleep(0.1)
    counter=0
    for t in threads:
        counter=counter+1
        print("ilia",counter)
        # print("queue size before put",qsize(q))

        t.queue.Q_calib_input.put('Print this! %d' %counter)
        print("queue size after put",my_ques.Q_calib_input.empty())

        time.sleep(0.1)

    for t in threads:
        t.join()

def lin_top(OldLut,fu,cal_in_dat,my_ques):
    NumOfChirps=cal_in_dat.lin_dat.Nchirps
    # SampledData,time_dat,fs = set_samp.main_grab(NumOfChirps)
    SampledData,time_dat,fs = set_samp.main_grab(cal_in_dat.scope_dat)
    str=cal_in_dat.lin_dat.file_name
#     str='C:/lin_data/piezo_lut_0_10000.txt'
    # str='C:/Users/Oryx/Desktop/piezo_lut_0_10000Linear.txt'
#     SampledData=np.loadtxt("this_dat.txt")
    # OldLut=np.loadtxt(str)
    # target_freq=cal_in_dat.lin_dat.target_freq
    iters=np.fromstring(cal_in_dat.lin_dat.iters[1:-1],sep=',')
    if len(iters)==1 and iters<10:
        n_inds_vec=np.linspace(300,700,num=iters[0].astype(int) ,endpoint=True)
    else:
        n_inds_vec=iters

    n_inds_per_slice_vec=np.round(n_inds_vec/2000*np.shape(SampledData)[0]).astype(int)
    counter=0
    # n_inds_per_slice_vec=np.round(np.array( [300])/2000*np.shape(SampledData)[0]).astype(int)
    for cur_n_inds_per_slice in n_inds_per_slice_vec:
        newLUT=lin_cal.LinearizationCalc(OldLut,SampledData,cal_in_dat,ChirpType=0,my_ques=my_ques,n_inds_per_slice=cur_n_inds_per_slice,UseScope=1)
        newLUT=newLUT.astype(int)
        # plt.plot(newLUT)
        # plt.show()
        # cal_out_dat=q_cls.calib_output_data()
        # cal_out_dat.lin_graph.set_data(ydat=OldLut,title='Old piezo LUT again')
        # cal_out_dat.message='created linearization vector'
        # my_ques.Q_calib_output.put(cal_out_dat)
        time.sleep(1)
        print('should update lin_graph')
        fu.UpdatePiezo(newLUT)
        print('sent piezo LUT')

        np.savetxt(str[:-4]+"_iter_%d" %counter+str[-4:], newLUT)
        print(str[:-4]+"_iter_%d" %counter+str[-4:])
        counter+=1
        # cal_out_dat.vco_graph.set_data(ydat=newLUT,title='new piezo LUT')
        # cal_out_dat.message='created linearization vector'
        # my_ques.Q_calib_output.put(cal_out_dat)
        print('should update vco_graph')
        OldLut=np.copy(newLUT)
        if not(cur_n_inds_per_slice==n_inds_per_slice_vec[-1]):
            SampledData,time_dat,fs = set_samp.main_grab(cal_in_dat.scope_dat)
    

    return newLUT

def calib_fun(my_ques,args):
    # start calib_thread which will run the laser in MCT flattening mode. immidiately push the 1st lineariztion vector to protect piezo
    # inside calib thread send  VCO graphs via Q_calib_output while making sure no response to buttons for 30 TBD seconds
    # calib thread should be initialized calling Main_flatCums_for_threading with pause_calibrate_flag=True (so cumsum flattening doesn't take over)
    # inside calib thread:
    #   while 1:
    #       check the state of the Q_calib_input periodically and wait for a request to perform any calibration
    #       if cumsum flattening or pause flattening: [0,1,0] or [0,0,0]
    #           call Main_flatCums_for_threading with pause_calibrate_flag=false
    #           FFT will continue grabbing and analysing
    #       if linearization or chip calib: # state is [1,0,0] or [0,0,1]
    #           send FFT_Thread a "busy" via Q_state_fft 
    #           verify FFT is done by checking if Q_state_fft is empty 
    #           perform the relevant calibration with the acquired data (by calling the relevant function)
    #           when function finishes - send a notification in Q_state_out so GUI_thread can reset the button state to [0,0,0]
    #           when function finishes - send FFT_Thread a "not busy" via Q_state_fft can acquire data from the scope
    time.sleep(1)
    no_in_dat=1
    while no_in_dat:
        try:
            cal_in_dat = my_ques.Q_calib_input.get()
            print('received Q_calib_input')
            # print("no_in_dat {}".format(no_in_dat))
            no_in_dat=0
            #Opt 1: Handle task here and call q.task_done()
        except:
            #Handle empty queue here
            print("$$$$no data in Q_calib_input",my_ques.Q_calib_input.qsize())
            pass
        print("queue size after get irad",my_ques.Q_calib_input.qsize())
    
    naive_connect=cal_in_dat.naive_connect#cahnge to 1 in code if necessary for testing

    OldLut=linearize.get_linearization_default(cal_in_dat.lin_dat.file_name)
    cal_out_dat=q_cls.calib_output_data()
    cal_out_dat.lin_graph.set_data(ydat=OldLut,title='Old piezo LUT')
    cal_out_dat.message='pushed linearization vector, MCT flattening started'
    my_ques.Q_calib_output.put(cal_out_dat)
    print("put to Q_calib_output performed ")
    # update other threads that we can start working
    state_dat=q_cls.state_data()
    state_dat.busy=0
    my_ques.Q_state_out.put(state_dat)
    my_ques.Q_state_fft.put(state_dat)

    # plt.plot(OldLut)
    # plt.show()
    
    fu = flut.FlatUtil(cal_in_dat.sparta_IP,naive_connect)
    if not( naive_connect):
    
        fu.start()
        fu.UpdatePiezo(OldLut.astype(int))
        time.sleep(20)
        # print("1 update")
        # fu.UpdatePiezo(OldLut.astype(int))
        # print("2 update")
    # 1st iteration checking button state
    but_state=cal_in_dat.but_state
    but_sum = but_state.lin_but + but_state.cums_but + but_state.chip_but
    continue_to_next_loop=0
    counter=0
    while 1:
        counter+=1
        if continue_to_next_loop:
            time.sleep(1)
        else:
            if but_sum>1:
                print('error in button state')
                break
            elif but_sum==0: # no button is pressed. if this is the 1st run- MCT flattening will automatically persist. otherwise flattening is stopped and the last VCO vector will persist
                print('no calib- continue grab')
                state_dat.busy=0
                my_ques.Q_state_out.put(state_dat)
                my_ques.Q_state_fft.put(state_dat)
                time.sleep(1)
                try:
                    shtl_reg.main(mode="Set_register",reg_val_pair=[('dac_init',cal_in_dat.chip_dat.Vbias),('CMPIN_SEL',cal_in_dat.cums_dat.by_D2S)])# load last calibration (********assuming Vb was set to 55e-3 ***fix later to save vb with calibration********)and switch to D2S output 
                except:
                    print('chip calibration register loading failed, perform chip calibration')
                cums.fun_flatCums(cal_in_dat,my_ques,fu)
            elif but_state.cums_but:
                print('perform cumsum flattening -continue grab')
                state_dat.busy=0
                my_ques.Q_state_out.put(state_dat)
                my_ques.Q_state_fft.put(state_dat)
                # time.sleep(1)
                try:
                    shtl_reg.main(mode="Set_register",reg_val_pair=[('dac_init',cal_in_dat.chip_dat.Vbias),('CMPIN_SEL',cal_in_dat.cums_dat.by_D2S)])# load last calibration (********assuming Vb was set to 55e-3 ***fix later to save vb with calibration********)and switch to D2S output 
                except:
                    print('chip calibration register loading failed, perform chip calibration')
                cums.fun_flatCums(cal_in_dat,my_ques,fu)
                
            else:
                print(' pause grabbing')
                state_dat.busy=1
                my_ques.Q_state_out.put(state_dat)
                my_ques.Q_state_fft.put(state_dat)
                time.sleep(1)
                busy_received=0
                while not busy_received:
                    busy_received= ( my_ques.Q_state_fft.qsize() == 0) & ( my_ques.Q_state_out.qsize() == 0)
                    # busy_received=1
                    print("**********busy_recieved not tested, chnage in future versions*******")
                    time.sleep(1)
                ## verify that the scope is set to the proper settings

                if but_state.lin_but: # request to perform linearization by pressing the linearization button
                    print('linearization')
                    # time.sleep(2)
                    cal_in_dat.scope_dat.set_scope_dat(cal_in_dat.lin_dat.scope_delay,cal_in_dat.lin_dat.scope_scale,cal_in_dat.lin_dat.Nchirps)
                    NewLut=lin_top(OldLut,fu,cal_in_dat,my_ques)
                    print("******* linearization done******")
                else :# this means chip_but= 1 : perform chip calibration
                    print('chip calibration')
                    ## verify that the scope is set to the proper settings
                    cal_in_dat.scope_dat.set_scope_dat(cal_in_dat.chip_dat.scope_delay,cal_in_dat.chip_dat.scope_scale)
                    shtl_cal.main(mode="Flow_rev2",Vb_start=cal_in_dat.chip_dat.Vbias)

                # report to other threads work can continue    
                state_dat.busy=0
                my_ques.Q_state_out.put(state_dat)
                my_ques.Q_state_fft.put(state_dat)
        # if new_linearization:
        #     a='place holder'
        #     #### push linearization vector
        #     new_linearization=0
        try:
            cal_in_dat = my_ques.Q_calib_input.get(False)
            print('received Q_calib_input')
            but_state=cal_in_dat.but_state
            but_sum = but_state.lin_but + but_state.cums_but + but_state.chip_but
            continue_to_next_loop=0
        except:
            continue_to_next_loop=1
            if counter%30:
                print("%d no data in Q_calib_input"% counter)
            pass
        # fu.UpdatePiezo(NewLut.astype(int))
    # return NewLut

def fft_fun(my_ques,args):
    # start FFT_Thread with relevant parameters from Q_FFT_input. data should be garbage.
    # 
    # inside FFT_thread:
    #   read start_state from Q_state_fft
    #   while start_state:
    #       get parameters from Q_FFT_input
    #       grab data from scope 
    #       analyse the data
    #       send analysed data to Q_FFT_output
    #       read start_state from Q_state_fft is performed as the first action in this loop and sends a continue to the loop so no conflict with scope occurs
    state_dat=q_cls.state_data()
    state_dat.busy=1
    first_input_received=0
    counter=0
    while 1:
        counter+=1

        try:
            state_dat = my_ques.Q_state_fft.get(False)
            
            print('received Q_state_fft')
            counter=0
            #Opt 1: Handle task here and call q.task_done()
        except:
            #Handle empty queue here
            time.sleep(1)
            # print('slept %d' %counter)
            if not counter%30:
                print("**",counter,"no data in Q_state_fft",my_ques.Q_state_fft.qsize(),"current state_dat.busy is",state_dat.busy)
            pass
        if not counter%30:
            print("-----------",counter," : fft thread still alive")
            
        if state_dat.busy:
            continue

        try:
            fft_in_dat = my_ques.Q_FFT_input.get(False)
            print('received Q_fft_input')
            #Opt 1: Handle task here and call q.task_done()
            first_input_received=1
        except:
            #Handle empty queue here
            time.sleep(1)
            # counter+=1
            # print('slept %d' %counter)
            if not counter%30:
    
                print("@@",counter,":no data in Q_fft_input",my_ques.Q_FFT_input.qsize())
            pass
        if first_input_received:
            print('fft 1st input received')   
            try : 
                fft_in_dat.scope_dat.set_scope_dat(fft_in_dat.scope_delay,fft_in_dat.scope_scale,fft_in_dat.Nchirps)
                fft_dat,fftabs,fftmean,fftstd,fftmax,freq=fft_mod.grab_fft_main(fft_in_dat)
                fft_out_dat=q_cls.FFT_output_data()
                fft_out_dat.fft_graph.set_data(xdat=freq,ydat=fftmean,xlim=fft_in_dat.xlim,ylim=fft_in_dat.ylim,ylog=fft_in_dat.ylog)
                my_ques.Q_FFT_output.put(fft_out_dat)
            except:
                print ("Unexpected error:", sys.exc_info()[0])

                print('---fft didn''t receive input')

            

    # print("queue size after get",my_ques.Q_calib_input.qsize())
    

  

    return 

def sparta_threads():
    # define 6 queues Q_calib_input,Q_calib_output,Q_FFT_input,Q_FFT_output,Q_state_out,Q_state_fft
    ques = nmd('ques', 'Q_calib_input Q_calib_output Q_FFT_input Q_FFT_output Q_state_out Q_state_fft')
    Q_calib_input= Queue()
    Q_calib_output= Queue()
    Q_FFT_input= Queue()
    Q_FFT_output= Queue()
    Q_state_out= Queue()
    Q_state_fft= Queue()
    
    my_ques=ques(Q_calib_input,Q_calib_output,Q_FFT_input,Q_FFT_output,Q_state_out,Q_state_fft)
    # define 3 threads with access to the 6 queues (in the defining class open the queues), and the relevant top function

    GUI_Thread=MyThread(my_ques,main_GUI.main, args=(my_ques,))# get from Alla. this function should push the parameters defined in parameter list
    calib_thread=MyThread(my_ques,calib_fun,args=(0,))# 
    FFT_Thread=MyThread(my_ques,fft_fun, args=(0,)) 
    print("gui before start")
    time.sleep(1)
    GUI_Thread.start()# Alla:gather required parameters from GUI_Thread into Q_calib_input,  Q_FFT_input
    print("good night")

   #time.sleep(10)
    print("wakey wakey")
    q_empty=1
    counter=0
    # while q_empty:
    #     print('q still empty %d' % counter)
    #     time.sleep(4)
    #     q_empty=my_ques.Q_calib_input.qsize()==0
    #     if not q_empty:
    #         print('q is full')
    #         try:
    #             cal_in_dat = my_ques.Q_calib_input.get(False)
    #             print('received Q_calib_input')
    #             but_state=cal_in_dat.but_state
    #             but_sum = but_state.lin_but + but_state.cums_but + but_state.chip_but
    #             q_empty=0

    #         except:
    #             print("no data in Q_calib_input",my_ques.Q_calib_input.qsize())
    #             q_empty=1
    #             pass            
    #     # q_empty=1
    #     counter+=1

    calib_thread.start()  
    FFT_Thread.start()
    print('ending Sparta thread') 
    end_program=0
    while  not end_program:
        c = input("Type exit to quit")
        end_program = c=="exit"

    print('ending Sparta thread')  
    
        
   
    # every get operation from the queue should be defined as:
    
    
    

if __name__ == '__main__':
    ques = nmd('ques', 'Q_calib_input Q_calib_output Q_FFT_input Q_FFT_output Q_state_out Q_state_fft')
    Q_calib_input= Queue()
    Q_calib_output= Queue()
    Q_FFT_input= Queue()
    Q_FFT_output= Queue()
    Q_state_out= Queue()
    Q_state_fft= Queue()
    my_ques=ques(Q_calib_input,Q_calib_output,Q_FFT_input,Q_FFT_output,Q_state_out,Q_state_fft)
    # old_thread_try(my_ques)
    sparta_threads()
    # calib_fun(my_ques)
