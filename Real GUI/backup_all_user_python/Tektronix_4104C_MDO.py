import VISADriver.VisaInterface as VISAHandel
import time

class clsTektronix_4104C_MDO():

    Instrument=None
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="30"):

        if ConnecationType == "GPIB":
            self.Instrument = VISAHandel.ConnectToGPIBInstrument(ControllerID, Address)
        else:
            self.Instrument = VISAHandel.ConnectToLocalLANInstrument(ControllerID, Address)

        # else:
        #     self.Instrument = VISAHandel.ConnectToLANInstrument(ControllerID, Address)

    def fnGetInstrumentObj(self):
        return self.Instrument

    def fnIDNInstrument(self):
        return VISAHandel.IDNInstrument(self.Instrument)


    def fnSetWFDataStart(self, StartPostion):
        VISAHandel.QuerySCPICmd(self.Instrument, "DATa:STARt %d" % StartPostion)

    def fnSetWFDataStop(self, StopPostion):
        VISAHandel.QuerySCPICmd(self.Instrument, "DATa:STOP %d" % StopPostion)

    def fnSetDataSource(self,source):
        """
        :DATa:SOUrce D5
        :DATa:START 1
        :DATa:STOP 25
        :WFMOutpre:ENCdg ASCii
        :WFMOutpre:BYT_Nr 1
        :HEADer 1
        :VERBose 1
        :WFMOutpre? Returns the following values. Each value represents the current settings that
        a CURVe? query will use to format the data that will be transferred from the
        oscilloscope to a PC or other device (see next table for explanations):
        :WFMOUTPRE:BYT_NR 1;BIT_NR 8;ENCDG ASCII;BN_FMT
        RI;BYT_OR MSB;WFID "D5, unknown coupling,
        100.0us/div, 10000 points, Digitalmode";NR_PT 25;PT_FMT
        Y;PT_ORDER LINEAR;XUNIT "s";XINCR 100.0000E-9;XZERO
        -500.0000E-6;PT_OFF 0;YUNIT "State";YMULT 1.0000;YOFF
        0.0E+0;YZERO 0.0E+0
        :CURVe? Returns the following values. Each value represents a data point:
        :CURVe 0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0

        :return:
        """
        VISAHandel.QuerySCPICmd(self.Instrument, ":DATa:SOUrce %s" % source)
    def fnGetScopeData(self,source,filename):

        VISAHandel.QuerySCPICmd(self.Instrument,"SAVe:WAVEform %s,'%s'" % (source, filename))
        time.sleep(1)
        Busy = VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?")
        while Busy!=0:
            print("I am waiting the Scope to save the file !!!")
            try:
                Busy = int(VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?"))
            except:
                Busy=0
            time.sleep(5)

        # pdb.set_trace()
        data = VISAHandel.QuerySCPICmd(self.Instrument,"FILESystem:READFile '%s'" % filename)

        return(data)

    def fnGetLogicData(self,source,filename):# , source, start, stop):
        """
        #SAVe:EVENTtable:{BUS<x>|B<x>} <file path>

        FILESystem:READFile <QString>
        """

        if _debug:
            VISAHandel.QuerySCPICmd(self.Instrument, "SAVe:EVENTtable:%s '%s'"%(source,filename))
            Busy=VISAHandel.QuerySCPICmd(self.Instrument,"BUSY?")
            while Busy.strip()!="0":
                print("I am waiting the Scope to save the file !!!")
                Busy = int(VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?"))
                time.sleep(0.1)
            time.sleep(4)
            data = VISAHandel.QuerySCPICmd(self.Instrument,"FILESystem:READFile '%s'" % filename)
        else:
            VISAHandel.QuerySCPICmd(self.Instrument, "SAVe:EVENTtable:%s '%s'" % (source, filename))
            Busy=int(VISAHandel.QuerySCPICmd(self.Instrument,"BUSY?"))
            while Busy!=0:
                print("I am waiting the Scope to save the file !!!")
                Busy = int(VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?"))
                time.sleep(0.1)
            time.sleep(4)
            data = VISAHandel.QuerySCPICmd(self.Instrument,"FILESystem:READFile '%s'" % filename)
        return(data)


    def fnRSTInstrument(self):

        VISAHandel.WriteSCPICmd(self.Instrument,"*RST")

    def fnTSTInstrument(self):

        return VISAHandel.QuerySCPICmd(self.Instrument,"*TST?")

    def fnIsBusy(self):
        Busy = VISAHandel.QuerySCPICmd(self.Instrument,"BUSY?")
        if Busy.isdigit():
            Busy = int(Busy)
        else: return True # if not int then means still busy
        if Busy:
            return True
        return False

    def fnRecallSetup(self, FileName):
        VISAHandel.WriteSCPICmd(self.Instrument,"RECALL:SETUp "+FileName)
        time.sleep(5)

    def fnGetSaveWFFormat(self):
        return VISAHandel.QuerySCPICmd(self.Instrument,"SAVe:WAVEform:FILEFormat?")

    def fnSetSaveWFFormat(self, FormatType):
        VISAHandel.WriteSCPICmd(self.Instrument,"SAVe:WAVEform:FILEFormat "+FormatType)

    def fnSaveWF(self, Ch, FileName):
        VISAHandel.WriteSCPICmd(self.Instrument,"SAVe:WAVEform %s,%s" % (Ch, FileName) )
        time.sleep(5)

#    SAVe:WAVEform:FILEFormat
#    {INTERNal | SPREADSheet}print

    def fnGetSaveWFDataStart(self):
        VISAHandel.WriteSCPICmd(self.Instrument, "DATa:STARt?")

    def fnSetSaveWFDataStart(self, StartPostion):
        VISAHandel.WriteSCPICmd(self.Instrument, "DATa:STARt %d" % StartPostion)

    def fnGetSaveWFDataStop(self):
        VISAHandel.WriteSCPICmd(self.Instrument, "DATa:STOP?")

    def fnSetSaveWFDataStop(self, StopPostion):
        VISAHandel.WriteSCPICmd(self.Instrument, "DATa:STOP %d" % StopPostion)

    def fnExportWF(self):
        VISAHandel.WriteSCPICmd(self.Instrument,"EXPort STArt")
        time.sleep(5)

    def fnGetAcquireState(self):
        return VISAHandel.QuerySCPICmd(self.Instrument,"ACQuire:STATE?")

    def fnSetAcquireState(self, AcquireState):
        if ((AcquireState=='ON') or (AcquireState=='OFF') or (AcquireState=='STOP') or (AcquireState=='RUN') or ((str(AcquireState)).isdigit()) ):
            return VISAHandel.WriteSCPICmd(self.Instrument,"ACQuire:STATE "+AcquireState)
        return False

    def fnGetAcquireStopAfter(self):
        return VISAHandel.QuerySCPICmd(self.Instrument,"ACQuire:STOPAfter?")

    def fnSetAcquireStopAfter(self, AcquireSeq):
        try:
            VISAHandel.WriteSCPICmd(self.Instrument, "ACQuire:STOPAfter " + AcquireSeq)
        except:
            raise
        # if ((AcquireSeq=='RUNSTOP') or (AcquireSeq=='SEQUENCE')):
        #     return
        return False

    def fnMeasurmentMeanValue(self, Slot):
        return VISAHandel.QuerySCPICmd(self.Instrument, "MEASUrement:MEAS"+str(Slot)+":MEAN?")


