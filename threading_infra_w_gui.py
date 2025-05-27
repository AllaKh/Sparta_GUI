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
from irad_stfftLinCalib import irad_stfftLinCalib as stft
sys.path.append('C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/tests') 
import flatutil as flut
sys.path.append('C:/Users/Oryx/Documents/python3sv/PFE_Shutle/Automation_Optics')
import MAIN_PFE_SHUTTLE as mpfe
import visa 
import SampleSigByClock as ssclk
import Main_flatCums as cums
from collections import namedtuple as nmd
import LinearizationCalc as lin_cal
import SetupandSampleFromScope as set_samp
import main_GUI



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

def lin_top(OldLut,fu):
    NumOfChirps=50
    SampledData,time_dat,fs = set_samp.main_grab(NumOfChirps)
#     str='C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/piezo_lut_0_10000.txt'
    str='C:/Users/Oryx/Desktop/piezo_lut_0_10000Linear.txt'
#     SampledData=np.loadtxt("this_dat.txt")
    # OldLut=np.loadtxt(str)
    target_freq=60e3
    n_inds_per_slice_vec=np.round(np.array( [400, 500, 600])/2000*np.shape(SampledData)[0]).astype(int)
    counter=0
    # n_inds_per_slice_vec=np.round(np.array( [300])/2000*np.shape(SampledData)[0]).astype(int)
    for cur_n_inds_per_slice in n_inds_per_slice_vec:
        newLUT=lin_cal.LinearizationCalc(OldLut,SampledData,target_freq,ChirpType=0,n_inds_per_slice=cur_n_inds_per_slice,UseScope=1)
        newLUT=newLUT.astype(int)
        plt.plot(newLUT)
        plt.show()
        fu.UpdatePiezo(newLUT)
        np.savetxt(str[:-4]+"_iter_%d" %counter+str[-4:], newLUT)
        print(str[:-4]+"_iter_%d" %counter+str[-4:])
        counter+=1
        if not(cur_n_inds_per_slice==n_inds_per_slice_vec[-1]):
            SampledData,time_dat,fs = set_samp.main_grab(NumOfChirps)

    return newLUT

def calib_fun(my_ques,args):
    naive_connect=1
    try:
        calib_input_data = my_ques.Q_calib_input.get(False)
        print('received Q_calib_input')
        #Opt 1: Handle task here and call q.task_done()
    except:
        #Handle empty queue here
        print("no data in Q_calib_input",my_ques.Q_calib_input.qsize())
        pass
    print("queue size after get",my_ques.Q_calib_input.qsize())
    
    OldLut=linearize.get_linearization_default(calib_input_data.lin_file_name)
    my_ques.Q_calib_output.put()
    # plt.plot(OldLut)
    # plt.show()
    
    fu = flut.FlatUtil(cur_IP,naive_connect)
    if not( naive_connect):
    
        fu.start()
        fu.UpdatePiezo(OldLut.astype(int))
        time.sleep(20)
        # print("1 update")
        # fu.UpdatePiezo(OldLut.astype(int))
        # print("2 update")

    for ind in np.arange(1):
        # if new_linearization:
        #     a='place holder'
        #     #### push linearization vector
        #     new_linearization=0
        try:
            task=ques.Q_calib_input.get(False)
            task[1]
            #Opt 1: Handle task here and call q.task_done()
        except:
          #Handle empty queue here
          pass
        NewLut=lin_top(OldLut,fu)
        # fu.UpdatePiezo(NewLut.astype(int))
    return NewLut

        

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
    FFT_Thread=MyThread(my_ques,len, args=(0,)) 
    print("gui before start")
    GUI_Thread.start()# Alla:gather required parameters from GUI_Thread into Q_calib_input,  Q_FFT_input
    print("good night")

    time.sleep(10)
    print("wakey wakey")
    q_empty=1
    while q_empty:
        print('q still empty')
        time.sleep(4)
        q_empty=my_ques.Q_calib_input.qsize()>0
        
    calib_thread.start()    

        
    # start calib_thread which will run the laser in MCT flattening mode. immidiately push the 1st lineariztion vector to protect piezo
    # inside calib thread send MCT and VCO graphs via Q_calib_output while making sure no response to buttons for 30 TBD seconds
    # calib thread should be initialized calling Main_flatCums_for_threading with pause_calibrate_flag=True (so cumsum flattening doesn't take over)
    # start FFT_Thread with relevant parameters from Q_FFT_input. data should be garbage.
    # inside calib thread:
    #   while 1:
    #       check the state of the Q_calib_input periodically and wait for a request to perform any calibration
    #       if linearization or chip calib: # state is [1,0,0] or [0,0,1]
    #           send FFT_Thread a "stop" via Q_state_fft 
    #           verify FFT is done by checking if Q_state_fft is empty 
    #           perform the relevant calibration with the acquired data (by calling the relevant function)
    #           when function finishes - send a notification in Q_state_out so GUI_thread can reset the button state to [0,0,0]
    #           when function finishes - send FFT_Thread a "start" via Q_state_fft can acquire data from the scope
    #       if cumsum flattening or pause flattening: [0,1,0] or [0,0,0]
    #           call Main_flatCums_for_threading with pause_calibrate_flag=false
    #           FFT will continue grabbing and analysing
    # inside FFT_thread:
    #   read start_state from Q_state_fft
    #   while start_state:
    #       get parameters from Q_FFT_input
    #       grab data from scope 
    #       analyse the data
    #       send analysed data to Q_FFT_output
    #       need to read start_state from Q_state_fft as the last action in this loop so no conflict with scope occurs
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
