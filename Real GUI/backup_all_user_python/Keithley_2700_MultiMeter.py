
import VISADriver.VisaInterface as VISAHandel

class clsKeithley_2700_MultiMeter():
    """This class is a driver for the Keithley 2700 MultiMeter/ Data acquisition
    system. a "K2700" instance inherint the class by default. """
    __Instrument=0
    def __init__(self, ControllerID="3", ConnecationType="GPIB",Address="18"):
        global Instrument
        if ConnecationType=="GPIB":
            self.__Instrument = VISAHandel.ConnectToGPIBInstrument(ControllerID, Address)
        else:
            self.__Instrument = VISAHandel.ConnectToLANInstrument(ControllerID, Address)


    def fnIDNInstrument(self):
        """Send an Identification query for the device"""
        return VISAHandel.IDNInstrument(self.__Instrument)

    def fnRSTInstrument(self):
        """Reset the device"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"*RST")

    def fnGetVoltageDC(self):
        """Measure the DC voltage"""
        self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:VOLT:DC?")
        return self[0:self.find("VDC")]

    def fnGetVoltageDCChannel(self,Channel):
        """Measure the DC voltage of a channel. selected channel must be between 1:20"""
        if (VISAHandel.QuerySCPICmd(self.__Instrument,"SYST:FRSW?")=='1'):
            print "Press the INPUTS key for rear panel operation!"
            return
        else:
            if (Channel>=1 and Channel<=9):
                self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:VOLT:DC? (@10%d)"%Channel)
            else:
                self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:VOLT:DC? (@1%d)"%Channel)
        print self[0:self.find("VDC")]

    """def fnGetCurrentDCChannel(self,Channel):
        """Measure the DC current of a channel. selected channel must be between 1:20"""
        if (VISAHandel.QuerySCPICmd(self.__Instrument,"SYST:FRSW?")=='1'):
            print "Press the INPUTS key for rear panel operation!"
            return
        else:
            if (Channel>=1 and Channel<=9):
                self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:CURR:DC? (@10%d)"%Channel)
            else:
                self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:CURR:DC? (@1%d)"%Channel)
        print self[0:self.find("ADC")]"""

    def fnGetCurrentDC(self):
        """Measure the DC current"""
        self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:CURR:DC?")
        print self[0:self.find("ADC")]

    def fnGetResistance2wire(self):
        """Measure the resistance by the 2-wire method (R>1kOHM)"""
        self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:RES?")
        print self[0:self.find("OHM")]

    def fnGetResistance4wire(self):
        """Measure the resistance by the 4-wire method (R<1kOHM)"""
        self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:FRES?")
        print self[0:self.find("OHM4W")]

    def fnGetFrequency(self):
        """Measure the frequency"""
        self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:FREQ?")
        print self[0:self.find("HZ")]

    def fnGetselfrature(self):
        """Measure the selfrature"""
        self=VISAHandel.QuerySCPICmd(self.__Instrument,"MEAS:TEMP?")
        print self[0:self.find(",")]

    def TEST(self):
        self=(VISAHandel.QuerySCPICmd(self.__Instrument,"SYST:FRSW?"))
        return self


K2700=clsKeithley_2700_MultiMeter('3','GPIB','18')
K2700.fnGetVoltageDCChannel(1)
