import os,sys
import access as BaseAccess
import time
from Services import IOFile
import Equipment as MyEquip
import inspect

_debug = False



class PFE_Low_Level():

    def __init__(self,RegPath=r'C:/Users/Oryx/Documents/python3sv/PFE_Shutle/',regs_sheet_name='PFE_Defaults.xlsx'):


        # Load Registers Defaults to pandas DataFrame
        self.excelIO = IOFile.ExcelHandler()

        ##Creating Register File pandas object
        use_last_calib=any(['CHANGE_REG_SHUTTLE' in inspect.stack()[ind].filename for ind in range(len(inspect.stack()))])
        try:
            # if regs_sheet_name is None:
            if use_last_calib:# irad's change 
                #If sheetname not given it will return dictionary pandas ver > 0.21
                # self.PFE_File_dict=self.excelIO.ReadFromExistedFile(RegPath,sheet_name=regs_sheet_name)

                # self.RegInfo=self.PFE_File_dict['PFE_Defaults']
                RegPath='C:\\Users\\user\\Documents\\projects\\pfe_shuttle\\Results\\PFE_Calibration.xlsx'
                regs_sheet_name='PFE3_Calibration_GM'
                self.RegInfo=self.excelIO.ReadFromExistedFile(RegPath,sheet_name=regs_sheet_name)
            else:
                RegPath='C:\\Users\\Oryx\\Documents\\python3sv\\PFE_Shutle\\PFE_Defaults.xlsx'
                regs_sheet_name='PFE_Defaults'
                self.RegInfo=self.excelIO.ReadFromExistedFile(RegPath,sheet_name=regs_sheet_name)

            self.RegInfo_Defaults = self.RegInfo.copy()

            ##Create FullFeed

            self.DefaultFF = self.fnFullFeed("Defaults")

            ##Create default  Buffer
            self.DefaultOutBuffer=self.CreateOutBuffer(self.DefaultFF, buf_range=16, reverse=False)

            #self.DefaultFF["Defaults"].values.astype(int)

        except:
            raise


        self.PfeAccess=BaseAccess.PFE()

        self.DacAccess=BaseAccess.DAC(self.PfeAccess.dev_handler)

    def write(self,pfe_select=3,ConfigName="Debug"):#(self,pfe_select=3,Out_buffer=None,FullFeed=None,ConfigName="Debug"):
        """

        :return:

        """

        # self.PfeAccess.setPFE(pfe_select)  ##Missed Function

        #if FullFeed is None:
        FullFeed = self.fnFullFeed(ConfigName=ConfigName)

        Out_buffer = self.CreateOutBuffer(DBFullFeed=FullFeed, FFname=ConfigName, buf_range=16, reverse=False)

        out_buffer = BaseAccess.array('B',Out_buffer)

        FF_out=self.PfeAccess.write_validate_sr(pfe_select,out_buffer)

        if not FF_out:
            print("Register Write Failed !!")

        return(FF_out)

    def write_defaults(self,pfe_select=3):

        """
        Write defaults for selected pfe
        """

        ##Select PFE

        #self.PfeAccess.setPFE(pfe_select)##Missed Function

        out_buffer = BaseAccess.array('B', self.DefaultOutBuffer)

        FF_out = self.PfeAccess.write_validate_sr(pfe_select, out_buffer)

        if not FF_out:
            print("Register Write Failed !!")

        return(FF_out)


    def fnFullFeed(self,ConfigName='Debug'):
        """
        Input pandas DataFrame example

                       Value	Start	Stop
        RegName

        AMP_ATT_3bit	1	       0	3

        AUXEN	        0	       3	4
        """
        fullfeed = ''
        DBFullFeed = IOFile.pd.DataFrame()

        for idx,RegName in enumerate(self.RegInfo.index):

            #RegLen = self.RegInfo.loc[RegName].Stop - self.RegInfo.loc[RegName].Start

            reg_value=bin(self.RegInfo.loc[RegName].Value)[2:]

            if len(reg_value)>self.RegInfo.loc[RegName].Bits:

                print("ALERT!!! - you tying to set ILEGAL value !!!")

                raise("Wrong Input Value")

                new_value=raw_input("Please set the right integer value for Register %s :"%RegName)

                reg_value = bin(new_value)[2:]

            reg_value=reg_value.zfill(self.RegInfo.loc[RegName].Bits)

            if len(reg_value)>1:

                reg_value=reg_value[::-1]

            fullfeed+=reg_value

        DBFullFeed[ConfigName] = [fullfeed]

        return(DBFullFeed)

    def CreateOutBuffer(self,DBFullFeed,FFname='Defaults',buf_range=16,reverse=False):

        out_buffer = []
        FF = DBFullFeed[FFname].values[0]
        if reverse:
            FF = FF[::-1]
        for i in range(buf_range):
            bvalue = FF[8 * i:8 * (i + 1)]
            if _debug:
                print(8 * i)
                print(8 * (i + 1))
                print(bvalue)
                print(hex(int('0b'+bvalue, 2)))
            out_buffer.append(int('0b'+bvalue, 2))

        return(out_buffer)



    def fnSetDAC(self, Gain=1, DAC_V=0.05, DAC_N = False):

        ##Set DAC###
        #self.get_pfe_dft_voltages(pfe)
        if not DAC_N:
            dac_N = int(self.DacAccess.volt_to_dac(DAC_V, 2.048) / Gain)
        else:
            dac_N = DAC_V
        self.DacAccess.DAC_Update(0,dac_N)
        return(dac_N)

    def fnSetYodaModeF1(self):
        self.RegInfo.Value.TIA_DRC1 = 64
        self.RegInfo.Value.DFT_Rsns = 1
        self.set_ana_dft_mux("AI1", "P")
        self.fnDFT_vp(1)

    def fnSetYodaModeF3(self):
        self.set_ana_dft_mux("AI1", "N")
        self.RegInfo.Value.REF_EN = 0

        self.RegInfo.Value.DFT_en_tiapn = 1
        self.RegInfo.Value.SEL_ref_vbn = 0
        self.RegInfo.Value.EN_ref_vbn = 1
        self.RegInfo.Value.DFT_SELN = 0
        self.RegInfo.Value.CMPIN_SEL = 0
        self.RegInfo.Value.CMPIN_EN = 1
        self.RegInfo.Value.CMPIP_EN = 0
        self.RegInfo.Value.CMPIP_SEL = 0

        self.write(pfe_sel)

        time.sleep(1)

    def fnCalibVpMuxConfig(self, pfe_sel, FFname='Cal', YODA_mode = False):
        #Enable P/N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1
        #Set REF to output 0.5VDD
        self.RegInfo.Value.EN_ref_vbn = 1
        self.RegInfo.Value.SEL_ref_vbn = 0
        # Changed by Michael on 08.04.19
        # self.RegInfo.Value.REF_SEL1 = 0
        # self.RegInfo.Value.REF_SEL0 = 1

        if YODA_mode:
            self.RegInfo.Value.REF_EN = 0

        #Set P/N MUX
        self.RegInfo.Value.DFT_SELP = 1
        self.RegInfo.Value.DFT_SELN = 0

        #Set CMP Mux
        self.RegInfo.Value.CMPIP_SEL = 1
        self.RegInfo.Value.CMPIN_SEL = 1
        self.RegInfo.Value.CMPIP_EN = 1
        self.RegInfo.Value.CMPIN_EN = 1
        self.write(pfe_sel)

    def fnCalibPRAMuxConfig(self, pfe_sel, FFname='Cal'):

        self.RegInfo.Value.EN_ref_vbn = 1

        #Enable P/N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        #Set P/N MUX
        self.RegInfo.Value.DFT_SELP = 2
        self.RegInfo.Value.DFT_SELN = 2

        #Set CMP Mux
        self.RegInfo.Value.CMPIP_SEL = 1
        self.RegInfo.Value.CMPIN_SEL = 1
        self.RegInfo.Value.CMPIP_EN = 1
        self.RegInfo.Value.CMPIN_EN = 1
        #Set PRA DFT ON
        self.RegInfo.Value.DFT_en_pra=1
        self.write(pfe_sel)

    def fnCalibD2SMuxConfig(self, pfe_sel, FFname='Cal'):

        # Enable P/N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        #Set REF to output 0.5VDD
        self.RegInfo.Value.EN_ref_vbn = 1
        self.RegInfo.Value.SEL_ref_vbn = 0
        #Changed by Michael on 08.04.19
        # self.RegInfo.Value.REF_SEL1 = 0
        # self.RegInfo.Value.REF_SEL0 = 1

        # Set P/N MUX
        self.RegInfo.Value.DFT_SELP = 1
        self.RegInfo.Value.DFT_SELN = 0

        # Set CMP Mux
        self.RegInfo.Value.CMPIP_SEL = 0
        self.RegInfo.Value.CMPIN_SEL = 1
        self.RegInfo.Value.CMPIP_EN = 1
        self.RegInfo.Value.CMPIN_EN = 1
        #Set PRA DFT OFF
        self.RegInfo.Value.DFT_en_pra=0

        self.write(pfe_sel)

    def fnCalibGMLPMuxConfig(self, pfe_sel, FFname='Cal'):

        self.fnOperationalMuxConfig(pfe_sel, FFname)
        
    def fnOperationalMuxConfig(self, pfe_sel, FFname='Cal'):

        # Enable P/N Mux
        self.RegInfo.Value.DFT_en_tiapn = 0

        # Set REF to output 0.5VDD
        self.RegInfo.Value.EN_ref_vbn = 1
        self.RegInfo.Value.SEL_ref_vbn = 0
        # Changed by Michael on 08.04.19
        # self.RegInfo.Value.REF_SEL1 = 0
        # self.RegInfo.Value.REF_SEL0 = 1

        # Set P/N MUX
        self.RegInfo.Value.DFT_SELP = 1
        self.RegInfo.Value.DFT_SELN = 0

        # Set CMP Mux
        self.RegInfo.Value.CMPIP_SEL = 0
        self.RegInfo.Value.CMPIN_SEL = 0
        self.RegInfo.Value.CMPIP_EN = 1
        self.RegInfo.Value.CMPIN_EN = 1

        #Set PRA DFT OFF
        self.RegInfo.Value.DFT_en_pra=0

        self.write(pfe_sel)

    def fnDFT_sen_Vnb(self, pfe_sel, FFname='DFT'):
        """
        Source -Michael

        #Enable P Mux
        DFT_EN_TIAPN = 1

        #Set TIA to mux DFT_sen to Vnb
        DFT_sel_tia_senvnb = 1
        DFT_en_tia_senvnb = 1

        #Set Positive Mux
        DFT_SELP = 0

        #Set CMP Mux
        CMPIP_SEL = 1
        CMPIP_EN = 1

        :param Register table name:
        :return:
        """
        #Enable P Mux
        self.RegInfo.Value.DFT_en_tiapn = 1
        # Set TIA to mux DFT_sen to Vnb
        self.RegInfo.Value.DFT_sel_tia_senvnb =1
        self.RegInfo.Value.DFT_en_tia_senvnb = 1

        #set positive MUX
        self.RegInfo.Value.DFT_SELP = 0

        # set CMP Mux

        self.RegInfo.Value.CMPIP_SEL = 1

        self.RegInfo.Value.CMPIP_EN = 1

        self.RegInfo.Value.CMPIN_EN = 0

        self.write(pfe_sel)


    def fnDFT_sen_sensor(self, pfe_sel, FFname='DFT'):
        """
        Source -Michael

        #Enable P Mux
        DFT_EN_TIAPN = 1

        #Set TIA to mux DFT_sen to sensor
        DFT_sel_tia_senvnb = 0
        DFT_en_tia_senvnb = 1

        #Set Positive Mux
        DFT_SELP = 0

        #Set CMP Mux
        CMPIP_SEL = 1
        CMPIP_EN = 1


        :param Register table name:
        :return:
        """
        #Enable P Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        # Set TIA to mux DFT_sen to Vnb
        self.RegInfo.Value.DFT_sel_tia_senvnb =0
        self.RegInfo.Value.DFT_en_tia_senvnb = 1

        #set positive MUX
        self.RegInfo.Value.DFT_SELP = 0

        # set CMP Mux

        self.RegInfo.Value.CMPIP_SEL = 1

        self.RegInfo.Value.CMPIP_EN = 1

        self.RegInfo.Value.CMPIN_EN = 0

        self.write(pfe_sel)


    def fnDFT_vp(self, pfe_sel, FFname='DFT'):

        """
        Source -Michael

        #Enable P Mux
        DFT_EN_TIAPN = 1

        #Set Positive Mux
        DFT_SELP = 1

        #Set CMP Mux
        CMPIP_SEL = 1
        CMPIP_EN = 1

        :param Register table name:
        :return:
        """

        # Enable P Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        # set positive MUX
        self.RegInfo.Value.DFT_SELP = 1

        # Set TIA to mux DFT_sen to Vnb
        self.RegInfo.Value.DFT_sel_tia_senvnb = 1
        self.RegInfo.Value.DFT_en_tia_senvnb = 1

        # set CMP Mux
        self.RegInfo.Value.CMPIP_SEL = 1
        self.RegInfo.Value.CMPIP_EN = 1

        self.write(pfe_sel)

    def set_ana_dft_mux(self, DFT_target, P_N_mux):
        if DFT_target == "AI1":
            self.RegInfo.Value.DFT_AI1_EN_passgate = 1
            self.RegInfo.Value.DFT_AI2_EN_passgate = 0
            self.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANO2_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANALOG_EN = 2
            if P_N_mux == "P":
                self.RegInfo.Value.DFT_ANALOG_SEL = 2
            elif P_N_mux == "N":
                self.RegInfo.Value.DFT_ANALOG_SEL = 0

        elif DFT_target == "AI2":
            self.RegInfo.Value.DFT_AI1_EN_passgate = 0
            self.RegInfo.Value.DFT_AI2_EN_passgate = 1
            self.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANO2_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANALOG_EN = 1
            if P_N_mux == "P":
                self.RegInfo.Value.DFT_ANALOG_SEL = 1
            elif P_N_mux == "N":
                self.RegInfo.Value.DFT_ANALOG_SEL = 0
        elif DFT_target == "AO1":
            self.RegInfo.Value.DFT_AI1_EN_passgate = 0
            self.RegInfo.Value.DFT_AI2_EN_passgate = 0
            self.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 1
            self.RegInfo.Value.DFT_ANO2_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANALOG_EN = 2
            if P_N_mux == "P":
                self.RegInfo.Value.DFT_ANALOG_SEL = 2
            elif P_N_mux == "N":
                self.RegInfo.Value.DFT_ANALOG_SEL = 0

        elif DFT_target == "AO2":
            self.RegInfo.Value.DFT_AI1_EN_passgate = 0
            self.RegInfo.Value.DFT_AI2_EN_passgate = 0
            self.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANO2_EN_analog_buffer = 1
            self.RegInfo.Value.DFT_ANALOG_EN = 1
            if P_N_mux == "P":
                self.RegInfo.Value.DFT_ANALOG_SEL = 1
            elif P_N_mux == "N":
                self.RegInfo.Value.DFT_ANALOG_SEL = 0
        elif DFT_target == "None":
            self.RegInfo.Value.DFT_AI1_EN_passgate = 0
            self.RegInfo.Value.DFT_AI2_EN_passgate = 0
            self.RegInfo.Value.DFT_ANO1_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANO2_EN_analog_buffer = 0
            self.RegInfo.Value.DFT_ANALOG_EN = 0
        else:
            print("Choose a single target: AI1/AI2/AO1/AO2/None")

    def fnDFT_prap(self, pfe_sel, FFname='DFT'):
        """
        Source -Michael

        #Enable P Mux
        DFT_EN_TIAPN = 1

        #Set PRA to DFT mode
        DFT_en_pra = 1

        #Set Positive Mux
        DFT_SELP = 2

        #Set CMP Mux
        CMPIP_SEL = 1
        CMPIP_EN = 1


        :param Register table name:
        :return:
        """

        # Enable P Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        #Set PRA to DFT mode
        self.RegInfo.Value.DFT_en_pra= 1

        # Set Positive Mux
        self.RegInfo.Value.DFT_SELP = 2

        # set CMP Mux

        self.RegInfo.Value.CMPIP_SEL = 1

        self.RegInfo.Value.CMPIP_EN = 1


        self.write(pfe_sel)

    def fnDFT_vn(self, pfe_sel, FFname='DFT'):

        """
        Source -Michael

        #Enable N Mux
        DFT_EN_TIAPN = 1

        #Set Negative Mux
        DFT_SELN = 1

        #Set CMP Mux
        CMPIN_SEL = 1
        CMPIN_EN = 1

        :param Register table name:
        :return:
        """

        # Enable N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        # Set Positive Mux
        self.RegInfo.Value.DFT_SELN = 1

        # set CMP Mux

        self.RegInfo.Value.CMPIN_SEL = 1

        self.RegInfo.Value.CMPIN_EN = 1

        self.RegInfo.Value.CMPIP_EN = 0

        self.write(pfe_sel)


    def fnDFT_pran(self, pfe_sel, FFname='DFT'):

        """
        Source -Michael

        #Enable N Mux
        DFT_EN_TIAPN = 1

        #Set PRA to DFT mode
        DFT_en_pra = 1

        #Set Negative Mux
        DFT_SELN = 2

        #Set CMP Mux
        CMPIN_SEL = 1
        CMPIN_EN = 1


        :param Register table name:
        :return:
        """

        # Enable P Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        #Set PRA to DFT mode
        self.RegInfo.Value.DFT_en_pra= 1

        # Set Positive Mux
        self.RegInfo.Value.DFT_SELN = 2

        # set CMP Mux

        self.RegInfo.Value.CMPIN_SEL = 1

        self.RegInfo.Value.CMPIN_EN = 1

        self.write(pfe_sel)


    def fnDFT_DAC_THRU_N_MUX(self, pfe_sel, FFname='DFT'):

        """
        Source -Michael

        #Enable N Mux
        DFT_EN_TIAPN = 1

        #Set IV_BIAS block to mux internal dac
        SEL_dac_vbp = 0

        #Set Negative Mux
        DFT_SELN = 3

        #Set CMP Mux
        CMPIN_SEL = 1
        CMPIN_EN = 1



        :param Register table name:
        :return:
        """

        # Enable N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        self.RegInfo.Value.SEL_dac_vbp = 0

        self.RegInfo.Value.DFT_SELN = 3

        self.RegInfo.Value.CMPIN_SEL = 1

        self.RegInfo.Value.CMPIN_EN = 1

        self.RegInfo.Value.CMPIP_EN = 0

        self.write(pfe_sel)

