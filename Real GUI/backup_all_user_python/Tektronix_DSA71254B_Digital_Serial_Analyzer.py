
import time
import VISADriver.VisaInterface as VISAHandel

class clsTektronix_DSA71254B_Digital_Serial_Analyzer():
    __Instrument=0
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="5"):
        global Instrument
        if ConnecationType=="GPIB":
            self.__Instrument = VISAHandel.ConnectToGPIBInstrument(ControllerID, Address)
            #self.fnSetInterfaceTermChars("\n")
        else:
            self.__Instrument = VISAHandel.ConnectToLANInstrument(ControllerID, Address)
            #self.fnSetInterfaceTermChars("\n")

    def fnSetInterfaceTermChars(self, Chars=""):
        VISAHandel.TermChars(self.__Instrument, Chars)

    def fnGetInstrument(self):
        return self.__Instrument

    def fnIDNInstrument(self):
        return VISAHandel.IDNInstrument(self.__Instrument)

    def fnRSTInstrument(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"*RST")
        time.sleep(3)

    def fnTSTInstrument(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"*TST?")

    def fnCheckBusy(self):
        time.sleep(0.5)# Reduse respond speed
        Stat = VISAHandel.QuerySCPICmd(self.__Instrument,"BUSY?")
        if Stat == "1":
            return True
        elif Stat == "0":
            return False
        return Stat

    def fnLoadSetup(self, Path):
        VISAHandel.WriteSCPICmd(self.__Instrument,"RECALL:SETUp "+"\""+Path+ ".set"+"\"")
        time.sleep(30)# Due to Scope responde time

    def fnMeasurementValue(self,MeasRow):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASUrement:MEAS"+str(MeasRow)+":VAL?")

    def fnMeasurementMean(self,MeasRow):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASUrement:MEAS"+str(MeasRow)+":MEAN?")

    def fnMeasurementMin(self,MeasRow):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASUrement:MEAS"+str(MeasRow)+":MINI?")

    def fnMeasurementMax(self,MeasRow):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASUrement:MEAS"+str(MeasRow)+":MAX?")

    def fnMeasurementStdDev(self,MeasRow):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASUrement:MEAS"+str(MeasRow)+":STD?")

    def fnClearDisplayPersistence(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"DISplay:PERSistence:RESET")

    def fnRUNState(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"ACQuire:STATE RUN")

    def fnSTOPState(self):

        VISAHandel.WriteSCPICmd(self.__Instrument,"ACQuire:STATE STOP")

    def fnClearPersistenceRUN(self):
        self.fnClearDisplayPersistence()
        self.fnRUNState()

    def fnSaveWaveform(self, Ch=1, Path = "C:\\TekScope\\Screen Captures\\", FileName="TEK0000.WFM"):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SAVE:WAVEFORM CH"+str(Ch)+",\""+Path+FileName+"\"")

    def fnSaveWaveformPic(self, CaptureType = "FULLNOmenu",Path = "C:\\TekScope\\Screen Captures\\REF\\ProcMonFreq", FileName="TEK0000"):
        FileName = "\"" + Path + "\\" + FileName + ".jpg\""
        VISAHandel.WriteSCPICmd(self.__Instrument,"HARDCopy:FILEName "+FileName)
        VISAHandel.WriteSCPICmd(self.__Instrument,"HARDCopy:VIEW "+CaptureType)#FULLNOmenu, FULLSCREEN
        VISAHandel.WriteSCPICmd(self.__Instrument,"HARDCopy:PORT FILE")
        VISAHandel.WriteSCPICmd(self.__Instrument,"HARDCopy START")

    def fnDPOJetPlotSavePic(self, Path = "C:\\TekScope\\Screen Captures\\REF\\ProcMonFreq\\", FileName="TEK0000", PlotNum=1):
        FileName = "\""+ Path + "\\" +FileName+".jpg\""
        VISAHandel.WriteSCPICmd(self.__Instrument,"DPOJET:EXPORT PLOT"+str(PlotNum)+", "+FileName)

    def fnDPOJetGetState(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:STATE?")

    def fnDPOJetCheckStopState(self):
        if self.fnDPOJetGetState()=="STOP":
            return True
        return False

    def fnDPOJetStateClear(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"DPOJET:STATE CLEAR")

    def fnDPOJetStateRun(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"DPOJET:STATE RUN")

    def fnDPOJetStateSingle(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"DPOJET:STATE SINGLE")

    def fnDPOJetStateRecalc(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"DPOJET:STATE RECALC")

    def fnDPOJetStateStop(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"DPOJET:STATE STOP")

    def fnDPOJetCheckError(self):
        strError = VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:LASTError?")
        strError = strError.replace("\n", "-> ")
        return strError

    def fnDPOJetClearMeasurments(self):
        """ This set-only parameter clears the entire current list of defined measurements in DPOJET """
        return VISAHandel.WriteSCPICmd(self.__Instrument,"DPOJET:CLEARALLMeas")

    def fnDPOJetGetMeasurmentMean(self, Slot=0):
        """ Returns the mean measurement for the currently loaded limit file. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:ALLAcqs:MEAN?")

    def fnDPOJetGetCurrentMeasurmentMean(self, Slot=0):
        """ Returns the mean measurement for the currently loaded limit file. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:CURRentacq:MEAN?")

    def fnDPOJetGetMeasurmentStdDev(self, Slot=0):
        """ Returns the standard deviation of the measurement value for the currently
        selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:ALLAcqs:StdDev?")

    def fnDPOJetGetCurrentMeasurmentStdDev(self, Slot=0):
        """ Returns the standard deviation of the measurement value for the currently
        selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:CURRentacq:StdDev?")

    def fnDPOJetGetMeasurmentMax(self, Slot=0):
        """ Returns the maximum value of the measurement value for the currently
        selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:ALLAcqs:MAX?")

    def fnDPOJetGetCurrentMeasurmentMax(self, Slot=0):
        """ Returns the maximum value of the measurement value for the currently
        selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:CURRentacq:MAX?")

    def fnDPOJetGetMeasurmentMin(self, Slot=0):
        """ Returns the minimum value of the measurement value for the currently
        selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:ALLAcqs:MIN?")

    def fnDPOJetGetCurrentMeasurmentMin(self, Slot=0):
        """ Returns the minimum value of the measurement value for the currently
        selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:CURRentacq:MIN?")

    def fnDPOJetGetMeasurmentPk2Pk(self, Slot=0):
        """ Returns the peak-to-peak value for the currently selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:ALLAcqs:PK2PK?")

    def fnDPOJetGetCurrentMeasurmentPk2Pk(self, Slot=0):
        """ Returns the peak-to-peak value for the currently selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:CURRentacq:PK2PK?")

    def fnDPOJetGetMeasurmentPopulation(self, Slot=0):
        """ Returns the mean measurement value for the currently selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:ALLAcqs:POPUlation?")

    def fnDPOJetGetCurrentMeasurmentPopulation(self, Slot=0):
        """ Returns the mean measurement value for the currently selected measurement for measurement slot <x>. """
        return VISAHandel.QuerySCPICmd(self.__Instrument,"DPOJET:MEAS"+str(Slot)+":RESULts:CURRentacq:POPUlation?")


    def fnSetTrigLevelA(self):
        """
        This function sets the A trigger level automatically to 50% of the range of the
        minimum and maximum values of the trigger input signal.
        """
        command= "TRIGger:A SETLevel"
        return VISAHandel.WriteSCPICmd(self.__Instrument,command)

    def fnSetMathVertScale(self, MathNum, Scale):
        """
		This command sets or queries the vertical scale of the specified math waveform.
        Example: "MATH4:VERTICAL:SCALE 100E-03" sets the Math 4 waveform scale to 100 mV per division
        """
        command= "MATH%s:VERTICAL:SCALE %s"%(str(MathNum), str(Scale))
        return VISAHandel.WriteSCPICmd(self.__Instrument,command)

    def fnClearMeasStatistics(self):
        """
        his command (no query form) clears existing measurement statistics from
        memory. This command is equivalent to selecting Measurement Setup from the
        Measure menu, selecting Statistics, and clicking the Reset button.
        """
        return VISAHandel.WriteSCPICmd(self.__Instrument,"MEASUREMENT:STATISTICS:COUNT RESET")

    def fnSetHorizontalScale(self, scale_val = 100e-6):
        """
        This func will set the horizontal scale per division
        """
        VISAHandel.WriteSCPICmd(self.__Instrument,"HORizontal:MODE:SCAle " + str(scale_val))

    def fnSetSampleRate(self, rate_val = 50e9):
        """
        This func will set the sample rate
        """
        VISAHandel.WriteSCPICmd(self.__Instrument,"HORizontal:MODE:SAMPLERate " + str(rate_val))

