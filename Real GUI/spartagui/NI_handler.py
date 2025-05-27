import nidaqmx
import numpy as np
import matplotlib.pyplot as plt

def sample_ni (anlg_ch=["Dev1/ai0"],trig_ch=["Dev1/PFI0"],clk_timing=2e6,samp_per_chan=200000,nsamp_per_ch=4000,NumOfChirps=2,plt_flag=0) :  
    with nidaqmx.Task() as task:
        a=task.ai_channels.add_ai_voltage_chan(anlg_ch[0])
        # c=task.di_channels.add_di_chan(trig_ch[0])
        task.timing.cfg_samp_clk_timing(2e6)
        #task.ai_channels.cfg_samp_clk_timing(2e6,'rising_edge_chan','FINITE = 10178',40000)
        task.timing.samp_quant_samp_per_chan=samp_per_chan # Single Chirp
        task.triggers.start_trigger.disable_start_trig=False
        task.triggers.start_trigger.anlg_win_dig_sync_enable=True
        task.triggers.start_trigger.dig_edge_dig_sync_enable=True
        #bg=task.triggers.start_trigger.cfg_dig_pattern_start_trig
        #g=nidaqmx.constants
        task.triggers.start_trigger.trig_type = nidaqmx.constants.TriggerType.DIGITAL_EDGE
        
        #  SensorData=np.zeros([NumOfChirps,nsamp_per_ch], dtype=int)
        SensorData=np.array( [] )
        for i in range( NumOfChirps):
            b=task.read(number_of_samples_per_channel=nsamp_per_ch)
            #nlg_out = np.asarray(b)
            #SensorData[i,]=np.asarray(b)
            if np.size(SensorData) ==0: ########################################
                SensorData=b
            else:
                SensorData=np.vstack ((SensorData,b) )      
    print(np.shape(SensorData))
    if plt_flag:
        plt.plot(b)
        plt.show()
        #plt.plot(b[1])
        #plt.show()
        #print(b) 
    return SensorData
if __name__ == "__main__":
    sample_ni (anlg_ch=["Dev1/ai0"],trig_ch=["Dev1/PFI0"],clk_timing=2e6,samp_per_chan=200000,nsamp_per_ch=4000,NumOfChirps=2,plt_flag=1) 

