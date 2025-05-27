import os,sys
sys.path.append(r'C:\Users\User\Documents\python3sv\PFE_Shutle\Automation_Optics\PyDAQmx\*')

from PyDAQmx import *

#from .DAQmxTypes import *
## Importing Legs###
## V1 05/03/2019

##  TEsts_PFE_Shuttle.py:
##             while (np.mean(CompOut) <= vth) and (i < 250):- Number of steps raised 25-->250
##                dac_init -= 0.00015 --> step is 150 uV
## Main_PFE_Shuttle
##  TestAutomation.pfell.RegInfo.Value.TIA_DRC1 = 512 TIA 5K-->512
# calibrate Vbias wherere the output is after the PRA
sys.path.append(r'C:\Users\User\Documents\python3sv\Equipment')
sys.path.append(r'C:\Users\User\Documents\python3sv')
import Equipment as MyEquip

from PFE_Shutle import access as MyAccess

import TESTS_PFE_SHUTTLE as MyTest
import numpy as np
from collections import OrderedDict

analog_input = Task()
read = int32()
data = numpy.zeros((1000,), dtype=numpy.float64)

# DAQmx Configure Code
analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
analog_input.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

# DAQmx Start Code
analog_input.StartTask()

# DAQmx Read Code
analog_input.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

#print "Acquired %d points"%read.value