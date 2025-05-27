import os,sys

## Importing Legs###
sys.path.append(r'C:\Users\User\Documents\python3sv')
import Equipment as MyEquip

from PFE_Shutle import access as MyAccess
import numpy as np
import TESTS_PFE_SHUTTLE as MyTest

from collections import OrderedDict

class clsStruct():
    def __init__(self, **entries):
         self.__dict__.update(entries)


def main_power_on(configuration,pfe_num):

    TestAutomation = MyTest.PFE_SHUTTLE_TESTS(**configuration)

    TestAutomation.power_on_tests(pfe_num)


def main_debug(configuration,pfe_num):

    TestAutomation=MyTest.PFE_SHUTTLE_TESTS(**configuration)

    vth= 3.3/2
    source_data  = "CHANnel2"
    source_clock = "CHANnel3"

    #TestAutomation.BandwidthExaminationMDO(source_data=source_data,source_clock=source_clock)
    #TestAutomation.BandwidthExaminationDSO(source_data=source_data,source_clock=source_clock)
    TestAutomation.pfe_dynamic_calib_stability(pfe_num=3,vth=vth)




def main_flow_rev0(configuration,pfe_num,TIA=True,PRA=True,D2S=True,GM=True):


    TestAutomation=MyTest.PFE_SHUTTLE_TESTS(**configuration)

    vth=1.65

    if TIA:

        TIA_DRC1 = TestAutomation.pfe_tia_vp_calib(pfe_num,direction='up',save_data=True,filename="PFE_Calibration.xlsx",vth=vth)

        print("TIA vp cal value is:",TIA_DRC1)

        if pfe_num<2:

            TIA_DRC0 = TestAutomation.pfe_tia_vn_calib(pfe_num,direction='up',save_data=True,filename="PFE_Calibration.xlsx",vth=vth)

            print("TIA vn cal value is:", TIA_DRC0)

    if PRA:
        pra_dac_vp_list,pra_dac_vn_list,CalibStatus=TestAutomation.pfe_pra_calib(pfe_num,vp_vn_tia_cal=True,save_data=True,filename="PFE_Calibration.xlsx",vth=vth)


        print("PRA DAC  vp list", pra_dac_vp_list)

        print("PRA DAC  vn list", pra_dac_vn_list)

        if not CalibStatus:

            print("Calibration failed")


    if D2S:

        d2s_dac_vp, d2s_dac_vn=TestAutomation.pfe_d2s_calib(pfe_num,pra_cal=False,save_data=True, filename="PFE_Calibration.xlsx",vth=vth)

        print("D2S DAC vp", d2s_dac_vp)

        print("D2S DAC vn", d2s_dac_vn)

    if GM:

        gm_dac_vp, gm_dac_vn = TestAutomation.pfe_gm_dac_calib(pfe_num,d2s_calib=False, save_data=True, filename="PFE_Calibration.xlsx",vth=vth)

        print("GM DAC vp", gm_dac_vp)

        print("GM DAC vn", gm_dac_vn)



