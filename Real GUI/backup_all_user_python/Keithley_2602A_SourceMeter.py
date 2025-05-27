
import VISADriver.VisaInterface as VISAHandel

class clsKeithley_2602A_SourceMeter():
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

    def fnRstChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.reset()")

    def fnRstChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.reset()")

####

    def fnOutputChAOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.output =smua.OUTPUT_ON")

    def fnOutputChBOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.output =smub.OUTPUT_ON")

    def fnOutputChAOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.output =smua.OUTPUT_OFF")

    def fnOutputChBOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.output =smub.OUTPUT_OFF")

    def fnOutputAllOff(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.output =smua.OUTPUT_OFF")
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.output =smub.OUTPUT_OFF")

    def fnOutputAllOn(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.output =smua.OUTPUT_ON")
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.output =smub.OUTPUT_ON")

####

    def fnReadVoltageChA(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smua.measure.v())")

    def fnReadCurrentChA(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smua.measure.i())")

    def fnReadVoltageChB(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smub.measure.v())")

    def fnReadCurrentChB(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smub.measure.i())")

####

    def fnSetVoltageSourceChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.func = smua.OUTPUT_DCVOLTS")

    def fnSetVoltageSourceChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.func = smub.OUTPUT_DCVOLTS")

    def fnSetCurrentSourceChA(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.func = smua.OUTPUT_DCAMPS")

    def fnSetCurrentSourceChB(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.func = smub.OUTPUT_DCAMPS")

####

    def fnSetVoltageChA(self, Volt=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.levelv = "+str(Volt))

    def fnSetVoltageChB(self, Volt=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.levelv = "+str(Volt))

    def fnSetCurrentChA(self, Curr=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.leveli = "+str(Curr))

    def fnSetCurrentChB(self, Curr=0):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.leveli = "+str(Curr))

####

    def fnSetVoltageLimitChA(self, VoltLimit=2):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.limitv = "+str(VoltLimit))

    def fnSetVoltageLimitChB(self, VoltLimit=2):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.limitv = "+str(VoltLimit))

    def fnSetCurrentLimitChA(self, CurrLimit=10e-6):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.limiti = "+str(CurrLimit))

    def fnSetCurrentLimitChB(self, CurrLimit=10e-6):
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.limiti = "+str(CurrLimit))

    def fnReadComplianceChA(self):
        """A returned value of 'true' indicates that the voltage limit has been reached if the unit is
            configured as a current source, or that the current limit has been reached if the
            unit is configured as a voltage source. If not return 'false'."""
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smua.source.compliance)")

    def fnReadComplianceChB(self):
        """A returned value of 'true' indicates that the voltage limit has been reached if the unit is
            configured as a current source, or that the current limit has been reached if the
            unit is configured as a voltage source. If not return 'false'."""
        return VISAHandel.QuerySCPICmd(self.__Instrument,"print(smub.source.compliance)")

####

    def fnSetSourceAutoRangeVoltageChA(self):
        """Enable voltage source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.autorangev = smua.AUTORANGE_ON")

    def fnSetSourceAutoRangeVoltageChB(self):
        """Enable voltage source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.autorangev = smub.AUTORANGE_ON")

    def fnSetSourceAutoRangeCurrentChA(self):
        """Enable current source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.autorangei = smua.AUTORANGE_ON")

    def fnSetSourceAutoRangeCurrentChB(self):
        """Enable current source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.autorangei = smub.AUTORANGE_ON")

    def fnSetMeasureAutoRangeVoltageChA(self):
        """Enable voltage measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.autorangev = smua.AUTORANGE_ON")

    def fnSetMeasureAutoRangeVoltageChB(self):
        """Enable voltage measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.autorangev = smub.AUTORANGE_ON")

    def fnSetMeasureAutoRangeCurrentChA(self):
        """Enable current measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.autorangei = smua.AUTORANGE_ON")

    def fnSetMeasureAutoRangeCurrentChB(self):
        """Enable current measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.autorangei = smub.AUTORANGE_ON")

####

    def fnSetOffSourceAutoRangeVoltageChA(self):
        """Disable voltage source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.autorangev = smua.AUTORANGE_OFF")

    def fnSetOffSourceAutoRangeVoltageChB(self):
        """Disable voltage source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.autorangev = smub.AUTORANGE_OFF")

    def fnSetOffSourceAutoRangeCurrentChA(self):
        """Disable current source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.autorangei = smua.AUTORANGE_OFF")

    def fnSetOffSourceAutoRangeCurrentChB(self):
        """Disable current source auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.autorangei = smub.AUTORANGE_OFF")

    def fnSetOffMeasureAutoRangeVoltageChA(self):
        """Disable voltage measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.autorangev = smua.AUTORANGE_OFF")

    def fnSetOffMeasureAutoRangeVoltageChB(self):
        """Disable voltage measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.autorangev = smub.AUTORANGE_OFF")

    def fnSetOffMeasureAutoRangeCurrentChA(self):
        """Disable current measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.autorangei = smua.AUTORANGE_OFF")

    def fnSetOffMeasureAutoRangeCurrentChB(self):
        """Disable current measure auto range."""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.autorangei = smub.AUTORANGE_OFF")

####

    def fnSetSourceManualRangeVoltageChA(self, rangeval):
        """Enable voltage source manual range.\n100mV,1V,6V,40V"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.rangev = "+str(rangeval) )

    def fnSetSourceManualRangeVoltageChB(self, rangeval):
        """Enable voltage source manual range.\n100mV,1V,6V,40V"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.rangev = "+str(rangeval) )

    def fnSetSourceManualRangeCurrentChA(self, rangeval):
        """Enable current source manual range.\n100nA,1uA,10uA,100uA,1mA,10mA,100mA,1A,3A"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.source.rangei = "+str(rangeval) )

    def fnSetSourceManualRangeCurrentChB(self, rangeval):
        """Enable current source manual range.\n100nA,1uA,10uA,100uA,1mA,10mA,100mA,1A,3A"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.source.rangei = "+str(rangeval) )

    def fnSetMeasureManualRangeVoltageChA(self, rangeval):
        """Enable voltage measure manual range.\n100mV,1V,6V,40V"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.rangev = "+str(rangeval) )

    def fnSetMeasureManualRangeVoltageChB(self, rangeval):
        """Enable voltage measure manual range.\n100mV,1V,6V,40V"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.rangev = "+str(rangeval) )

    def fnSetMeasureManualRangeCurrentChA(self, rangeval):
        """Enable current measure manual range.\n100nA,1uA,10uA,100uA,1mA,10mA,100mA,1A,3A"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.measure.rangei = "+str(rangeval) )

    def fnSetMeasureManualRangeCurrentChB(self, rangeval):
        """Enable current measure manual range.\n100nA,1uA,10uA,100uA,1mA,10mA,100mA,1A,3A"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smub.measure.rangei = "+str(rangeval) )






# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##DC and pulsed linear staircase sweeps (A):With this type of sweep, the voltage or current
##increases or decreases in fixed steps, beginning witha start voltage or current and ending with a stop
##voltage or current. This portion of the figure (A) shows an increasing linear staircase sweep and a
##pulsed staircase sweep. Pulsed linear staircase sweeps function the same way that DC linear
##staircase sweeps function, except that pulsed linear staircase sweeps return to the idle level between
##pulses.

#  step = (stop - start) / (points - 1)

# -- Configure a sweep from 0 to 10 V in 1 V steps.

#   smua.trigger.source.linearv(0, 10, 11)
# -- Enable the source action.
#  smua.trigger.source.action = smua.ENABLE


    def fnSweepVoltConfChA(self, MinV, MaxV, Steps):
        """Enable current measure manual range.\n100nA,1uA,10uA,100uA,1mA,10mA,100mA,1A,3A"""
##        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.trigger.source.linearv = "+str(MinV),+str(MaxV),+str(Steps) )

        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.trigger.source.linearv(0, 2, 11)")


    def fnSweepVoltEnableChA(self):
        """Enable current measure manual range.\n100nA,1uA,10uA,100uA,1mA,10mA,100mA,1A,3A"""
        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.trigger.source.action = smua.ENABLE")
##        VISAHandel.WriteSCPICmd(self.__Instrument,"smua.trigger.source.linearY")