##########
    def fnDFT_DAC_AUX_THRU_P_MUX(self, pfe_sel, FFname='DFT'):

        """
        Source -Michael

        #Enable P Mux
        DFT_EN_TIAPN = 1

        #Set IV_BIAS block to aux current source (beta mult)
        SEL_dac_vbp = 1

        #Set Positive Mux
        DFT_SELP = 3

        #Set CMP Mux
        CMPIP_SEL = 1
        CMPIP_EN = 1


        :param Register table name:
        :return:
        """

        # Enable N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        self.RegInfo.Value.SEL_dac_vbp = 1

        self.RegInfo.Value.DFT_SELP = 3

        self.RegInfo.Value.CMPIN_SEL = 1

        self.RegInfo.Value.CMPIN_EN = 1

        self.write(pfe_sel)




    def fnDFT_DAC_AUX_THRU_N_MUX(self, pfe_sel, FFname='DFT'):

        """
        Source -Michael

        #Enable N Mux
        DFT_EN_TIAPN = 1

        #Set IV_BIAS block to aux current source (beta mult)
        SEL_dac_vbp = 1

        #Set Negative Mux
        DFT_SELN = 3

        #Set CMP Mux
        CMPIN_SEL = 1
        CMPIN_EN = 1

        :param Register table name:
        :return:
        """

        # Enable N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        self.RegInfo.Value.SEL_dac_vbp = 1

        self.RegInfo.Value.DFT_SELN = 3

        self.RegInfo.Value.CMPIN_SEL = 1

        self.RegInfo.Value.CMPIN_EN = 1

        self.RegInfo.Value.CMPIP_EN = 0

        self.write(pfe_sel)

    def fnDFT_vbn(self, pfe_sel, FFname='DFT'):

        """
        Source -Michael

        #Enable N Mux
        DFT_EN_TIAPN = 1

        #Set ref_out Mux
        SEL_ref_vbn = 1
        EN_ref_vbn = 1

        #Set Negative Mux
        DFT_SELN = 0

        #Set CMP Mux
        CMPIN_SEL = 1
        CMPIN_EN = 1


        :param Register table name:
        :return:
        """

        # Enable N Mux
        self.RegInfo.Value.DFT_en_tiapn = 1

        self.RegInfo.Value.SEL_ref_vbn = 1

        self.RegInfo.Value.EN_ref_vbn = 1

        self.RegInfo.Value.DFT_SELN = 0

        self.RegInfo.Value.CMPIN_SEL = 1

        self.RegInfo.Value.CMPIN_EN = 1

        self.RegInfo.Value.CMPIP_EN = 0

        self.write(pfe_sel)

    def fnDFT_REF_OUT(self, pfe_sel, FFname='DFT'):
        """
        Source -Michael

        #Enable N Mux
        DFT_EN_TIAPN = 1

        #Set ref_out Mux
        SEL_ref_vbn = 0
        EN_ref_vbn = 1

        #Set Negative Mux
        DFT_SELN = 0

        #Set CMP Mux
        CMPIN_SEL = 1
        CMPIN_EN = 1

        :param Register table name:
        :return:
        """
        # Enable P Mux

        self.RegInfo.Value.DFT_en_tiapn = 1

        self.RegInfo.Value.SEL_ref_vbn = 0

        self.RegInfo.Value.EN_ref_vbn = 1

        self.RegInfo.Value.DFT_SELN = 0

        self.RegInfo.Value.CMPIN_SEL = 1

        self.RegInfo.Value.CMPIN_EN = 1

        self.RegInfo.Value.CMPIP_EN = 0

        self.write(pfe_sel)



    def fnDFT_D2S_OUT(self, pfe_sel, FFname='DFT'):

        """
        #Set CMP Mux
        CMPIP_SEL = 0
        CMPIP_EN = 1

        :param FFname:
        :return:
        """

        # Enable P Mux

        self.RegInfo.Value.CMPIP_SEL = 0

        self.RegInfo.Value.CMPIP_EN = 1

        # self.RegInfo.Value.CMPIN_EN = 0

        self.write(pfe_sel)

    def fnDFT_GM_LP(self, pfe_sel, FFname='DFT'):

        """
        #Set CMP Mux
        CMPIN_SEL = 0
        CMPIN_EN = 1

        :param FFname:
        :return:
        """

        # Enable N Mux

        self.RegInfo.Value.CMPIN_SEL = 0

        self.RegInfo.Value.CMPIN_EN = 1

        # Disable P Mux

        self.RegInfo.Value.CMPIP_EN = 0

        self.write(pfe_sel)

    def getCompOut_PE(self, pfe_num):
        cmp_out_f, sr_data_out_f =self.PfeAccess.port_extender.read_port(1)
        return cmp_out_f[3-pfe_num]

def main(RegPath=r'D:\sharedrive\projects\pfe_shuttle\Configurations\PFE_Defaults.xlsx'):

    pfell=PFE_Low_Level(RegPath)
    pfell.write_defaults(3)
    #time.sleep(0.1)

    ConfigName="Debug"

    # pfell.RegInfo.Value.DFT_clk_out = 0
    # pfell.RegInfo.Value.DFT_Rsns = 1
    # pfell.RegInfo.Value.TIA_DRC1 = 1

    #pfell.fnDFT_vp(3)


    #FullFeed = pfell.fnFullFeed(ConfigName=ConfigName)
    #out_buffer = pfell.CreateOutBuffer(DBFullFeed=FullFeed, FFname=ConfigName, buf_range=16, reverse=False)

    #write_ok = pfell.write(3)

    #print(write_ok)

if __name__ == '__main__':

    main()
