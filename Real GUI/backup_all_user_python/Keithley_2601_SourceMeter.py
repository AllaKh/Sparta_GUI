
import VISADriver.VisaInterface as VISAHandel

class clsKeithley_2601_SourceMeter():
    __Instrument=0
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="13"):
        global Instrument
        if ConnecationType=="GPIB":
            self.__Instrument = VISAHandel.ConnectToGPIBInstrument(ControllerID, Address)
        else:
            self.__Instrument = VISAHandel.ConnectToLANInstrument(ControllerID, Address)

    def fnIDNInstrument(self):
        return VISAHandel.IDNInstrument(self.__Instrument)

    def fnRSTInstrument(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"*RST")

    def fnTSTInstrument(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"*TST?")

    def fnRstChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.reset()")

    def fnRstChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.reset()")

    def fnOutputChAOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.output =smua.OUTPUT_ON")

    def fnOutputChBOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.output =smub.OUTPUT_ON")

    def fnOutputChAOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.output =smua.OUTPUT_OFF")

    def fnOutputChBOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.output =smub.OUTPUT_OFF")

    def fnReadVoltageChA(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smua.measure.v())")

    def fnReadCurrentChA(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smua.measure.i())")

    def fnReadVoltageChB(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smub.measure.v())")

    def fnReadCurrentChB(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smub.measure.i())")

    def fnSetVoltageSourceChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.func = smua.OUTPUT_DCVOLTS")

    def fnSetVoltageSourceChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.func = smub.OUTPUT_DCVOLTS")

    def fnSetCurrentSourceChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.func = smua.OUTPUT_DCAMPS")

    def fnSetCurrentSourceChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.func = smub.OUTPUT_DCAMPS")

    def fnSetVoltageChA(self, Volt=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.levelv = "+str(Volt))

    def fnSetVoltageChB(self, Volt=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.levelv = "+str(Volt))

    def fnSetSourceAutoRangeVoltageChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.autorangev = smua.AUTORANGE_ON")

    def fnSetSourceAutoRangeVoltageChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.autorangev = smub.AUTORANGE_ON")

    def fnSetCurrentChA(self, Curr=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.leveli = "+str(Curr))

    def fnSetCurrentChB(self, Curr=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.leveli = "+str(Curr))

    def fnSetSourceAutoRangeCurrentChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.autorangei = smua.AUTORANGE_ON")

    def fnSetSourceAutoRangeCurrentChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.autorangei = smub.AUTORANGE_ON")

    def fnSetMeasureAutoRangeVoltageChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.autorangev = smua.AUTORANGE_ON")

    def fnSetMeasureAutoRangeVoltageChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.autorangev = smub.AUTORANGE_ON")

    def fnSetMeasureAutoRangeCurrentChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.autorangei = smua.AUTORANGE_ON")

    def fnSetMeasureAutoRangeCurrentChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.autorangei = smub.AUTORANGE_ON")
