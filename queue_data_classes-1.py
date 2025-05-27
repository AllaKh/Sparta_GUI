import sys
import numpy as np
import cycle_marker 
import SetupFromScope as set_scope
# import numpy as np

mar='_'
class chip_dat():
    def __init__(self):
        self.Vbias=55e-3
        self.GM_DAC=7
        self.AMP_ATT=2
        self.scope_delay=700e-6
        self.scope_scale=100e-6
        self.file_name='C:\\Users\\user\\Documents\\projects\\pfe_shuttle\\Results\\PFE_Calibration.xlsx'
        self.sheet_name='PFE3_Calibration_GM'
        

class lin_dat():
    def __init__(self):
        self.chirp_type=0 #0 for up, 1 for down
        self.Nchirps=50
        self.Nchirps_to_average=5 
        self.iters=[3]# can be either number of iterations or a vector of slice lengths relative to 2000
        self.slice_ignore=[0,-2,-1]# slice numbers to ignore
        self.sub_pulse_times=[0]# can be either number of sub pulses or a vector of sub pulse start times
        self.target_freq=60e5
        self.scope_delay=700e-6
        self.scope_scale=100e-6
        self.first_correction_ind=200
        self.flatness_crit=0.6# the allowed middle percentile: signal is between -flatness_crit and flatness_crit if entire signal range is -1 to 1
        self.file_name='C:/Users/Oryx/Desktop/piezo_lut_0_10000Linear.txt'

class cums_dat():
    def __init__(self):
        self.by_D2S=[0]# can be either number of iterations or a vector of slice lengths relative to 2000
        self.V0=160# slice numbers to ignore
        self.Kd=0.1# can be either number of sub pulses or a vector of sub pulse start times
        self.Kp=1e-4
        self.Ki=0
        self.err_min=0.01
        self.smooth_win=11
        self.flat_window=0 #use cumulative sum over whole signal or over a moving window
        self.Fs=2e6 # sampling frequency of the Msignal (units of Hz). will be probably will be different in the real system
        self.Tos=222e-6 #100e-6; # the time delay between ignition and sampling (units of sec)

        self.file_name='C:/Users/Oryx/Documents/Python_Code/flat_by_cums_folder/24_Jun_2019_08_27_49test840_kd0.1_kp0.0001_flt1951.txt'

class but_state():
    def __init__(self):
        self.lin_but=0
        self.cums_but=0
        self.chip_but=0

class scope_dat():
    def __init__(self,scope_IP,scope_delay,scope_scale):
        self.Chan1Offset="1.2" #1.3v
        self.TrigCh1="2.0" #V
        self.Chan1Scale="1.0" #V
        self.Chan4Offset="0.11" #v
        self.TrigCh4="2.0" #V
        self.Chan4Scale="0.05" #V
        self.ScopeAdress = scope_IP
        self.TScale="{:.9f}".format(scope_scale) #  sec
        self.TOffset="{:.9f}".format(scope_delay) #sec
        self.num_of_chirps=50
        self.scope_handle=set_scope.main_set(self)
    
    def set_scope_dat(self,scope_delay,scope_scale,num_of_chirps=50):
        self.Chan1Offset="1.2" #1.3v
        self.TrigCh1="2.0" #V
        self.Chan1Scale="1.0" #V
        self.Chan4Offset="0.11" #v
        self.TrigCh4="2.0" #V
        self.Chan4Scale="0.05" #V
        self.TScale="{:.9f}".format(scope_scale) #  sec
        self.TOffset="{:.9f}".format(scope_delay) #sec
        self.num_of_chirps=num_of_chirps

        self.scope_handle=set_scope.main_set(self)


class calib_input_data():
    def __init__(self):
        self.scope_IP="TCPIP0::10.99.0.18::inst0::INSTR"
        self.sparta_IP='10.99.0.127'
        self.naive_connect=0
        self.chip_dat=chip_dat()
        self.lin_dat=lin_dat()
        self.cums_dat=cums_dat()
        self.but_state=but_state()
        self.scope_dat=scope_dat(self.scope_IP,self.chip_dat.scope_delay,self.chip_dat.scope_scale)# verify that the values don't change unexpectedly


class graph_data():
    def __init__(self,xdat=[0],ydat=np.array([3,6]),xlim=[0],ylim=[0],ylog=0,title=''):
        global mar
        self.xdat = xdat if len(xdat)>1 else np.arange(np.size(ydat))
        self.ydat = ydat
        self.xlim = xlim if len(xlim)>1 else np.array([np.amin(xdat),np.amax(xdat)])
        self.ylim = ylim if len(ylim)>1 else np.array([np.amin(ydat),np.amax(ydat)])
        self.ylog = ylog
        self.title = title
        mar=cycle_marker.cycle_marker(mar)
        line_spec='-'+mar
        self.line_spec=line_spec

    def set_data(self,xdat=[0],ydat=np.array([3,6]),xlim=[0],ylim=[0],ylog=0,title=''):
        global mar
        self.xdat = xdat if len(xdat)>1 else np.arange(np.size(ydat))
        self.ydat = ydat
        self.xlim = xlim if len(xlim)>1 else np.array([np.amin(xdat),np.amax(xdat)])
        self.ylim = ylim if len(ylim)>1 else np.array([np.amin(ydat),np.amax(ydat)])
        self.ylog = ylog     
        self.title = title
        mar=cycle_marker.cycle_marker(mar)
        line_spec='-'+mar
        self.line_spec=line_spec

        
class calib_output_data():
    def __init__(self):
        self.message='system off'
        self.lin_graph = graph_data()
        self.cums_graph = graph_data()
        self.vco_graph = graph_data()
        self.oneBit_graph = graph_data()

# define 6 queues Q_calib_input,Q_calib_output,Q_FFT_input,Q_FFT_output,Q_state_out,Q_state_fft
class FFT_input_data():
    def __init__(self):
        self.xlim =  np.array([1,1e6])
        self.ylim =  np.array([1,10])
        self.ylog = 1
        self.Nchirps = 10
        self.analysis_type = 1#0 mean; 1 std; 2 max; 3 min
        self.noise_freqs = np.array([70e5,80e5])
        self.peak_freqs = np.array([55e5,65e5])
        self.save_path = ""
        self.camera_cursor_pos = [600,600]
        self.scope_delay=700e-6
        self.scope_scale=100e-6
        self.scope_dat=scope_dat(self.scope_delay,self.scope_scale)
        self.save_name="***"

class FFT_output_data():
    def __init__(self):
        self.fft_graph = graph_data()
        self.time_graph = graph_data()

class state_data():
    def __init__(self):
        self.busy=0

# class state_fft_data():
#     def __init__(self):
#         self.release=0

if __name__ == "__main__":
    my_dat=calib_input_data()
    out_dat=calib_output_data()
    a=1 
    b=5
    c= (not a>0) & (not b>0) 
    # print(c)
    # gg=graph_data()
    print(my_dat)
    print("hi")
    pass