import VISADriver.VisaInterface as VISAHandel

class clsKeithley_3390_Generator_50MGHZ():
    __Instrument=0
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="5"):
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


    def fnSetFrequency(self,Frequency="'0.0"):
        VISAHandel.WriteSCPICmd(self.__Instrument,"FREQuency " + Frequency)

    def fnGetPeriod(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"PULSe:PERiod?")

    def fnGetFrequency(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"FREQuency?")

    def fnSetAmplitude(self,Amplitude="'0.0"):
        VISAHandel.WriteSCPICmd(self.__Instrument,"VOLTage " + Amplitude )


    def fnSetFunction(self,Function=''):
        """{SINusoid | SQUare | RAMP |PULSe | NOISe | DC | USER
        """
        VISAHandel.WriteSCPICmd(self.__Instrument,"FUNCtion " + str(Function))

    def fnSetOutputOffset(self,Offset="'0.0"):
        VISAHandel.WriteSCPICmd(self.__Instrument,"VOLTage:OFFSet" + Offset)

    def fnOutputLoad(self,LOAD):
        """
        {<ohms> | INFinity|
         MINimum | MAXimum
        """
        VISAHandel.WriteSCPICmd(self.__Instrument,"OUTPut:LOAD " + str(LOAD))


    def fnOutputOnOff(self, OUT):
        VISAHandel.WriteSCPICmd(self.__Instrument,"OUTPut " + str(OUT))








