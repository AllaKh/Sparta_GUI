import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
with nidaqmx.Task() as task:
   
    a=task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    

   # c=task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
    task.timing.cfg_samp_clk_timing(2e6)
    #task.ai_channels.cfg_samp_clk_timing(2e6,'rising_edge_chan','FINITE = 10178',40000)
    task.timing.samp_quant_samp_per_chan=200000 # Single Chirp
    task.triggers.start_trigger.disable_start_trig=False
    task.triggers.start_trigger.anlg_win_dig_sync_enable=True
    task.triggers.start_trigger.dig_edge_dig_sync_enable=True
    #bg=task.triggers.start_trigger.cfg_dig_pattern_start_trig
    #g=nidaqmx.constants
    task.triggers.start_trigger.trig_type = nidaqmx.constants.TriggerType.DIGITAL_EDGE
    b=task.read(number_of_samples_per_channel=4000)
    myarray = np.asarray(b)
    plt.plot(b)
    plt.show()
    #plt.plot(b[1])
    #plt.show()
    #print(b) 
    
