import os,sys
import numpy as np
import matplotlib.pyplot as plt
from PFE_Shutle import pfe_shuttle_ll as ll
from Services import IOFile
import time
import pdb

from Equipment import Agilent_34410A_DMM
from Equipment import GWINSTEK_GDM8261A_DMM
from Equipment import Agilent_DSO_X_2024A
from Equipment import Tektronix_4104C_MDO
import io
StringIO=io.StringIO
from Tools import pfe_shuttle_analysis as analysis

from Services.sparta_app.tests import api_fpga_pc


_debug=False
_debug1=False


class clsStruct():
    def __init__(self, **entries):
         self.__dict__.update(entries)
    def append(self, update):
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        for i in range(len(members)):
            getattr(self, members[i]).append(getattr(update, members[i])[0])


class PFE_SHUTTLE_TESTS():

    def __init__(self,**kwargs):

        print("Setting the following Attributes")
        print(kwargs.keys())
        for key,value in kwargs.items():
            setattr(self,key,value)

        if self.USE_DMM == "34410A":
            try:
                self.dmm11 = Agilent_34410A_DMM.clsAgilent34410A_DMM(ControllerID="0", ConnecationType="LAN", Address='10.99.10.200')
            except:
                pass
        else:
            try:
                self.dmm11 = GWINSTEK_GDM8261A_DMM.cls_GDM_8261A(ControllerID="0", ConnecationType="GPIB", Address='5')
            except:
                pass

        try:
            #self.DSO1 = Agilent_DSO_X_2024A.clsAgilent_DSO_X_2024A(ControllerID="0", ConnecationType="LAN", Address='10.0.0.11')
            self.DSO1 = Agilent_DSO_X_2024A.clsAgilent_DSO_X_2024A(ControllerID="0", ConnecationType="LAN", Address='10.99.0.163')
            #self.DSO1 = Agilent_DSO_X_2024A.clsAgilent_DSO_X_2024A(ControllerID="0", ConnecationType="LAN",Address='10.99.10.222')
            #self.DSO1.fnGetWaveform()
        except:
            pass

        try:
            #self.MDO1 = Tektronix_4104C_MDO.clsTektronix_4104C_MDO(ControllerID="0", ConnecationType="LAN",Address="10.99.0.162")
            self.MDO1 = Tektronix_4104C_MDO.clsTektronix_4104C_MDO(ControllerID="0", ConnecationType="LAN",Address="10.99.0.162")

        except:
            raise


        #self.DSO1.fnGetScopeDataBytes(source="CH1")

        #self.DSO1.fnGetScopeDataAscii(source="CH1")

        #ch1=self.getCompOut(Input="Scope_MDO",source="CH1",filename=r"F:\pfe_data.csv")
        #ch2=self.getCompOut(Input="Scope_MDO",source="CH2",filename=r"F:\pfe_data.csv")

        self.R1 = 33.2
        self.R2 = 3

        #self.CompInput = "Scope_DSO"

        #self.CompInput = "Scope_DSO_PP"
        self.CompInput = "PortExtender"
        #self.CompInput = "FPGA"
        #self.CompInput = "DMM"


        #self.CompInput = "Scope_MDO"

        ## Don't change if not necessary
        self.ResultsFolder="Results"
        self.ConfigurationFolder="Configurations"

        #self.ResultsPath = r'Z:\projects\pfe_shuttle\Results'

        self.results_sheet_name = "Sheet1"

        self.ResultsFilename = "pfe_shuttle.xlsx"  # consider to provide it from config file

        self.timestamp = IOFile.pd.Timestamp.now()

        self.ResultPath=os.path.join(self.ProjectPath,self.ResultsFolder)

        ##Set Path and sheetname for Results regression file
        self.ExcelFileHandler=IOFile.ExcelHandler()



        ##Creating Results  Regression File pandas object
        try:

            if not os.path.exists(self.ResultPath):
                os.makedirs(self.ResultPath)
            else:
                if not os.path.isfile(os.path.join(self.ResultPath,self.ResultsFilename)):
                    print("Results file not exist- Creating Results.xlsx file @ Result path provided ")
                    self.ExcelFileHandler.CreateEmptyFile(os.path.join(self.ResultPath,self.ResultsFilename),self.results_sheet_name,save_now=True)
            self.ResultsFile_dict=self.ExcelFileHandler.ReadFromExistedFile(RegPath=os.path.join(self.ResultPath,self.ResultsFilename),sheet_name=self.results_sheet_name)

        except IOError:
            raise

        ##init aadvark device
        try:
            self.handler=self.pfell.PfeAccess.init_device()
        except:
            pass
        ## Bringing the register access object
        #r'D:\sharedrive\projects\pfe_shuttle\Configurations\PFE_Defaults.xlsx'
        self.pfell = ll.PFE_Low_Level(os.path.join(self.ProjectPath,self.ConfigurationFolder,"PFE_Defaults.xlsx"))  # optional params --> RegPath = r'./PFE3_Defaults.xlsx' ; sheet_name = 'PFE3_Defaults'


    def override_defaults(self,pfe):

        self.pfell.RegInfo.at['GM_DACA', 'Value'] = 4

        self.pfell.RegInfo.at['AMP_ATT', 'Value'] = 1
        #self.pfell.RegInfo.at['AMP_ATT', 'Value'] = 2

        self.pfell.RegInfo.at['REF_SEL_lh', 'Value'] = 0

        self.pfell.write(pfe)

    def getCompOut(self,source="CHANnel1",source_clock="CHANnel3",filename="E:\calib_data.csv",iters=1,pfe_num=3,vth=3.15):

        """
        Reading the comprator output
        :return:

        """
        Input=self.CompInput

        if Input=="PortExtender":
            CompOut=np.zeros(2000)
            for i in range(2):
                CompOut_temp=np.array([self.pfell.getCompOut_PE(pfe_num) for i in range(2000)])
                CompOut = CompOut + CompOut_temp


            # for i in range(10000):
            #     CompOut.append(self.pfell.getCompOut_PE(pfe_num)
            return(CompOut/2)

        elif Input=="Logic_MDO":
            # clock=self.mdo4104C.fnSaveWF("D8")

            data = self.MDO1.fnGetLogicData(source,filename)
            tempfile=os.path.join('Z:\sharedrive\projects\pfe_shuttle\Results','compout_temp.txt')
            try:
                with open(tempfile,'w') as outfile:
                    outfile.write(data)
            except:
                pass
            df=IOFile.pd.read_csv(tempfile,skiprows=2)

            return(df[' Data'])

        elif Input == "Scope_MDO":

            data_temp=self.MDO1.fnGetScopeData(source,filename)

            data = StringIO(data_temp)

            df=IOFile.pd.read_csv(data, skiprows=20)

            return (df[source])

        elif Input=="Scope_DSO_PP":
            #CompOut=None
            CompOut = []
            AcquireSeq = "Single"
            #for i in range(iters):
            i = 0
            while(i < iters):
                time.sleep(0.5)
            #while CompOut is None:
                try:
                    self.DSO1.fnSetAcquireStopRunSingle(AcquireSeq)
                    CompOut.append(float(self.DSO1.fnGetAVerageOutput(source)))
                    i += 1

                except:

                    print("Connection Lost--> Reinitializing")
                    time.sleep(0.5)
                    #pdb.set_trace()
                    #self.DSO1 = Agilent_DSO_X_2024A.clsAgilent_DSO_X_2024A(ControllerID="0", ConnecationType="LAN",Address='10.0.0.11')
                    self.DSO1 = Agilent_DSO_X_2024A.clsAgilent_DSO_X_2024A(ControllerID="0", ConnecationType="LAN",Address='10.99.0.163')
                    self.DSO1.fnSetAcquireStopRunSingle(AcquireSeq)
                    CompOut.append(float(self.DSO1.fnGetAVerageOutput(source)))
                    #self.DSO1.fnGetAVerageOutput(source)
                    #CompOut=float(CompOut)

            #CompOut = float(CompOut)

            AcquireSeq="RUN"
            #
            self.DSO1.fnSetAcquireStopRunSingle(AcquireSeq)


            return(np.mean(vth-np.array(CompOut)))


        elif Input=="Scope_DSO":

            df=IOFile.pd.DataFrame()

            AcquireSeq = "Single"

            self.DSO1.fnSetAcquireStopRunSingle(AcquireSeq)

            data_temp1 = self.DSO1.fnGetScopeDataAscii(source='CHANnel2')

            df["data"] =data_temp1

            data_temp2 = self.DSO1.fnGetScopeDataAscii(source='CHANnel3')

            AcquireSeq="RUN"

            self.DSO1.fnSetAcquireStopRunSingle(AcquireSeq)

            df["clock"] = data_temp2

            CompOut = analysis.ExtractDataFromScopeDSO(df)

            df["CompOut"]=CompOut

            return(df)


        elif Input=="DMM":
            df = IOFile.pd.DataFrame()
            data=[]
            for i in range(iters):
                time.sleep(0.5)
                data.append(float(self.dmm11.fnGetVoltage()))

            df[' Data']=data
            return (df[' Data'])

        elif Input=="FPGA":

            api_fpga_pc._debug=False

            fpga_host = self.fpga_api_params["fpga_host"]

            sessions_num = self.fpga_api_params["sessions_num"]

            frames = self.fpga_api_params["frames"]

            savefile = self.fpga_api_params["savefile"]

            df=api_fpga_pc.rpc_client(fpga_host,sessions_num,frames,savefile,pixel=299)

            data=np.array([])

            for i in range(0,frames):

                data=np.append(data,df["TD_Frame%d"%i].values)

            #df[' Data']=data

            #return (df[' Data'])

            return(data)

    def printRegInfo(self, RegInfo):
        print("Register Status: [TIA_DRC1, TIA_DRC0, PRA_DACP, PRA_DACN, D2S_DACP, D2S_DACN, GM_DACP, GM_DACN]")
        print("                     %d        %d      %d        %d        %d         %d        %d       %d" %(RegInfo.Value.TIA_DRC1, RegInfo.Value.TIA_DRC0, RegInfo.Value.PRA_DACP, RegInfo.Value.PRA_DACN,        RegInfo.Value.D2S_DACP, RegInfo.Value.D2S_DACN, RegInfo.Value.GM_DACP, RegInfo.Value.GM_DACN))

    #region Old Stuff
    def power_on_tests0(self,pfe_num):

        write_ok = self.pfell.write_defaults(pfe_num)
        print(write_ok)

        self.pfe_tia_vn_calib(pfe=pfe_num,save_data=False)
        self.pfe_tia_vp_calib(pfe=pfe_num,save_data=False)

        self.pfe_pra_calib(pfe=pfe_num,save_data=False)

    def power_on_tests1(self,pfe_num):

        write_ok = self.pfell.write_defaults(pfe_num)
        print(write_ok)

        self.pfe_tia_vn_calib(pfe=pfe_num,save_data=False)
        self.pfe_tia_vp_calib(pfe=pfe_num,save_data=False)

        self.pfe_pra_calib(pfe=pfe_num,save_data=False)

    def power_on_tests2(self,pfe_num):

        write_ok = self.pfell.write_defaults(pfe_num)


        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 2
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        #self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1

        write_ok = self.pfell.write(pfe_num)


        self.pfell.fnDFT_vp(pfe_num)
        time.sleep(0.1)
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (vp) is: %.3f" %float(self.dmm11.fnGetVoltage()))

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_vn(pfe_num)
        time.sleep(0.1)
        print("Voltage on AI1 (vn) is: %.3f" % float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 2
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_prap(pfe_num)
        time.sleep(0.1)
        v_prap = float(self.dmm11.fnGetVoltage());
        print("Voltage on AI1 (prap) is: %.3f" %v_prap)

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_pran(pfe_num)
        time.sleep(0.1)
        v_pran = float(self.dmm11.fnGetVoltage());
        print("Voltage on AI1 (pran) is: %.3f" %v_pran)
        print("prap - pran = %.1f" %((v_prap-v_pran)*1000) + " mV")
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 2
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_D2S_OUT(pfe_num)

        print("Voltage on AI1 (D2S Out) is: %.3f" % float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_GM_LP(pfe_num)

        print("Voltage on AI1 (GM LP) is: %.3f" %float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 2
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_sen_sensor(pfe_num)

        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (V Sensor) is: %.3f" % float(self.dmm11.fnGetVoltage()))

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 2
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_sen_Vnb(pfe_num)

        print("Voltage on AI1 (V Sensor VNB) is: %.3f" % float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_REF_OUT(pfe_num)

        print("Voltage on AI1 (VREF) is: %.3f" % float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_DAC_THRU_N_MUX(pfe_num)

        print("Voltage on AI1 (DFT DAC) is: %.3f" % float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_vbn(pfe_num)

        print("Voltage on AI1 (VBN) is: %.3f" % float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 2

        self.pfell.fnDFT_DAC_AUX_THRU_N_MUX(pfe_num)

        print("Voltage on AI1 (Beta Multiplier) is: %.3f" % float(self.dmm11.fnGetVoltage()))
        print("-----------------------------------------------------------------")

        write_ok = self.pfell.write_defaults(pfe_num)
    #endregion



    def get_register_sweep_range(self, register):
        if register == "TIA_DRC1":
            bits = self.pfell.RegInfo.loc[register].Bits
            r = list(2**np.array(range(bits)))
        elif register == "TIA_DRC0":
            bits = self.pfell.RegInfo.loc[register].Bits
            r1 = (2 ** np.array(range(bits)))
            r2 = 3*r1
            r = sum(zip(r1,r2,()))
        else:
            bits = self.pfell.RegInfo.loc[register].Bits
            r = range(1,2**bits)
        return r

    def sweep_register(self,pfe_num, register, tp="AI1"):
        initial_config = self.pfell.RegInfo.copy()
        sweep_range = self.get_register_sweep_range(register)
        for i in range(len(sweep_range)):
            self.pfell.RegInfo.loc[register].Value = sweep_range[i]
            self.pfell.write(pfe_num)
            if i == 0:
                voltages = self.get_pfe_dft_voltages(pfe_num, tp, 0.001)
            else:
                voltages.append(self.get_pfe_dft_voltages(pfe_num, tp, 0.001))

        self.pfell.RegInfo = initial_config.copy()
        return voltages, sweep_range


    def power_on_tests(self,pfe_num):

        write_ok = self.pfell.write_defaults(pfe_num)

        ##self.getCompOut()

        dac = self.pfell.DacAccess
        self.get_pfe_dft_voltages(pfe_num)
        R1 = 33.2
        R2 = 3
        Gain = (R1+R2)/R2
        # dac_N = int(dac.volt_to_dac(0.10, 2.048) * Gain)
        # dac.DAC_Update(0, dac_N)
        # self.pfell.RegInfo.Value.TIA_DRC1 = 64
        # self.pfell.RegInfo.Value.TIA_DRC0 = 4096
        # self.pfell.RegInfo.Value.PRA_DACP = 1
        # self.pfell.RegInfo.Value.PRA_DACN = 63
        # self.pfell.RegInfo.Value.GM_DACA = 1
        # self.pfell.write(1)

        dac_N = int(dac.volt_to_dac(0.11, 2.048) * Gain)
        dac.DAC_Update(0, dac_N)
        self.pfell.RegInfo.Value.TIA_DRC1 = 64
        self.pfell.RegInfo.Value.PRA_DACP = 60
        self.pfell.RegInfo.Value.PRA_DACN = 4
        self.pfell.RegInfo.Value.GM_DACP = 16
        self.pfell.RegInfo.Value.GM_DACN = 16
        self.pfell.RegInfo.Value.GM_DACA = 4
        self.pfell.RegInfo.Value.D2S_HGb = 1
        self.pfell.write(1)
        self.get_pfe_dft_voltages(3, "AO2", 0.01)

        voltages, sweep_range = self.sweep_register(3,"TIA_DRC1","AO1")

        plt.subplot(3,2,1)
        plt.plot(sweep_range, voltages.v_p)
        plt.xlabel("TIA_DRC1")
        plt.ylabel("Voltage [v]")
        plt.title("vp")
        plt.grid()

        plt.subplot(3, 2, 2)
        plt.plot(sweep_range, voltages.v_n)
        plt.xlabel("TIA_DRC1")
        plt.ylabel("Voltage [v]")
        plt.title("vn")
        plt.grid()

        plt.subplot(3, 2, 3)
        plt.plot(sweep_range, voltages.v_prap)
        plt.xlabel("TIA_DRC1")
        plt.ylabel("Voltage [v]")
        plt.title("vprap")
        plt.grid()

        plt.subplot(3, 2, 4)
        plt.plot(sweep_range, voltages.v_pran)
        plt.xlabel("TIA_DRC1")
        plt.ylabel("Voltage [v]")
        plt.title("vpran")
        plt.grid()

        plt.subplot(3, 2, 5)
        plt.plot(sweep_range, voltages.v_d2s)
        plt.xlabel("TIA_DRC1")
        plt.ylabel("Voltage [v]")
        plt.title("vD2S")
        plt.grid()

        plt.subplot(3, 2, 6)
        plt.plot(sweep_range, voltages.v_gm_lp)
        plt.xlabel("TIA_DRC1")
        plt.ylabel("Voltage [v]")
        plt.title("vGMLP")
        plt.grid()

        plt.show()

        print("Power On Tests Done")

        #self.d2s_vs_dac(pfe_num)
        #self.vp_vs_dac(pfe_num)

        #self.pfell.RegInfo.Value.DFT_clk_out = 1
        #self.pfell.write(3)

    def d2s_vs_dac(self, pfe_num):

        #write_ok = self.pfell.write_defaults(pfe_num)
        #self.pfell.RegInfo.Value.DFT_AI1_EN_passgate = 1
        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 0
        self.pfell.RegInfo.Value.DFT_ANALOG_SEL = 0

        self.pfell.RegInfo.Value.DFT_en_tiapn = 1
        self.pfell.RegInfo.Value.SEL_dac_vbp = 0
        self.pfell.RegInfo.Value.DFT_SELN = 3
        self.pfell.RegInfo.Value.DFT_SELP = 1
        self.pfell.RegInfo.Value.CMPIN_SEL = 1
        self.pfell.RegInfo.Value.CMPIN_EN = 1
        self.pfell.RegInfo.Value.CMPIP_EN = 1
        self.pfell.RegInfo.Value.CMPIP_SEL = 0
        self.pfell.write(pfe_num)

    def vp_vs_dac(self, pfe_num):

        write_ok = self.pfell.write_defaults(pfe_num)

        self.pfell.RegInfo.Value.DFT_ANALOG_EN = 0

        self.pfell.RegInfo.Value.DFT_en_tiapn = 1
        self.pfell.RegInfo.Value.SEL_dac_vbp = 0
        self.pfell.RegInfo.Value.DFT_SELN = 3
        self.pfell.RegInfo.Value.DFT_SELP = 1
        self.pfell.RegInfo.Value.CMPIN_SEL = 1
        self.pfell.RegInfo.Value.CMPIN_EN = 1
        self.pfell.RegInfo.Value.CMPIP_EN = 1
        self.pfell.RegInfo.Value.CMPIP_SEL = 1
        self.pfell.write(pfe_num)

    def get_pfe_dft_voltages(self, pfe_num, tp="AI1", Source = "SCOPE_CH3" , iters = 3 ,delay=0.1):

        initial_config = self.pfell.RegInfo.copy()

        self.pfell.set_ana_dft_mux(tp, "P")
        self.pfell.fnDFT_vp(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_p = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_p = self.getCompOut(source="CHANnel3",iters = iters,pfe_num = pfe_num, vth= 0)*(-1)


        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)


        self.pfell.set_ana_dft_mux(tp, "N")
        self.pfell.fnDFT_vn(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_n = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_n = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)


        self.pfell.set_ana_dft_mux(tp, "P")
        self.pfell.fnDFT_prap(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_prap = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_prap = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)


        self.pfell.set_ana_dft_mux(tp, "N")
        self.pfell.fnDFT_pran(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_pran = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_pran = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        self.pfell.set_ana_dft_mux(tp, "P")
        self.pfell.fnDFT_D2S_OUT(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_d2s_out = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_d2s_out = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        self.pfell.set_ana_dft_mux(tp, "N")
        self.pfell.fnDFT_GM_LP(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_gm_lp = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_gm_lp = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        self.pfell.set_ana_dft_mux(tp, "P")
        self.pfell.fnDFT_sen_sensor(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_sense = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_sense = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.set_ana_dft_mux(tp, "P")
        self.pfell.fnDFT_sen_Vnb(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_sense_vnb = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_sense_vnb = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        self.pfell.set_ana_dft_mux(tp, "N")
        self.pfell.fnDFT_REF_OUT(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_ref = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_ref = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)


        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        self.pfell.set_ana_dft_mux(tp, "N")
        self.pfell.fnDFT_DAC_THRU_N_MUX(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_dft_dac = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_dft_dac = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        self.pfell.set_ana_dft_mux(tp, "N")
        self.pfell.fnDFT_vbn(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_nb = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_nb = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        self.pfell.set_ana_dft_mux(tp, "N")
        self.pfell.fnDFT_DAC_AUX_THRU_N_MUX(pfe_num)
        time.sleep(delay)
        if Source == "DVM":
            v_beta_mul = float(self.dmm11.fnGetVoltage())
        elif Source == "SCOPE_CH3":
            v_beta_mul = self.getCompOut(source="CHANnel3", iters=iters, pfe_num=pfe_num, vth=0)*(-1)

        self.pfell.RegInfo = initial_config.copy()
        write_ok = self.pfell.write(pfe_num)

        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (vp) is: %.3f" %v_p)
        print("Voltage on AI1 (vn) is: %.3f" %v_n)
        print("vp - vn = %.1f" % ((v_p - v_n) * 1000) + " mV")
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (prap) is: %.3f" %v_prap)
        print("Voltage on AI1 (pran) is: %.3f" %v_pran)
        print("prap - pran = %.1f" %((v_prap-v_pran)*1000) + " mV")
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (D2S Out) is: %.3f" % v_d2s_out)
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (GM LP) is: %.3f" % v_gm_lp)
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (V Sensor) is: %.3f" % v_sense)
        print("Voltage on AI1 (V Sensor VNB) is: %.3f" % v_sense_vnb)
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (VREF) is: %.3f" %v_ref)
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (DFT DAC) is: %.3f" %v_dft_dac)
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (VBN) is: %.3f" % v_nb)
        print("-----------------------------------------------------------------")
        print("Voltage on AI1 (Beta Multiplier) is: %.3f" %v_beta_mul)
        print("-----------------------------------------------------------------")

        v={"v_p":[v_p],"v_n":[v_n], "v_prap":[v_prap], "v_pran":[v_pran], "v_d2s":[v_d2s_out], "v_gm_lp":[v_gm_lp],
           "v_sense":[v_sense], "v_sense_vnb":[v_sense_vnb], "v_ref":[v_ref], "v_dft_dac":[v_dft_dac], "v_nb":[v_nb],
           "v_beta_mul":[v_beta_mul]}
        voltages=clsStruct(**v)
        return voltages


    def pfe_tia_vp_calib(self, pfe=3, direction="up", save_data=True, filename="PFE_Calibration.xlsx", delay = 0.01,vth=1.65,dac_int=0.1):

        """
        vp calibration should not be depended on pfe
        """

        #region Need to move this block to MAIN_PFE this is the initial configuration code
        #TODO: Move this over !

        #self.YODA_mode=True
        #Set F1 with internal sense resistor and minimum vp gain resistor

        # if self.YODA_mode:
        #     self.pfell.fnSetYodaModeF1()
        #
        #     self.pfell.write(1)
        #
        # self.pfell.RegInfo = self.pfell.RegInfo_Defaults.copy()
        # print("Settings F1's TIA to 512")
        # self.pfell.RegInfo.Value.TIA_DRC1 = 512
        #
        # self.pfell.write(1)
        #
        # self.pfell.RegInfo = self.pfell.RegInfo_Defaults.copy()
        #
        # self.pfell.write_defaults(pfe_select=pfe)
        # print("Writing Defaults")

        self.override_defaults(pfe)


        # if self.YODA_mode:
        #     self.pfell.fnSetYodaModeF3()
        #endregion


        # Set Mux for TIA Calibration
        self.printRegInfo(self.pfell.RegInfo)
        print("Starting TIA vp calibration on %d"%pfe)
        if save_data:
            print("Creating results .xlsx File")
            self.ExcelFileHandler.CreateEmptyFile(os.path.join(self.ResultPath,filename),sheetname="pfe_tia_vp_calib",save_now=True)

        if save_data:
            try:
                #PFE_Calibration.xlsx
                sheet_name = "PFE%d_Calibration" % pfe
                self.ConfigFile_dict = self.ExcelFileHandler.ReadFromExistedFile(os.path.join(self.ProjectPath,self.ConfigurationFolder,"PFE_Calibration.xlsx"),sheet_name=None)
                PFEdf=self.ConfigFile_dict[sheet_name]
                print("PFE Excel file DB loaded")
            except IOError:
                raise

        step=1

        time.sleep(delay)

        self.pfell.fnCalibVpMuxConfig(pfe_sel=pfe, YODA_mode = self.YODA_mode)

        #tia_drc1_values=2**np.arange(0+int(np.log2(self.pfell.RegInfo.loc['TIA_DRC1'].Value)), self.pfell.RegInfo.Bits.TIA_DRC1 , step )
        tia_drc1_values = 2 ** np.arange(0,self.pfell.RegInfo.Bits.TIA_DRC1, step)

        tia_drc1_values=np.insert(tia_drc1_values,0,0)

        #tia_drc1_values=tia_drc1_values[::-1]

        #Setting intial TIA_DRC1
        #CompOut=0

        CompOut = self.getCompOut()

        #CompOut = 0

        if np.mean(CompOut)<vth:

            direction='up' #up
        else:

            direction = 'down'


        if direction=='up':
            i = 0
            while (np.mean(CompOut) < vth) and (i < len(tia_drc1_values)):

                self.pfell.RegInfo.at['TIA_DRC1', 'Value']=tia_drc1_values[i]

                print("TIA_DRC1 value is ",tia_drc1_values[i])

                self.printRegInfo(self.pfell.RegInfo)

                self.pfell.write(pfe)#out_buffer)

                time.sleep(delay)

                CompOut=self.getCompOut()

                print("Comp Out ",np.mean(CompOut))

                i+=1

                # if (i==(self.pfell.RegInfo.Bits.TIA_DRC1)) and (np.mean(CompOut)<vth/4):
                #     print("ERROR VP FAIL MAX")
                #     return False
            print("The final TIA_DRC1 value is: ",self.pfell.RegInfo.loc['TIA_DRC1'].Value)


        elif direction=='down':
            i=len(tia_drc1_values)-1
            while (np.mean(CompOut) > vth) and (i >= 0):

                self.pfell.RegInfo.at['TIA_DRC1', 'Value'] = tia_drc1_values[i]

                print("TIA_DRC1 value is ", tia_drc1_values[i])
                self.printRegInfo(self.pfell.RegInfo)
                self.pfell.write(pfe)#out_buffer)

                time.sleep(delay)

                CompOut = self.getCompOut()

                i -= 1;

                # time.sleep(0.1)
                # self.get_pfe_dft_voltages(pfe, "AO2")

                if (i == (self.pfell.RegInfo.Bits.TIA_DRC1)) and (np.mean(CompOut) < vth/4):
                    print("ERROR VP FAIL MIN")
                    return False

        # time.sleep(0.1)
        # self.get_pfe_dft_voltages(pfe, "AO2")

        if save_data:
            PFEdf=self.pfell.RegInfo.copy()

            self.ExcelFileHandler.WriteToExistedFile(os.path.join(self.ResultPath,filename), PFEdf, sheet_name='PFE%d_Calibration'%pfe+"_TIA")

        return(self.pfell.RegInfo.loc['TIA_DRC1'].Value)

    def pfe_tia_vnb_DAC_calib(self, pfe=3,vth=1.65, direction="up", save_data=True, filename="PFE_Calibration.xlsx",delay=0.1,dac_init=0.1):

        print("\n\nStarting TIA vnb DAC calibration on pfe %d\n"%pfe)

        #self.pfell.write_defaults(pfe_select=pfe)

        ##Set DAC###

        Gain = self.R2/(self.R1+self.R2)

        dac_N = self.pfell.fnSetDAC(Gain=Gain)

        step=0.001

        dac = self.pfell.DacAccess
        # #self.get_pfe_dft_voltages(pfe)
        # R1 = 33.2
        # R2 = 3
        # Gain = (R1+R2)/R2
        #
        # dac_N = int(dac.volt_to_dac(0.10, 2.048) * Gain)
        #
        # dac.DAC_Update(0, dac_N)

        #self.pfell.write(pfe)

        time.sleep(delay)

        CompOut = self.getCompOut()

        if np.mean(CompOut) < vth:

            i=0

            while (np.mean(CompOut) <= vth) and (i < 20):

                dac_init = dac_init-step*1

                if abs(dac_init)>0.12:
                    print("VNB too high")

                    break

                dac_N=self.pfell.fnSetDAC(Gain=Gain, DAC_V=dac_init)

                time.sleep(delay)

                CompOut = self.getCompOut()

                # if abs(np.mean(CompOut)-vth/2.)>0.1:
                #     if step>0.0005:
                #         step-=0.001
                print("Comp Out", np.mean(CompOut))
                print("DAC Value: ", dac_N)
                print("DAC Voltage: %.2f mV" % (1000 * (float(dac_N) / 2 ** 12) * 2.048 * Gain))
                print("-----------------------------------------------------------------------------------------------")
                i+= 1;

        elif (np.mean(CompOut) > vth):

            i=0

            while (np.mean(CompOut) > vth) and (i < 20):

                dac_init =dac_init +step*1

                if abs(dac_init) > 0.12:
                    print("VNB too high")

                    break

                dac_N = self.pfell.fnSetDAC(Gain=Gain, DAC_V=dac_init)

                time.sleep(delay)

                CompOut = self.getCompOut()

                # if abs(np.mean(CompOut)-vth/2.)>0.1:
                #     if step>0.0005:
                #         step-=0.001


                print("Comp Out", np.mean(CompOut))
                print("DAC Value: ", dac_N)
                print("DAC Voltage: %.2f mV" % (1000 * (float(dac_N) / 2 ** 12) * 2.048 * Gain))
                print("-----------------------------------------------------------------------------------------------")
                i+= 1;

        # time.sleep(0.1)
        # self.get_pfe_dft_voltages(pfe, "AO2")

        return(dac_N)


    def pfe_tia_vn_calib(self, pfe=3, direction="up", save_data=True, filename="PFE_Calibration.xlsx", delay=0.01, vth=1.65):

        print("Starting TIA vn calibration on pfe %d"%pfe)

        #self.pfell.write_defaults(pfe_select=pfe)
        if save_data:
            try:
                #PFE_Calibration.xlsx
                sheet_name = "PFE%d_Calibration" % pfe
                self.ConfigFile_dict = self.ExcelFileHandler.ReadFromExistedFile(os.path.join(self.ProjectPath,self.ConfigurationFolder,"PFE_Calibration.xlsx"),sheet_name=None)
                PFEdf=self.ConfigFile_dict[sheet_name]
                print("PFE Excel file DB loaded")
            except IOError:
                raise

        # Set  excel file name from MAIN-->TestsResultFile
        step=1

        tia_drc0_values=2**np.arange(0,self.pfell.RegInfo.Bits.TIA_DRC0,step)
        #Setting intial TIA_DRC1
        CompOut=0


        if direction=='up':
            i = 0
            ## Sweeping to find first  DRC0 bit
            while (np.mean(CompOut) <= vth) and (i < self.pfell.RegInfo.Bits.TIA_DRC0):

                self.pfell.RegInfo.at['TIA_DRC0','Value']=tia_drc0_values[i]

                self.pfell.write(pfe,"Debug")

                time.sleep(delay)

                CompOut=self.pfell.getCompOut()
                i+=1;

                if (i==(self.pfell.RegInfo.Bits.TIA_DRC0-1)) and (np.mean(CompOut)<vth/4):
                    print("ERROR VN FAIL MAX")
                    return False

            ## Decrease by one notch
            self.pfell.RegInfo.at['TIA_DRC0','Value']=tia_drc0_values[i]+tia_drc0_values[i]/2

            self.pfell.write(pfe,"Debug")

            time.sleep(delay)

            CompOut = self.getCompOut()

            if (np.mean(CompOut)> vth):
                pass
                #return(self.pfell.RegInfo.loc['TIA_DRC0'].Value)
            else:
                self.pfell.RegInfo.at['TIA_DRC0','Value']=tia_drc0_values[i]

                #return (self.pfell.RegInfo.loc['TIA_DRC0'].Value)

        elif direction == 'down':
            i = self.pfell.RegInfo.Bits.TIA_DRC0-1
            ## Sweeping to find first  DRC0 bit
            while (np.mean(CompOut) >= vth) and (i >= 0):

                self.pfell.RegInfo.at['TIA_DRC0', 'Value'] = tia_drc0_values[i]

                self.pfell.write(pfe,"Debug")

                time.sleep(delay)

                CompOut = self.pfell.getCompOut()

                i -= 1;

                if (i == (self.pfell.RegInfo.Bits.TIA_DRC0 - 1)) and (np.mean(CompOut) < vth/4):
                    print("ERROR VN FAIL MAX")
                    return False

            ## Decrease by one notch
            self.pfell.RegInfo.at['TIA_DRC0', 'Value'] = tia_drc0_values[i] + tia_drc0_values[i] / 2

            self.pfell.write(pfe)

            time.sleep(delay)

            CompOut = self.pfell.getCompOut()

            print("Average CompOut value", np.mean(CompOut))

            if (np.mean(CompOut) > vth):
                pass
                #return (self.pfell.RegInfo.loc['TIA_DRC0'].Value)
            else:
                self.pfell.RegInfo.at['TIA_DRC0', 'Value'] = tia_drc0_values[i]
                #return (self.pfell.RegInfo.loc['TIA_DRC0'].Value)

            #FullFeed = self.pfell.fnFullFeed(ConfigName=self.mode)

            #out_buffer = self.pfell.CreateOutBuffer(FullFeed, buf_range=16, reverse=False)

            self.pfell.write(pfe)

        if save_data:
            PFEdf=self.pfell.RegInfo.copy()

            self.ExcelFileHandler.WriteToExistedFile(os.path.join(self.ResultPath, filename), PFEdf, sheet_name='PFE%d_Calibration'%pfe+'_TIA')


        return(self.pfell.RegInfo.loc['TIA_DRC0'].Value)




    def pfe_pra_calib(self, pfe=3, vp_vn_tia_cal=False, save_data=True, filename="PFE_Calibration.xlsx", delay=0.01, vth=1.65,Retry=False,dac_init=0.05):
        """

        :param pfe: pfe value
        :param vp_vn_tia_cal: Set by user ,if not provided tia calibration will be done before
        :return:
        """

        CalibStatus=True

        #dac=self.pfell.DacAccess

        Gain = self.R2/(self.R1+self.R2)
        print("Setting DAC Output Voltage to: ", 1000 * dac_init, " mV")
        dac_N = self.pfell.fnSetDAC(Gain=Gain,DAC_V=dac_init)

        if vp_vn_tia_cal:
            self.pfell.write_defaults(pfe_select=pfe)

        if save_data:
            try:
                #PFE_Calibration.xlsx
                sheet_name = "PFE%d_Calibration" % pfe
                self.ConfigFile_dict = self.ExcelFileHandler.ReadFromExistedFile(os.path.join(self.ProjectPath,self.ConfigurationFolder,"PFE_Calibration.xlsx"),sheet_name=None)
                PFEdf=self.ConfigFile_dict[sheet_name]
                print("PFE Excel file DB loaded")
            except IOError:
                raise



        if vp_vn_tia_cal:
            print("Starting TIA calibration first")
            if pfe>1:
                vp_tia_cal = self.pfe_tia_vp_calib(pfe,"up",vth=vth,dac_int=dac_init)
                vp_tia_cal = vp_tia_cal# / 2 ;  # One value below
                vn_tia_cal = PFEdf.loc['TIA_DRC0'].Value  # Load from config file
            else:
                vp_tia_cal = self.pfe_tia_vp_calib(pfe,"up",vth=vth,dac_int=dac_init)
                vn_tia_cal = self.pfe_tia_vn_calib(pfe,"up")
                vp_tia_cal=vp_tia_cal #/ 2 ;# One value below

        else:

            try:
                print("Loading calibration values from config file")

                #vp_tia_cal = PFEdf.loc['TIA_DRC1'].Value #Load from config file

                #vn_tia_cal = PFEdf.loc['TIA_DRC0'].Value #Load from config file
            except:
                print( "Setting default values as DB not given")
                vp_tia_cal = self.pfell.RegInfo['TIA_DRC1'].Value
                vn_tia_cal = self.pfell.RegInfo['TIA_DRC0'].Value

        # if (self.pfell.RegInfo.loc['TIA_DRC1'].Value)<=2:
        #
        #     self.pfell.RegInfo.at['REF_SEL0', 'Value'] = 1
        #
        #     self.pfell.RegInfo.at['REF_SEL_lh', 'Value'] = 1
        #
        #     self.pfell.write(pfe)


        CompOut=self.getCompOut()

        if np.mean(CompOut)>vth:
            direction = 1
        else:
            direction = -1

            # #Use V sensor to fine tune vp

        dac_N=self.pfe_tia_vnb_DAC_calib(pfe=pfe,direction=direction,dac_init=dac_init)


        dac_N_list = [dac_N]

        #
        # #Set Mux for  PRA Calibration
        #self.pfell.fnCalibPRAMuxConfig(pfe_sel=pfe)
        if not self.YODA_mode:
            self.pfell.fnCalibD2SMuxConfig(pfe_sel=pfe)


        if Retry:
            self.pfell.fnCalibGMLPMuxConfig(pfe_sel=pfe)
        else:
            self.pfell.fnCalibD2SMuxConfig(pfe_sel=pfe)

        ###All Lists
        PRA_VP_ALL=[]
        PRA_VN_ALL = []
        COMP_OUT_ALL=[]

        ## For J list last 2 if j=2
        pra_dac_vn_list = []
        pra_dac_vp_list = []
        comp_out_list=[]


        vp_tia_list=[]
        vn_tia_list=[]
        pra_calib_list=[]

        if pfe>1:
            if vp_tia_cal==111:
                pra_calib_list = [[vp_tia_cal*2, vn_tia_cal],[vp_tia_cal,vn_tia_cal]]
                #direction=-1
            else:
                if vp_tia_cal > 0:
                    pra_calib_list=[[vp_tia_cal,vn_tia_cal],[vp_tia_cal>>1,vn_tia_cal]] #[vp_tia_cal*2,vn_tia_cal]
                #direction = 1
        else:
            if vp_tia_cal ==111:
                pra_calib_list = [[vp_tia_cal*2, vn_tia_cal//2],[vp_tia_cal, vn_tia_cal//2],[vp_tia_cal/2, vn_tia_cal],[vp_tia_cal, vn_tia_cal]]
                #direction = -1
            else:
                pra_calib_list = [[vp_tia_cal // 2, vn_tia_cal // 2], [vp_tia_cal, vn_tia_cal// 2],[vp_tia_cal // 2, vn_tia_cal], [vp_tia_cal, vn_tia_cal]]
                #direction = 1

        RegConfigsTemp=self.pfell.RegInfo.copy()
        dfPRAcalib=IOFile.pd.DataFrame()

        step=1

        for j,tia in enumerate(pra_calib_list):

            ###Setting default value
            # if j>1:
            #     direction = -1


            print("Start PRA with TIA [DRC1, DRC0] = ",tia)

            pra_dac_vn_init =  RegConfigsTemp.at['PRA_DACN', 'Value']

            pra_dac_vp_init =  RegConfigsTemp.at['PRA_DACP', 'Value']

            pra_dac_vn = pra_dac_vn_init
            pra_dac_vp = pra_dac_vp_init

            vp_tia=tia[0];vn_tia=tia[1]

            vp_tia_list.append(vp_tia)
            vn_tia_list.append(vn_tia)

            self.pfell.RegInfo.at['TIA_DRC1', 'Value'] = vp_tia

            self.pfell.RegInfo.at['TIA_DRC0', 'Value'] = vn_tia

            # Set PRA DAC vp & vn

            self.pfell.RegInfo.at['PRA_DACN', 'Value'] = pra_dac_vn_init

            self.pfell.RegInfo.at['PRA_DACP', 'Value'] = pra_dac_vp_init

            self.printRegInfo(self.pfell.RegInfo)

            self.pfell.write(pfe)

            # Use V sensor to fine tune vp
            # This if to tune lower TIA value TIA/2
            if j > 0:

                self.pfell.fnCalibVpMuxConfig(pfe_sel=pfe, YODA_mode = self.YODA_mode)

                CompOut = self.getCompOut()

                if np.mean(CompOut) > vth:
                    direction = 1
                else:
                    direction = -1

                dac_N = self.pfe_tia_vnb_DAC_calib(pfe=pfe,direction=direction,dac_init=dac_init)

                dac_N_list.append(dac_N)
                # #Set Mux for  PRA Calibration
                # self.pfell.fnCalibPRAMuxConfig(pfe_sel=pfe)
                if not self.YODA_mode:
                    self.pfell.fnCalibD2SMuxConfig(pfe_sel=pfe)

            time.sleep(delay)

            CompOut=self.getCompOut()

            print("PRA DAC VP ", pra_dac_vp)
            print("PRA DAC VN ", pra_dac_vn)
            print("TIA value", vp_tia)
            print("Average CompOut value", np.mean(CompOut))
            print("-------------------------------------------")


            init_comp_val = np.mean(CompOut)

            if init_comp_val< vth:
                i=0
                pra_dac_vp_loop=[]
                pra_dac_vn_loop=[]
                comp_out_list_loop=[]
                while np.mean(CompOut)< vth and (i < 2 ** (self.pfell.RegInfo.Bits.PRA_DACN - 1) - 1):

                    pra_dac_vn-=step
                    pra_dac_vp+=step

                    # if abs(pra_dac_vn>57) or abs(pra_dac_vp)>57:
                    #     break
                    print("PRA DAC VP ",pra_dac_vp)
                    print("PRA DAC VN ",pra_dac_vn)
                    print("TIA value",vp_tia )
                    self.pfell.RegInfo.at['PRA_DACN', 'Value'] = pra_dac_vn
                    self.pfell.RegInfo.at['PRA_DACP', 'Value'] = pra_dac_vp

                    self.printRegInfo(self.pfell.RegInfo)
                    self.pfell.write(pfe)

                    time.sleep(delay)

                    CompOut = self.getCompOut()

                    print("Average CompOut value", np.mean(CompOut))


                    print("-------------------------------------------")

                    # if abs(np.mean(CompOut)-vth/2)>0.1:
                    #     if step > 1:
                    #         step = step // 2



                    if (i==(2**self.pfell.RegInfo.Bits.PRA_DACN-1)) and (np.mean(CompOut)<vth/4):
                        print("ERROR VN FAIL MAX")
                        return False

                    ###We have to debug it  shouldn't be in product !!!
                    if (init_comp_val>np.mean(CompOut)) and (i>2) and (np.mean(CompOut)>vth/8):

                        print("Wrong direction !!! ")

                        print("Break with Comp Out > vth")

                        print("Revert pra configs")
                        pra_dac_vn += step
                        pra_dac_vp -= step

                        self.pfell.RegInfo.at['PRA_DACP', 'Value'] = pra_dac_vp
                        self.pfell.RegInfo.at['PRA_DACN', 'Value'] = pra_dac_vn

                        self.printRegInfo(self.pfell.RegInfo)
                        self.pfell.write(pfe)

                        CalibStatus=False

                    pra_dac_vp_loop.append(pra_dac_vp)
                    pra_dac_vn_loop.append(pra_dac_vn)
                    comp_out_list_loop.append(np.mean(CompOut))

                    i+=1
                PRA_VP_ALL.append(pra_dac_vp_loop)
                PRA_VN_ALL.append(pra_dac_vn_loop)
                COMP_OUT_ALL.append(comp_out_list_loop)

                pra_dac_vn_list.append(pra_dac_vn)
                pra_dac_vp_list.append(pra_dac_vp)
                comp_out_list.append(np.mean(CompOut))



            elif np.mean(CompOut)> vth:

                i=0
                pra_dac_vp_loop=[]
                pra_dac_vn_loop=[]
                comp_out_list_loop = []
                while (np.mean(CompOut) > vth) and (i < 2 ** (self.pfell.RegInfo.Bits.PRA_DACP - 1) - 1):

                    pra_dac_vp-=step
                    pra_dac_vn+=step
                    print("PRA DAC VP ",pra_dac_vp)
                    print("PRA DAC VN ",pra_dac_vn)
                    print("TIA value", vp_tia)
                    self.pfell.RegInfo.at['PRA_DACP', 'Value'] = pra_dac_vp
                    self.pfell.RegInfo.at['PRA_DACN', 'Value'] = pra_dac_vn

                    self.printRegInfo(self.pfell.RegInfo)
                    self.pfell.write(pfe)

                    # time.sleep(0.1)
                    # self.get_pfe_dft_voltages(pfe, "AO2")

                    time.sleep(delay)

                    CompOut = self.getCompOut()

                    print("Average CompOut value", np.mean(CompOut))
                    print("-------------------------------------------")

                    # if abs(np.mean(CompOut)-vth/2)>0.1:
                    #     if step > 1:
                    #         step = step // 2

                    if (i==(2**self.pfell.RegInfo.Bits.PRA_DACP-1)) and (np.mean(CompOut)>vth*3./4):
                        print("ERROR VP FAIL MAX")
                        return False

                    ###We have to debug it  shouldn't be in product !!!
                    if (init_comp_val < np.mean(CompOut)) and (i > 2) and (np.mean(CompOut) < vth*8./10):
                        print("Wrong direction !!! ")

                        print("Break with Comp Out > 0.5")

                        print("Revert pra configs")
                        pra_dac_vn -= step
                        pra_dac_vp += step

                        self.pfell.RegInfo.at['PRA_DACP', 'Value'] = pra_dac_vp
                        self.pfell.RegInfo.at['PRA_DACN', 'Value'] = pra_dac_vn

                        self.printRegInfo(self.pfell.RegInfo)
                        self.pfell.write(pfe)

                        CalibStatus=False

                    pra_dac_vp_loop.append(pra_dac_vp)
                    pra_dac_vn_loop.append(pra_dac_vn)
                    comp_out_list_loop.append(np.mean(CompOut))


                    i+=1

                PRA_VP_ALL.append(pra_dac_vp_loop)
                PRA_VN_ALL.append(pra_dac_vn_loop)
                COMP_OUT_ALL.append(comp_out_list_loop)

                comp_out_list.append(np.mean(CompOut))
                pra_dac_vn_list.append(pra_dac_vn)
                pra_dac_vp_list.append(pra_dac_vp)

        #ref_l=max([len(pra_dac_vp_list),len(pra_dac_vn_list),len(vp_tia_list),len(comp_out_list)])

        print("PRA DAC VP LIST", pra_dac_vp_list)
        dfPRAcalib['pra_dac_vp'] = pra_dac_vp_list
        # if len(pra_dac_vn_list)<ref_l:
        #     pra_dac_vn_list.append(None)
        print("PRA DAC VN LIST", pra_dac_vn_list)
        dfPRAcalib['pra_dac_vn'] = pra_dac_vn_list


        print("TIA VP LIST", vp_tia_list)
        # if len(vp_tia_list)<ref_l:
        #     vp_tia_list.append(None)
        dfPRAcalib['tia_vp'] = vp_tia_list

        print("TIA VN LIST", vn_tia_list)
        # if len(vn_tia_list)<ref_l:
        #     vn_tia_list.append(None)
        dfPRAcalib['tia_vn'] = vn_tia_list

        print("COMP OUT LIST AVERAGE", comp_out_list)
        # if len(comp_out_list)<ref_l:
        #     comp_out_list.append(None)
        dfPRAcalib['CompOut'] = comp_out_list

        #### Setting per the closet PRAs vp ,vn ####
        print("Setting the TIA value by the low pra distance")
        pra_diff_arr=np.abs(np.array(pra_dac_vp_list)-np.array(pra_dac_vn_list))
        min_index=np.argmin(pra_diff_arr)

        print("Setting TIA DRC1: ",vp_tia_list[min_index])
        #print("Setting Vbn for TIA DRC" ,dac_N_list[min_index])
        print("Setting DAC Output Word to: ", dac_N_list[min_index])
        self.pfell.fnSetDAC(Gain=self.R2/(self.R1+self.R2), DAC_V=dac_N_list[min_index], DAC_N=True)

        #dac.DAC_Update(0, dac_N_list[min_index])


        print("Setting PRA DAC P : ", pra_dac_vp_list[min_index])
        print("Setting PRA DAC N : ", pra_dac_vn_list[min_index])

        self.pfell.RegInfo.at['TIA_DRC1', 'Value'] = vp_tia_list[min_index]

        self.pfell.RegInfo.at['TIA_DRC0', 'Value'] = vn_tia_list[min_index]

        ###### Setting PRA by the closet to Vref/2 Comp Out#######

        comp_out_last = COMP_OUT_ALL[min_index][-1]

        if len(COMP_OUT_ALL[min_index])>1:
            comp_out_2_last = COMP_OUT_ALL[min_index][-2]
        else:
            comp_out_2_last=comp_out_last

        print("Previous CompOut :",comp_out_2_last)
        print("CompOut Last:", comp_out_last)

        if abs(comp_out_last-vth)>abs(comp_out_2_last-vth) and abs(comp_out_2_last-vth)<((vth * 10.)/100) and (comp_out_last!=comp_out_2_last):

            print("Setting previous PRA values as close to Vref/2")
            print("Setting PRA DAC P : ", PRA_VP_ALL[min_index][-2])
            print("Setting PRA DAC N : ", PRA_VN_ALL[min_index][-2])

            self.pfell.RegInfo.at['PRA_DACP','Value'] = PRA_VP_ALL[min_index][-2]

            self.pfell.RegInfo.at['PRA_DACN','Value'] = PRA_VN_ALL[min_index][-2]

            self.printRegInfo(self.pfell.RegInfo)
            self.pfell.write(pfe)

            # time.sleep(0.1)
            # self.get_pfe_dft_voltages(pfe, "AO2")

        else:
            print("Last CompOut is the closest to Vref")
            print("Setting last PRA values")
            print("Setting PRA DAC P : ", PRA_VP_ALL[min_index][-1])
            print("Setting PRA DAC N : ", PRA_VN_ALL[min_index][-1])

            self.pfell.RegInfo.at['PRA_DACP','Value'] = PRA_VP_ALL[min_index][-1]

            self.pfell.RegInfo.at['PRA_DACN','Value'] = PRA_VN_ALL[min_index][-1]

            self.printRegInfo(self.pfell.RegInfo)
            self.pfell.write(pfe)





        writer=self.ExcelFileHandler.CreateEmptyFile(os.path.join(self.ResultPath,"pfe_pra_calib.xlsx"),sheetname="pra__calib")

        dfPRAcalib.to_excel(writer,sheet_name="pfe_pra_calib")

        writer.save()

        #Saving the calibrated values
        # idx_min = np.argmin(abs(np.array(pra_dac_vp_list)-np.array(pra_dac_vn_list)))
        #
        # self.pfell.RegInfo.at['PRA_DACP', 'Value'] = pra_dac_vp_list[idx_min]
        # self.pfell.RegInfo.at['PRA_DACN', 'Value'] = pra_dac_vn_list[idx_min]

        # time.sleep(0.1)
        # self.get_pfe_dft_voltages(pfe, "AO2")

        if save_data:
            PFEdf = self.pfell.RegInfo.copy()

            self.ExcelFileHandler.WriteToExistedFile(os.path.join(self.ResultPath, filename), PFEdf, sheet_name='PFE%d_Calibration'%pfe+'_PRA')

        return(pra_dac_vp_list,pra_dac_vn_list,CalibStatus)

    def pfe_d2s_calib(self, pfe=3, pra_cal=False, save_data=True, filename="PFE_Calibration.xlsx", delay=0.01, vth=1.65):

        print("Starting D2S calibration on pfe %d"%pfe)

        #if pra_cal:
            #self.pfell.write_defaults(pfe_select=pfe)

        if save_data:
            try:
                #PFE_Calibration.xlsx
                sheet_name = "PFE%d_Calibration" % pfe
                self.ConfigFile_dict = self.ExcelFileHandler.ReadFromExistedFile(os.path.join(self.ProjectPath,self.ConfigurationFolder,"PFE_Calibration.xlsx"),sheet_name=None)
                PFEdf=self.ConfigFile_dict[sheet_name]
                print("PFE Excel file DB loaded")
            except IOError:
                raise


        #Set Mux for D2S Calibration
        if not self.YODA_mode:
            self.pfell.fnCalibD2SMuxConfig(pfe_sel=pfe)

        #self.pfell.RegInfo.at['TIA_DRC1', 'Value'] = PFEdf.loc['TIA_DRC1', 'Value']

        #self.pfell.RegInfo.at['TIA_DRC0', 'Value'] = PFEdf.loc['TIA_DRC0', 'Value']

        # Set PRA DAC vp & vn

        #self.pfell.RegInfo.at['PRA_DACN', 'Value'] = PFEdf.loc['PRA_DACN', 'Value']

        #self.pfell.RegInfo.at['PRA_DACP', 'Value'] = PFEdf.loc['PRA_DACP', 'Value']

        #self.pfell.RegInfo.at['D2S_DACP', 'Value']=16

        #self.pfell.RegInfo.at['D2S_DACN', 'Value']=16

        #self.pfell.write(pfe)

        CompOut=self.getCompOut()

        d2s_dac_vn=self.pfell.RegInfo.loc['D2S_DACN'].Value
        d2s_dac_vp = self.pfell.RegInfo.loc['D2S_DACP'].Value

        # if (vth - LeftGuard)<np.mean(CompOut)<(vth + RightGuard):
        #
        #     self.pfell.RegInfo.at['D2S_DACP', 'Value'] = d2s_dac_vp
        #     self.pfell.RegInfo.at['D2S_DACN', 'Value'] = d2s_dac_vn
        #
        #     if save_data:
        #         PFEdf = self.pfell.RegInfo.copy()
        #
        #         self.ExcelFileHandler.WriteToExistedFile(os.path.join(self.ResultPath, filename), PFEdf,
        #                                                  sheet_name='PFE%d_Calibration' % pfe + '_D2S')
        #
        #     return (d2s_dac_vp, d2s_dac_vn)

        d2s_dac_vn_list=[]
        d2s_dac_vp_list = []
        CompOut_list=[]

        init_comp_val = np.mean(CompOut)
        step=1
        if init_comp_val <= vth:
            i = 0
            while (np.mean(CompOut) <= vth) and (i < 2 ** (self.pfell.RegInfo.Bits.D2S_DACN - 1) - 1):

                d2s_dac_vn -= step
                d2s_dac_vp += step

                self.pfell.RegInfo.at['D2S_DACN', 'Value'] = d2s_dac_vn
                self.pfell.RegInfo.at['D2S_DACP', 'Value'] = d2s_dac_vp

                print("D2S DAC VP : %d" %d2s_dac_vp)
                print("D2S DAC VN : %d" %d2s_dac_vn)

                self.printRegInfo(self.pfell.RegInfo)
                self.pfell.write(pfe)
                # time.sleep(0.1)
                # self.get_pfe_dft_voltages(pfe, "AO2")

                time.sleep(delay)

                CompOut = self.getCompOut()

                # if abs(np.mean(CompOut) - vth / 2) > 0.1:
                #     if step > 1:
                #         step = step / 2

                d2s_dac_vn_list.append(d2s_dac_vn)

                d2s_dac_vp_list.append(d2s_dac_vp)

                avg_comp=np.mean(CompOut)

                CompOut_list.append(avg_comp)

                print("Average CompOut value : %f" %avg_comp)
                print("-------------------------------------------")


                if (i == (2 ** self.pfell.RegInfo.Bits.D2S_DACN - 1)) and (np.mean(CompOut) < vth/4):
                    print("ERROR VN FAIL MAX")
                    return False

                # ###We have to debug it  shouldn't be in product !!!
                # if (init_comp_val < np.mean(CompOut)) and (i > 2) and (np.mean(CompOut) > vth/4):
                #
                #     print("Wrong direction !!! ")
                #     print("Break with Comp Out > 0.5")
                #     print("Revert d2s configs")
                #     d2s_dac_vn += i
                #     d2s_dac_vp -= i
                #
                #     self.pfell.RegInfo.at['D2S_DACN', 'Value'] = d2s_dac_vn
                #     self.pfell.RegInfo.at['D2S_DACP', 'Value'] = d2s_dac_vp
                #
                #     print("D2S DAC VP ", d2s_dac_vp)
                #     print("D2S DAC VN ", d2s_dac_vn)
                #
                #     self.pfell.write(pfe)

                i += 1

        elif init_comp_val> vth:

            i = 0
            while (np.mean(CompOut) > vth) and (i < 2 ** (self.pfell.RegInfo.Bits.D2S_DACP - 1) - 1):

                d2s_dac_vn += step
                d2s_dac_vp -= step


                print("D2S DAC VP %d" %d2s_dac_vp)
                print("D2S DAC VN %d" %d2s_dac_vn)

                self.pfell.RegInfo.at['D2S_DACP', 'Value'] = d2s_dac_vp
                self.pfell.RegInfo.at['D2S_DACN', 'Value'] = d2s_dac_vn

                self.printRegInfo(self.pfell.RegInfo)
                self.pfell.write(pfe)
                # time.sleep(0.1)
                # self.get_pfe_dft_voltages(pfe, "AO2")

                time.sleep(delay)

                CompOut = self.getCompOut()

                # if abs(np.mean(CompOut) - vth / 2) > 0.05:
                #     if step > 1:
                #         step = step / 2

                d2s_dac_vn_list.append(d2s_dac_vn)

                d2s_dac_vp_list.append(d2s_dac_vp)

                avg_comp=np.mean(CompOut)

                CompOut_list.append(avg_comp)

                print("Average CompOut value : %f" %avg_comp)
                print("-------------------------------------------")


                # ###We have to debug it  shouldn't be in product !!!
                # if (init_comp_val < np.mean(CompOut)) and (i > 2) and (np.mean(CompOut) < vth*8/10):
                #
                #     print("Wrong direction !!! ")
                #     print("Break with Comp Out < 0.5")
                #     print("Revert pra configs")
                #     d2s_dac_vn -= i
                #     d2s_dac_vp += i
                #
                #     self.pfell.RegInfo.at['D2S_DACN', 'Value'] = d2s_dac_vn
                #     self.pfell.RegInfo.at['D2S_DACP', 'Value'] = d2s_dac_vp
                #
                #     print("D2S DAC VP ", d2s_dac_vp)
                #     print("D2S DAC VN ", d2s_dac_vn)
                #
                #     self.pfell.write(pfe)



                if (i == (2 ** self.pfell.RegInfo.Bits.PRA_DACP - 1)) and (np.mean(CompOut) < vth/4):
                    print("ERROR VP FAIL MAX")
                    return False

                i += 1

        if  sum(np.diff(CompOut_list))>0.01:

            CompIdx = np.argmin(np.abs(np.array(CompOut_list)-vth))

            d2s_dac_vn = d2s_dac_vn_list[CompIdx]

            d2s_dac_vp = d2s_dac_vp_list[CompIdx]
        else:

            print("No CompOut Changes in D2S calibration setting last values")

            d2s_dac_vn = d2s_dac_vn_list[-1]

            d2s_dac_vp = d2s_dac_vp_list[-1]


        self.pfell.RegInfo.at['D2S_DACP', 'Value'] = d2s_dac_vp
        self.pfell.RegInfo.at['D2S_DACN', 'Value'] = d2s_dac_vn

        if save_data:

            PFEdf = self.pfell.RegInfo.copy()

            self.ExcelFileHandler.WriteToExistedFile(os.path.join(self.ResultPath, filename), PFEdf, sheet_name='PFE%d_Calibration'%pfe+'_D2S')

        return(d2s_dac_vp,d2s_dac_vn)

    def pfe_gm_dac_calib(self, pfe=3, d2s_calib=False, save_data=True, filename="PFE_Calibration.xlsx", delay=0.01, vth=1.65):

        print("Starting GM calibration on pfe %d"%pfe)

        #if d2s_calib:
            #self.pfell.write_defaults(pfe_select=pfe)


        if save_data:
            try:
                #PFE_Calibration.xlsx
                sheet_name = "PFE%d_Calibration"%pfe
                self.ConfigFile_dict = self.ExcelFileHandler.ReadFromExistedFile(os.path.join(self.ProjectPath,self.ConfigurationFolder,"PFE_Calibration.xlsx"),sheet_name=None)
                PFEdf=self.ConfigFile_dict[sheet_name]
                print("PFE Excel file DB loaded")
            except IOError:
                raise


        #Set Mux for GM Calibration
        if not self.YODA_mode:
            self.pfell.fnCalibGMLPMuxConfig(pfe_sel=pfe)


        #self.pfell.RegInfo.at['TIA_DRC1', 'Value'] = PFEdf.loc['TIA_DRC1', 'Value']

        #self.pfell.RegInfo.at['TIA_DRC0', 'Value'] = PFEdf.loc['TIA_DRC0', 'Value']

        # Set PRA DAC vp & vn

        #self.pfell.RegInfo.at['PRA_DACN', 'Value'] = PFEdf.loc['PRA_DACN', 'Value']

        #self.pfell.RegInfo.at['PRA_DACP', 'Value'] = PFEdf.loc['PRA_DACP', 'Value']

        #self.pfell.RegInfo.at['D2S_DACP', 'Value'] = PFEdf.loc['D2S_DACN', 'Value']

        #self.pfell.RegInfo.at['D2S_DACN', 'Value'] = PFEdf.loc['D2S_DACP', 'Value']

        #self.pfell.RegInfo.at['GM_DACP', 'Value'] = 16

        #self.pfell.RegInfo.at['GM_DACN', 'Value'] = 16

        self.printRegInfo(self.pfell.RegInfo)
        self.pfell.write(pfe)
        time.sleep(1)
        # self.get_pfe_dft_voltages(pfe, "AO2")

        CompOut=self.getCompOut()

        print("Average CompOut value : %f" %np.mean(CompOut))

        LeftGuard = (vth * 10) / 100
        RightGuard = (vth * 10) / 100

        gm_dac_vn = self.pfell.RegInfo.loc['GM_DACN'].Value

        gm_dac_vp = self.pfell.RegInfo.loc['GM_DACP'].Value

        gm_dac_vn_list = []
        gm_dac_vp_list = []
        CompOut_list = []

        step=1

        if np.mean(CompOut)<= vth:
            i = 0
            while (np.mean(CompOut))<= vth and (i < 2 ** (self.pfell.RegInfo.Bits.GM_DACN - 1) - 1):

                gm_dac_vn -= step
                gm_dac_vp += step

                print("GM DAC VP : %d" %gm_dac_vp)
                print("GM DAC VN : %d" %gm_dac_vn)

                self.pfell.RegInfo.at['GM_DACP', 'Value'] = gm_dac_vp
                self.pfell.RegInfo.at['GM_DACN', 'Value'] = gm_dac_vn

                self.printRegInfo(self.pfell.RegInfo)
                self.pfell.write(pfe)
                # time.sleep(0.1)
                # self.get_pfe_dft_voltages(pfe, "AO2")
                time.sleep(delay)

                CompOut = self.getCompOut()
                if abs(np.mean(CompOut) - vth / 2) > 0.05:
                    if step > 1:
                        step = step / 2

                gm_dac_vn_list.append(gm_dac_vn)

                gm_dac_vp_list.append(gm_dac_vp)

                avg_comp=np.mean(CompOut)

                CompOut_list.append(avg_comp)


                print("Average CompOut value : %f" %avg_comp)
                print("-------------------------------------------")

                if (i == (2 ** self.pfell.RegInfo.Bits.GM_DACN - 1)) and (np.mean(CompOut) < vth/4):
                    print("ERROR VN FAIL MAX")
                    return False

                i += 1

        elif np.mean(CompOut) > vth:

            i = 0
            while np.mean(CompOut) > vth and (i < 2 ** (self.pfell.RegInfo.Bits.GM_DACP - 1) - 1):

                gm_dac_vn += step
                gm_dac_vp -= step


                print("GM DAC VP : %d" %gm_dac_vp)
                print("GM DAC VN : %d" %gm_dac_vn)

                self.pfell.RegInfo.at['GM_DACP', 'Value'] = gm_dac_vp
                self.pfell.RegInfo.at['GM_DACN', 'Value'] = gm_dac_vn

                self.printRegInfo(self.pfell.RegInfo)
                self.pfell.write(pfe)
                # time.sleep(0.1)
                # self.get_pfe_dft_voltages(pfe, "AO2")
                time.sleep(delay)

                CompOut = self.getCompOut()

                if abs(np.mean(CompOut) - vth / 2) > 0.05:
                    if step>1:
                        step = step/2

                gm_dac_vn_list.append(gm_dac_vn)

                gm_dac_vp_list.append(gm_dac_vp)

                avg_comp=np.mean(CompOut)

                CompOut_list.append(avg_comp)


                print("Average CompOut value :%f" %avg_comp)
                print("-------------------------------------------")

                if (i == (2 ** self.pfell.RegInfo.Bits.PRA_DACP - 1)) and (np.mean(CompOut) < vth/4):
                    print("ERROR VP FAIL MAX")
                    return False

                i += 1


        CompIdx=np.argmin(np.abs(np.array(CompOut_list)-vth))

        gm_dac_vn = gm_dac_vn_list[CompIdx]

        gm_dac_vp = gm_dac_vp_list[CompIdx]

        self.pfell.RegInfo.at['GM_DACP', 'Value'] = gm_dac_vp
        self.pfell.RegInfo.at['GM_DACN', 'Value'] = gm_dac_vn


        if save_data:

            PFEdf = self.pfell.RegInfo.copy()

            self.ExcelFileHandler.WriteToExistedFile(os.path.join(self.ResultPath, filename), PFEdf, sheet_name='PFE%d_Calibration'%pfe+'_GM')



        return(gm_dac_vp,gm_dac_vn)


    def BandwidthExaminationMDO(self,source_data="CH1",source_clock="CH2",filename=r"F:\pfe_data.csv",sample_edge="pos"):

        from Tools import pfe_shuttle_analysis as analysis

        self.CompInput = "Scope_MDO"

        filename="E:\sensor_calib_data.csv"

        AcquireSeq = "SEQUENCE" #'RUNSTOP'

        self.MDO1.fnSetAcquireStopAfter(AcquireSeq)

        data=self.getCompOut(source_data,filename=filename)

        clock=self.getCompOut(source=source_clock,filename=filename)

        CompOut = analysis.ExtractDataFromScope(data,clock,sample_edge="pos")

        import matplotlib.pyplot as plt

        import scipy.signal as signal



        w = signal.get_window('hann', len(CompOut))

        df=IOFile.pd.DataFrame()

        f, sxx = signal.periodogram(CompOut, 1.25e9, w, nfft=None, scaling='spectrum')

        df['Freq']=f
        df['sxx'] = sxx

        df.to_csv(r'C:\Debug\FFFT_Sensor_vs_Rsense\FFT_Sensor_260.csv')

        plt.semilogy(f,np.sqrt(sxx))

        plt.title("FFT Sensor 260")

        plt.xlabel('frequency [GHz]')

        plt.ylabel('Linear spectrum [V RMS]')

        plt.savefig(r'C:\Debug\FFFT_Sensor_vs_Rsense\FFT_Sensor_260.png')

        plt.grid()

        plt.show()

        #_sxx, f, SNR, Pnd, Ps, Pdc= analysis.SNRCalc(vin=CompOut,cleanDC=True)



    def BandwidthExaminationDSO(self,source_data="CHANnel1",source_clock="CHANnel2",filename=r"E:\pfe_data.csv",sample_edge="pos"):

        from Tools import pfe_shuttle_analysis as analysis

        self.CompInput="Scope_DSO"

        df=self.getCompOut(source=source_data,source_clock=source_clock)

        #self.DSO1.fnGetScopeDataAscii(source=1)

        #clock = self.getCompOut(source=source_clock)

        #clock = self.DSO1.fnGetScopeData(source= source_clock)

        #clock=self.getCompOut(Input="Scope_MDO",source=source_clock,filename=filename)

        #CompOut = analysis.ExtractDataFromScope(data,clock,sample_edge="pos")

        print("CompOut average", np.mean(df["CompOut"]))

        #print("CompOut average", np.mean(CompOut))



        # CompOutA=[]
        # for i in range(100):
        #     CompOutA.append(self.pfell.getCompOut_PE(3))
        #
        # print("CompOut average", np.mean(CompOutA))
        #
        #
        # import matplotlib.pyplot as plt
        #
        # import scipy.signal as signal
        #
        # w = signal.get_window('hann', len(CompOut))
        #
        # f, sxx = signal.periodogram(CompOut, 48e6, w, nfft=None, scaling='spectrum')
        #
        # plt.plot(f,10*np.log10(sxx))
        #
        # plt.show()

        #_sxx, f, SNR, Pnd, Ps, Pdc= analysis.SNRCalc(vin=CompOut,cleanDC=True,plotData=False,showPlot=False)
        #print("SNR value is:",SNR)

    def BandwidthExaminationFPGA(self):

        from Tools import pfe_shuttle_analysis as analysis

        self.CompInput = "FPGA"
        CompOut = self.getCompOut()

        _sxx, f, SNR, Pnd, Ps, Pdc= analysis.SNRCalc(vin=CompOut,fin=4.123e6,cleanDC=True,plotData=False,showPlot=False)


    def pfe_dynamic_calib_stability(self,pfe_num=3,vth=0.5):

        print("Start Dynamic Calibration")

        print("Checking stability on CompOut")

        #self.CompInput = "PortExtender"
        self.CompInput = "Scope_DSO_PP"
        # Stability check
        stability_table=[]
        delay=1
        for i in range(10):

            time.sleep(delay)

            CompOut = self.getCompOut()

            stability_table.append(np.mean(CompOut))

            print("CompOut after %d seconds"%(i*delay),np.mean(CompOut))

        #self.BandwidthExaminationMDO()

        StabDev = np.std(stability_table)

        print("Deviation from Threshold is :",StabDev)

        #gm_dac_vp = self.pfell.RegInfo.loc['GM_DACP'].Value
        #gm_dac_vn = self.pfell.RegInfo.loc['GM_DACN'].Value

        # self.CompInput = "Scope_DSO_PP"
        # while (0<gm_dac_vp<=31) or (0<gm_dac_vn<=31):
        #
        #     stability_table=[]
        #
        #     for i in range(5):
        #
        #         time.sleep(delay)
        #
        #         CompOut = self.getCompOut()
        #
        #         stability_table.append(np.mean(CompOut))
        #
        #         print("CompOut after %d seconds" % (i * delay), np.mean(CompOut))
        #
        #     CompAvg=np.mean(stability_table)
        #
        #     if CompAvg<= (vth -5*StabDev):
        #
        #         print("Calibration lost")
        #         gm_dac_vn -= 1
        #         gm_dac_vp += 1
        #
        #         print("Updating GM DAC VP : %d" %gm_dac_vp)
        #         print("Updating GM DAC VN : %d" %gm_dac_vn)
        #
        #         self.pfell.RegInfo.at['GM_DACP', 'Value'] = gm_dac_vp
        #         self.pfell.RegInfo.at['GM_DACN', 'Value'] = gm_dac_vn
        #
        #         self.pfell.write(3)
        #
        #     elif CompAvg>=(vth +5*StabDev):
        #
        #         print("Calibration lost")
        #         gm_dac_vn += 1
        #         gm_dac_vp = 1
        #
        #         print("Updating GM DAC VP : %d" %gm_dac_vp)
        #         print("Updating GM DAC VN : %d" %gm_dac_vn)
        #
        #         self.pfell.RegInfo.at['GM_DACP', 'Value'] = gm_dac_vp
        #         self.pfell.RegInfo.at['GM_DACN', 'Value'] = gm_dac_vn
        #
        #     time.sleep(300)



        # import matplotlib.pyplot as plt
        #
        # import scipy.signal as signal
        #
        # w = signal.get_window('hann', len(CompOut))
        #
        # f, sxx = signal.periodogram(CompOut, 48e6, w, nfft=None, scaling='spectrum')
        #
        # plt.plot(f,10*np.log10(sxx))
        #
        # plt.show()
        #self.BandwidthExaminationFPGA

        #print("CompOut value", CompOut)

        #return(CompOut)



def main():

    Ptests = PFE_SHUTTLE_TESTS()

    Ptests.getCompOut()


if __name__ == '__main__':

    main()










