import nidaqmx as nidaq
import numpy as np

t = nidaq.Task()
t.CreateAIVoltageChan('Dev1/ai0', None, nidaq.DAQmx_Val_Diff, 0, 10, nidaq.DAQmx_Val_Volts, None)
t.CfgSampClkTiming('', 2e6, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_FiniteSamps, 5000)
t.StartTask()

data = np.zeros((5000,), dtype=np.float64)
read = nidaq.int32()
t.ReadAnalogF64(5000, 5, nidaq.DAQmx_Val_GroupByChannel, data, len(data), nidaq.byref(read), None)