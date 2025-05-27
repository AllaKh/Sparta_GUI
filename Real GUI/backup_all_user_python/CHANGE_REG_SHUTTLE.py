import os, sys


## Importing Legs###
## V1 05/03/2019

##  TEsts_PFE_Shuttle.py:
##             while (np.mean(CompOut) <= vth) and (i < 250):- Number of steps raised 25-->250
##                dac_init -= 0.00015 --> step is 150 uV
## Main_PFE_Shuttle
##  TestAutomation.pfell.RegInfo.Value.TIA_DRC1 = 512 TIA 5K-->512
# calibrate Vbias wherere the output is after the PRA
#sys.path.append(r'C:\Users\User\Documents\python3sv\Equipment')
sys.path.append(r'C:/Users/Oryx/Documents/python3sv')
import Equipment as MyEquip

from PFE_Shutle import access as MyAccess

import TESTS_PFE_SHUTTLE as MyTest
import numpy as np
from collections import OrderedDict

class clsStruct():
    def __init__(self, **entries):
         self.__dict__.update(entries)


# def main_power_on(configuration,pfe_num):

#     TestAutomation = MyTest.PFE_SHUTTLE_TESTS(**configuration)

#     TestAutomation.power_on_tests(pfe_num)


# def main_debug(configuration,pfe_num):


#     TestAutomation = MyTest.PFE_SHUTTLE_TESTS(**configuration)

#     TestAutomation.BandwidthFPGATest()
#     #TestAutomation.NoiseExaminationFPGA()





def set_register_flow(configuration, pfe_num, reg_val_pair, Retry=False):

    print(configuration)
    TestAutomation=MyTest.PFE_SHUTTLE_TESTS(**configuration)
    print(f'REF_SEL0 = {TestAutomation.pfell.RegInfo.Value.REF_SEL0} , REF_SEL1 = {TestAutomation.pfell.RegInfo.Value.REF_SEL1}, REF_SEL_lh = {TestAutomation.pfell.RegInfo.Value.REF_SEL_lh}')
    Dynamic_Calib=False

    #TestAutomation.BandwidthExaminationFPGA()

    vth=1.65#1.03#1.65#0.5 # 3.3/2
    dac_init =reg_val_pair[0][1] #VBais in Volts
    reg_val_pair=reg_val_pair[1:]
    Gain = TestAutomation.R2 / (TestAutomation.R1 + TestAutomation.R2)

    dac_N = TestAutomation.pfell.fnSetDAC(Gain=Gain, DAC_V=dac_init)

    TestAutomation.pfell.RegInfo.Value.TIA_DRC1 = 512
    #TestAutomation.pfell.RegInfo.Value.DFT_Rsns = 1 #ONLY FOR BRD 2
    TestAutomation.pfell.write(1) #Send to PFE#1
    TestAutomation.pfell.write_defaults(3)
    TestAutomation.pfell.RegInfo = TestAutomation.pfell.RegInfo_Defaults.copy()

    # stam=True
    # set_d2s=True
    # while(stam):
    for new_register,new_value in reg_val_pair:
        TestAutomation.printRegInfo(TestAutomation.pfell.RegInfo)

        print(f'REF_SEL0 = {TestAutomation.pfell.RegInfo.Value.REF_SEL0} , REF_SEL1 = {TestAutomation.pfell.RegInfo.Value.REF_SEL1}, REF_SEL_lh = {TestAutomation.pfell.RegInfo.Value.REF_SEL_lh}')
        print(f'Current value of GM_DACA = {TestAutomation.pfell.RegInfo.Value.GM_DACA}')

        # value=input("Enter new value for GM_DACA:")
        # TestAutomation.pfell.RegInfo.Value.GM_DACA = int(value) # Barak write params to shuttle 
        # TestAutomation.pfell.write(3)
        #print('Continue Loop = {TestAutomation.pfell.RegInfo.Value.GM_DACA}')
        # value = input("Continue loop? (1/0)")
        # stam= value=='1'
        # if stam:
        # new_register=input("Enter new register to change:")
        # new_value=input("Enter new register value:")
        print('TestAutomation.pfell.RegInfo.Value.'+new_register+' = '+new_value)
        exec('TestAutomation.pfell.RegInfo.Value.'+new_register+' = '+new_value)
        TestAutomation.pfell.write(3)
        print('written')
        # set_d2s_in=input("Press Enter for analog output? (1/0)")  # ATurn on nalog output of the Amplifier
        # set_d2s= set_d2s_in=='1'
        # if set_d2s:
        #     TestAutomation.get_d2s_ana_with_cmp(pfe_num=3, enable=True)
    TestAutomation.pfell.PfeAccess.close_adap()
    # input("press enter to quit")


def main(mode="Set_register",reg_val_pair=[('dac_init',55e-3),('CMPIN_SEL','1')]):

    pfe_num=3

    test_name='flow_1'

    Header=[u'BOARD_CONFIG', u'BOARD_ID', u'BOARD_INPUT_VOL', u'TEMP', u'TEC',
     u'BOARD_DAC_VBIAS', u'SIGNAL_INPUT', u'COMP_FREQ', u'FLAVOR', u'TIA_VP',
     u'TIA_VN', u'PRA_VP', u'PRA_VN', u'D2S_VP', u'D2S_VN', u'GM_VP',
     u'GM_VN ', u'TIME_STAMP', u'COMP_OUT']

    fpga_api_params = {"fpga_host": "10.99.0.167", "sessions_num": 1, "frames": 1,
                       "savefile": r'D:\sharedrive\projects\pfe_shuttle\Results\Debug\fpga_td_data.csv'}


    #configuration = {"mode":mode,"equip": MyEquip, "access": MyAccess,"ProjectPath":r'Z:\projects\pfe_shuttle','TestsResultFile':'%s.xlsx'%test_name}
    #"GDM-8261A"
    configuration = {"mode": mode, "equip": MyEquip, "access": MyAccess,"USE_DMM":"GDM-8261A","YODA_mode":False,"fpga_api_params":fpga_api_params,
                     "ProjectPath":r'C:\Users\User\Documents\projects\pfe_shuttle','TestsResultFile': '%s.xlsx' % test_name,"reg_sheet_name":'PFE3_Calibration_GM'}

    if mode == "Set_register":


        TestAutomation = set_register_flow(configuration, pfe_num, reg_val_pair,Retry=False)

  

if __name__ == '__main__':

    #mode='Flow_rev0'

    #mode='Flow_rev0'
    #mode = 'Flow_rev1'

    mode = 'Set_register'

    #mode = 'PowerOn'
    #mode="debug"
    reg_val_pair=[('dac_init',48.9e-3),('CMPIN_SEL','1')]
    main(mode,reg_val_pair)
