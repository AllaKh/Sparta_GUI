
import VISADriver.VisaInterface as VISAHandel


class clsTektronix_6804b_Digital_Storage_oscilloscope():
    __Instrument=None
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="30"):
        global Instrument
        #print "*** Connecting to Tektronix Scope..."
        if ConnecationType=="GPIB":

            self.__Instrument = VISAHandel.ConnectToGPIBInstrument(ControllerID, Address)

        else:

            self.__Instrument = VISAHandel.ConnectToLocalLANInstrument(ControllerID, Address)

        #else:
        #    self.__Instrument = VISAHandel.ConnectToLANInstrument(ControllerID, Address)

    def fnGetInstrumentObj(self):
        return self.__Instrument

    def fnIDNInstrument(self):
        return VISAHandel.IDNInstrument(self.__Instrument)

    def fnRSTInstrument(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"*RST")

    def fnTSTInstrument(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"*TST?")

    def fnIsBusy(self):
        Busy = VISAHandel.QuerySCPICmd(self.__Instrument,"BUSY?")
        if Busy.isdigit():
            Busy = int(Busy)
        else: return True # if not int then means still busy
        if Busy:
            return True
        return False

    def fnRecallSetup(self, FileName):
        VISAHandel.WriteSCPICmd(self.__Instrument,"RECALL:SETUp "+FileName)
        time.sleep(5)

    def fnGetSaveWFFormat(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"SAVe:WAVEform:FILEFormat?")

    def fnSetSaveWFFormat(self, FormatType):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SAVe:WAVEform:FILEFormat "+FormatType)

    def fnSaveWF(self, Ch, FileName):
        VISAHandel.WriteSCPICmd(self.__Instrument,"SAVe:WAVEform %s,%s" % (Ch, FileName) )
        time.sleep(5)

    def fnGetSaveWFDataStart(self):
        VISAHandel.WriteSCPICmd(self.__Instrument, "DATa:STARt?")

    def fnSetSaveWFDataStart(self, StartPostion):
        VISAHandel.WriteSCPICmd(self.__Instrument, "DATa:STARt %d" % StartPostion)

    def fnGetSaveWFDataStop(self):
        VISAHandel.WriteSCPICmd(self.__Instrument, "DATa:STOP?")

    def fnSetSaveWFDataStop(self, StopPostion):
        VISAHandel.WriteSCPICmd(self.__Instrument, "DATa:STOP %d" % StopPostion)

    def fnExportWF(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"EXPort STArt")
        time.sleep(5)

    def fnGetAcquireState(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"ACQuire:STATE?")

    def fnSetAcquireState(self, AcquireState):
        if ((AcquireState=='ON') or (AcquireState=='OFF') or (AcquireState=='STOP') or (AcquireState=='RUN') or ((str(AcquireState)).isdigit()) ):
            return VISAHandel.WriteSCPICmd(self.__Instrument,"ACQuire:STATE "+AcquireState)
        return False

    def fnGetAcquireStopAfter(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"ACQuire:STOPAfter?")

    def fnSetAcquireStopAfter(self, AcquireSeq):
        if ((AcquireSeq=='RUNSTOP') or (AcquireSeq=='SEQUENCE')):
            return VISAHandel.WriteSCPICmd(self.__Instrument,"ACQuire:STOPAfter " + AcquireSeq )
        return False

    def fnMeasurmentMeanValue(self, Slot):
        return VISAHandel.QuerySCPICmd(self.__Instrument, "MEASUrement:MEAS"+str(Slot)+":MEAN?")







