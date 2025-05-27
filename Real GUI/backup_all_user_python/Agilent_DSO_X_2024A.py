import VISADriver.VisaInterface as VISAHandel
import time
_debug=False
class clsAgilent_DSO_X_2024A():

    Instrument=None
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="30"):

        if ConnecationType == "GPIB":
            self.Instrument = VISAHandel.ConnectToGPIBInstrument(ControllerID, Address)
        else:
            self.Instrument = VISAHandel.ConnectToLocalLANInstrument(ControllerID, Address)
        self.ControllerID=ControllerID
        self.Address=Address

    def fnGetInstrumentObj(self):
        return self.Instrument

    def fnIDNInstrument(self):
        return VISAHandel.IDNInstrument(self.Instrument)


    def fnWGENsetFreq(self,FREQ):

        try:
            VISAHandel.QuerySCPICmd(self.Instrument, ":WGEN:FREQuency %d"%FREQ)
        except:
            raise

    def fnWGENsetFreq(self, FREQ):

        try:
            VISAHandel.QuerySCPICmd(self.Instrument, ":WGEN:FREQuency %d" % FREQ)
        except:
            raise

    def fnGetAVerageOutput(self,source='CHANnel2'):

        try:
            avgout = VISAHandel.QuerySCPICmd(self.Instrument, ":MEASure:VAVerage? %s" % source)
            attempt = 0
            while (avgout == None) and (attempt < 30):
                time.sleep(0.1)
                attempt += 1
                print("Connection lost -Reconnection attempt # %d" % attempt)
                self.Instrument = VISAHandel.ConnectToLocalLANInstrument(self.ControllerID, self.Address)
                avgout = VISAHandel.QuerySCPICmd(self.Instrument, ":MEASure:VAVerage? %s" % source)
            return (avgout)
        except:
            try:

                avgout=None
                attempt=0
                while (avgout==None) and (attempt<30):
                    time.sleep(1)
                    attempt+=1
                    print("Attempt # %d"%attempt)
                    self.Instrument = VISAHandel.ConnectToLocalLANInstrument(self.ControllerID, self.Address)
                    avgout = VISAHandel.QuerySCPICmd(self.Instrument, ":MEASure:VAVerage? %s" % source)
                return(avgout)
            except:
                print("Communication to scope fails several times!!!!")
                return False
        return(avgout)

    def fnGetScopeDataAscii(self,source,filename=''):

        VISAHandel.QuerySCPICmd(self.Instrument, "WAVeform:SOURce %s" %(source))
        VISAHandel.QuerySCPICmd(self.Instrument, "WAVeform:FORMat ASCii")
        self.Instrument.write("WAVeform:DATA?")

        time.sleep(1)
        # Busy = VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?")
        # while Busy<>0:
        #     print("I am waiting the Scope to save the file !!!")
        #     Busy = VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?")
        #     time.sleep(0.1)

        temp_data = self.Instrument.read_raw()

        temp_data=temp_data.strip()

        if _debug:
            print(temp_data[0:100])

        index_8000 = temp_data.index("#")
        try:
            index_bytedata=min(temp_data.index(" "),temp_data.index("-"))
        except:
            index_bytedata = temp_data.index(" ")

        data_len=int(temp_data[index_8000+5:index_bytedata])

        data_str = temp_data[index_bytedata:].split(',')

        #data=[float(d) for d in data_str]
        return(data_str)



    def fnGetScopeDataBytes(self,source,filename=''):

        import struct
        import re

        VISAHandel.QuerySCPICmd(self.Instrument, "WAVeform:SOURce %s" %(source))
        VISAHandel.QuerySCPICmd(self.Instrument, "WAVeform:FORMat BYTE")
        self.Instrument.write("WAVeform:DATA?")
        time.sleep(1)
        # Busy = VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?")
        # while Busy<>0:
        #     print("I am waiting the Scope to save the file !!!")
        #     Busy = VISAHandel.QuerySCPICmd(self.Instrument, "BUSY?")
        #     time.sleep(0.1)

        temp_data = self.Instrument.read_raw()

        temp_data=temp_data.strip()

        sp_list = re.findall('[^A-Za-z0-9]', temp_data[0:50])

        index_8000 = temp_data.index(sp_list[0])

        index_bytedata=temp_data.index(sp_list[1])

        data_len=int(temp_data[index_8000+5:index_bytedata])

        data = struct.unpack("B"*data_len,temp_data[index_bytedata:])

        return(data)

    def fnSetAcquireStopRunSingle(self, AcquireSeq):
        """

        :param AcquireSeq: Single,STOP,RUN
        :return:
        """

        if (AcquireSeq=='Single'):
            VISAHandel.WriteSCPICmd(self.Instrument,":SINGle")
        elif (AcquireSeq=='STOP'):
            VISAHandel.WriteSCPICmd(self.Instrument,":STOP")

        elif (AcquireSeq=='RUN'):
            VISAHandel.WriteSCPICmd(self.Instrument,":RUN")

        else:
            return False

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
        if ((AcquireSeq=='RUNSTOP') or (AcquireSeq=='SEQUENCE')):
            return VISAHandel.WriteSCPICmd(self.Instrument,"ACQuire:STOPAfter " + AcquireSeq )
        return False

    def fnMeasurmentMeanValue(self, Slot):
        return VISAHandel.QuerySCPICmd(self.Instrument, "MEASUrement:MEAS"+str(Slot)+":MEAN?")


