
import VISADriver.VisaInterface as VISAHandel

class clsKeithley_6487_PicoAmmeter():
    __Instrument=0
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="19"):
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

    def fnSetVoltageSourceRange(self,Range="10"):
        """ Range may be "10", "50" or "500" Volts """
        VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:RANGe " + Range )

    def fnSetVoltageSource(self,Volt="0.0"):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage " + Volt )

    def fnSetCurrentLimit(self,CurrentLimit="2.5"):
        """ Current limit may be "25e-6","250e-6", "2.5e-3" or "25e-3" Ampere """
        VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:ILIMit " + CurrentLimit )

    def fnSetVoltageSourceOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:STATe ON")

    def fnSetVoltageSourceOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SOURce:VOLTage:STATe OFF")
