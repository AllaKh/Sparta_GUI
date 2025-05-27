import VISADriver.VisaInterface as VISAHandel

class clsKeithley_2200_30_5_PS():
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

    def fnGetVoltage(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASure:VOLTage:DC?")

    def fnGetCurrent(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASure:CURRent:DC?")

    def fnSetVoltage(self, Volt="0.0"):
        if type(Volt) == str:VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:LEVel "+Volt)
        else:VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:LEVel "+str(Volt))

    def fnSetVoltageLimit(self, Lim="2.0"):
        if type(Lim) == str:VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:RANGe "+Lim)
        else:VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:RANGe "+str(Lim))

    def fnSetCurrent(self, Curr="0.0"):
        if type(Curr) == str:VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:CURRent:LEVel "+Curr)
        else:VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:CURRent:LEVel "+str(Curr))

    def fnOutputOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:OUTPut:STATe ON")

    def fnOutputOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:OUTPut:STATe OFF")