def main_flow_rev1(configuration,pfe_num,TIA=True,PRA=True,D2S=True,GM=True,Retry=False):


    TestAutomation=MyTest.PFE_SHUTTLE_TESTS(**configuration)

    vth = 0.5#1.65#0.5#1.65
    dac_init=0.05
    Dynamic_Calib = True



    print("\n\nSetting F1's TIA to 512")
    TestAutomation.pfell.RegInfo.Value.TIA_DRC1 = 512
    #TestAutomation.pfell.write(1)

    #TestAutomation.pfell.RegInfo = TestAutomation.pfell.RegInfo_Defaults.copy()
    #TestAutomation.pfell.RegInfo.Value.AMP_ATT = 2
    #print("Overriding AMP_ATT = %d" %(TestAutomation.pfell.RegInfo.Value.AMP_ATT))


    # print("Overriding D2S_DACP = 31")
    # print("Overriding D2S_DACN = 31")
    # TestAutomation.pfell.RegInfo.Value.D2S_DACP = 31
    # TestAutomation.pfell.RegInfo.Value.D2S_DACN = 31

    TestAutomation.pfell.write(1)

    TestAutomation.pfell.write(pfe_select=3)

    TestAutomation.pfell.RegInfo = TestAutomation.pfell.RegInfo_Defaults.copy()

    print("Default Settings Written")
    # self.override_defaults(pfe)

    print("Setting DAC Output Voltage to 0")
    #TestAutomation.pfell.fnSetDAC(DAC_V = 0)

    TestAutomation.pfell.fnSetDAC(Gain=TestAutomation.R2 / (TestAutomation.R1 + TestAutomation.R2), DAC_V=0)


    if TIA:

        TIA_DRC1 = TestAutomation.pfe_tia_vp_calib(pfe_num,direction='up',save_data=True,filename="PFE_Calibration.xlsx",vth=vth)

        print("TIA vp cal value is:",TIA_DRC1)

        if pfe_num<2:

            TIA_DRC0 = TestAutomation.pfe_tia_vn_calib(pfe_num,direction='up',save_data=True,filename="PFE_Calibration.xlsx",vth=vth)

            print("TIA vn cal value is:", TIA_DRC0)

    if PRA:
        pra_dac_vp_list,pra_dac_vn_list,CalibStatus=TestAutomation.pfe_pra_calib(pfe_num,vp_vn_tia_cal=True,save_data=True,filename="PFE_Calibration.xlsx",vth=vth,dac_init=dac_init,Retry=Retry)

        print("PRA DAC vp list", pra_dac_vp_list)

        print("PRA DAC vn list", pra_dac_vn_list)

        if not CalibStatus:

            print("Calibration failed")


    if D2S:

        d2s_dac_vp, d2s_dac_vn=TestAutomation.pfe_d2s_calib(pfe_num,pra_cal=False,save_data=True, filename="PFE_Calibration.xlsx",vth=vth)

        print("D2S DAC vp", d2s_dac_vp)

        print("D2S DAC vn", d2s_dac_vn)

    if GM:

        gm_dac_vp, gm_dac_vn = TestAutomation.pfe_gm_dac_calib(pfe_num,d2s_calib=False, save_data=True, filename="PFE_Calibration.xlsx",vth=vth)

        print("GM DAC vp", gm_dac_vp)

        print("GM DAC vn", gm_dac_vn)


    if Dynamic_Calib:

        CompOut, Stability_Table = TestAutomation.pfe_dynamic_calib_stability(pfe_num,vth=vth)
        print("CompOut Average (using port extender) : %f" %np.mean(CompOut))
        print("DC 'calibraton' error is: %.2f %%" % (abs(np.mean(Stability_Table) - vth) / vth * 100))
        #TestAutomation.get_pfe_dft_voltages(pfe_num, "AO2", 0.05)



        if abs(np.mean(Stability_Table) - vth) < 0.25*vth:
            return TestAutomation
        else:
            TestAutomation.pfell.PfeAccess.close_adap()
            return False

    # if Dynamic_Calib:
    #
    #     TestAutomation.pfe_dynamic_calib_stability(pfe_num, vth=vth)

        #CompOut, stability_table = TestAutomation.pfe_dynamic_calib_stability(pfe_num, vth=vth)

        #print("CompOut Average",sum(CompOut)/float(len(CompOut)))

        #print("Stablity Table", stability_table)

    #print("Connect DVM to AO2")
    #TestAutomation.get_pfe_dft_voltages(3, "AO2")
    #raw_input("Press Enter to continue...")


    #TestAutomation.BandwidthExamination()





def main(mode="debug",):

    pfe_num=3

    test_name='flow_1'

    Header=[u'BOARD_CONFIG', u'BOARD_ID', u'BOARD_INPUT_VOL', u'TEMP', u'TEC',
     u'BOARD_DAC_VBIAS', u'SIGNAL_INPUT', u'COMP_FREQ', u'FLAVOR', u'TIA_VP',
     u'TIA_VN', u'PRA_VP', u'PRA_VN', u'D2S_VP', u'D2S_VN', u'GM_VP',
     u'GM_VN ', u'TIME_STAMP', u'COMP_OUT']

    fpga_api_params = {"fpga_host": "10.99.0.155", "sessions_num": 1, "frames": 1,
                       "savefile": r'C:\Debug\fpga\td_data.csv'}
    #configuration = {"mode":mode,"equip": MyEquip, "access": MyAccess,"ProjectPath":r'Z:\projects\pfe_shuttle','TestsResultFile':'%s.xlsx'%test_name}
    #"GDM-8261A"

    configuration = {"mode": mode, "equip": MyEquip, "access": MyAccess,"USE_DMM":"34410A","YODA_mode":False,"fpga_api_params":fpga_api_params,
                     "ProjectPath":r'\\ORYXLAB\Sharedrive\projects\pfe_shuttle','TestsResultFile': '%s.xlsx' % test_name}




    if mode=="PowerOn":

        main_power_on(configuration,pfe_num)

    elif mode=="debug":

        main_debug(configuration,pfe_num)

    elif mode=="Flow_rev0":

        TIA = False
        PRA = True
        D2S = True
        GM = True

        main_flow_rev0(configuration,pfe_num,TIA=TIA,PRA=PRA,D2S=D2S,GM=GM)

    elif mode=="Flow_rev1":

        TIA = False
        PRA = True
        D2S = True#False#True
        GM = True

        TestAutomation = main_flow_rev1(configuration,pfe_num,TIA=TIA,PRA=PRA,D2S=D2S,GM=GM,Retry=True)



        if ((not TestAutomation) and isinstance(TestAutomation, (bool))):
            print("CompOut is more than 50% out")
            print("Retrying Calibration with comperator at D2S & GMLP")
            TestAutomation = main_calib_flow_rev1(configuration, pfe_num, TIA=TIA, PRA=PRA, D2S=D2S, GM=GM, Retry=True)

    elif mode == "Flow_YODA_rev2":


        TIA = False
        PRA = True
        D2S = True
        GM = True

        main_flow_yoda_rev2(configuration,pfe_num,TIA=TIA,PRA=PRA,D2S=D2S,GM=GM)


    else:

        main_debug(configuration,pfe_num)



if __name__ == '__main__':

    #mode='Flow_rev0'

    #mode='Flow_rev0'

    mode = 'Flow_rev1'

    #mode = 'PowerOn'

    #mode ="debug"

    main(mode)
