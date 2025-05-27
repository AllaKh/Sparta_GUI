import VISADriver.VisaInterface as VISAHandel

class clsKeithley_2000_DMM():
    __Instrument=0
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="11"):
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

    def fnGetVoltage(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,":MEASure:VOLTage:DC?")

    def fnGetCurrent(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:CURRent:DC?")

if __name__=='__main__':

        temp=clsKeithley_2000_DMM(Address="5")