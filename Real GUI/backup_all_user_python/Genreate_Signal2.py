import os,sys
import numpy as np
import matplotlib.pyplot as plt
#from PFE_Shutle import pfe_shuttle_ll as ll
#from Services import IOFile
#from Services.sparta_app.tests import api_fpga_pc
#from Tools import filtering
#from Tools import pfe_shuttle_analysis as analysis
#import time
##\import datetime
import sys
import visa
import csv
## Define VISA Resource Manager & Install directory
## This directory will need to be changed if VISA was installed somewhere else.
#rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # this uses pyvisa
## This is more or less ok too: rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
## In fact, it is generally not needed to call it explicitly
## rm = visa.ResourceManager()
#from Equipment import Agilent_34410A_DMM
#from Equipment import GWINSTEK_GDM8261A_DMM
from Equipment import Agilent_DSO_X_2024A
#from Equipment import Tektronix_4104C_MDO

DSO_X_3034T = Agilent_DSO_X_2024A.clsAgilent_DSO_X_2024A(ControllerID="0", ConnecationType="LAN", Address='10.99.0.18')
DSO_X_3034T.write(':SINGle')


