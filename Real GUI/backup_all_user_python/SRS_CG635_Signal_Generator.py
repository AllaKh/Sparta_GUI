
import VISADriver.VisaInterface as VISAHandel

class clsSRS_CG635_Signal_Generator():
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

    def fnGetFreq(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"FREQ?")

    def fnSetFreq(self, Freq=123.456):
        VISAHandel.WriteSCPICmd(self.__Instrument,"FREQ "+str(Freq))

    def fnSetQOutputHigh(self, HiLevel=0.5):
        VISAHandel.WriteSCPICmd(self.__Instrument,"QOUT 1,"+str(HiLevel))

    def fnSetQOutputLow(self, LoLevel=0.0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"QOUT 0,"+str(LoLevel))

    def fnSetQOutput(self, HiLevel=0.5, LoLevel=0.0):
        self.fnSetQOutputHigh(HiLevel)
        self.fnSetQOutputLow(LoLevel)
        
    def fnGetQOutputHigh(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"QOUT1?")

    def fnGetQOutputLow(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"QOUT0?")

    def fnGetQOutput(self):
        return self.fnGetQOutputHigh(), self.fnGetQOutputLow()
        
    def fnGetSigGenOutState(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"RUNS?")

    def fnSetSigGenOutStateOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"RUNS1")

    def fnSetSigGenOutStateOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"RUNS0")
