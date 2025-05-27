import os,sys
sys.path.append(r'C:\Users\User\Documents\Product\PixelScanShuttle\python3sv\Equipment')
import VISADriver.VisaInterface as VISAHandel
import pandas as pd
import pylab
from os.path import join
import struct
import re
import visa
import time

rm = visa.ResourceManager()

ControllerID='0'
TCPIPAddress='10.99.10.203'

#global Instrument

#Instrument=rm.open_resource('TCPIP'+ControllerID+'::'+TCPIPAddress+"::inst"+ControllerID+"::INSTR")

Instrument = VISAHandel.ConnectToLocalLANInstrument(ControllerID="0", TCPIPAddress=TCPIPAddress)

print(Instrument)


# global Instrument
#
# Instrument=rm.open_resource('TCPIP'+ControllerID+'::'+TCPIPAddress+"::inst"+ControllerID+"::INSTR")
#
# print(Instrument)



def main_get_data_via_Ethernet(source = "CHANnel1", format = "CSV",length=50000, folder="_",savepath=r"C:\Debug\DATA.csv",plotData=False):

    df=pd.DataFrame()

    Instrument.write(":SAVE:WAVeform:FORMat %s"%format)

    Instrument.write(":WAVeform:SOURce %s" % source)

    Instrument.write(":SAVE:WAVeform:LENGth %d" % length)

    temp_data=fnGetScopeDataBytes()

    # j = 0
    # #Instrument.query("*OPC?")
    # busy = Instrument.query("*OPC?")
    # while (busy.strip() == "0") and (j < 50):
    #     busy = Instrument.query("*OPC?")
    #     time.sleep(0.15)
    #     j += 1

    data = Extract_Byte_Data(temp_data)

    df['DATA']=data

    df.to_csv(savepath,index=False)

    if plotData:

        pylab.plot(data)

        pylab.show()

    #print(data)



def main_save_to_drive(source = "CHANnel1", format = "CSV",length=50000, FREQ=None ,folder="_"):

    if FREQ is None:
        FREQ="NoInput"
        VISAHandel.QuerySCPICmd(Instrument,":WGEN:OUTPut 0")
    else:
        VISAHandel.QuerySCPICmd(Instrument,":WGEN:FREQuency %d" % FREQ)
        VISAHandel.QuerySCPICmd(Instrument,":WGEN:OUTPut 1")

    VISAHandel.QuerySCPICmd(Instrument,":SAVE:WAVeform:FORMat %s"%format)

    VISAHandel.QuerySCPICmd(Instrument,":WAVeform:SOURce %s" % source)

    VISAHandel.QuerySCPICmd(Instrument,":SAVE:WAVeform:LENGth %d" % length)

    for i in range(1,2,1):

        VISAHandel.QuerySCPICmd(Instrument,":SINGle")

        if format=="CSV":
            filename = join(folder,'Sensor_250ohm_50Mgs_%s_iter%d.csv'%(FREQ, i))
        elif format=="BINary":
            filename = join(folder,'Sensor_250ohm_50Mgs_%s_iter%d.bin'%(FREQ, i))

        VISAHandel.QuerySCPICmd(Instrument,":SAVE:WAVeform:FORMat %s" % format)
        time.sleep(0.15)
        VISAHandel.QuerySCPICmd(Instrument,":SAVE:WAVeform '%s'" % filename)

        j = 0
        time.sleep(0.1)
        busy =VISAHandel.QuerySCPICmd(Instrument,"*OPC?")
        while(busy.strip() =="0") and (j < 50):
            busy = VISAHandel.QuerySCPICmd(Instrument,"*OPC?")
            time.sleep(0.15)
            j += 1

        VISAHandel.QuerySCPICmd(Instrument,":RUN")

        time.sleep(0.1)



def main(source,NumSegments):


    #VISAHandel.QuerySCPICmd(Instrument, ":SAVE:WAVeform:FORMat BINary")
    Instrument.write(":SAVE:WAVeform:FORMat BINary")
    Instrument.write(":WAVeform:FORMat BYTE")
    Instrument.write(":ACQuire:MODE SEGMented")
    #VISAHandel.QuerySCPICmd(Instrument, ":WAVeform:FORMat BYTE")

    Instrument.write(":WAVeform:SOURce %s"%source)

    Instrument.write(":ACQuire:SEGMented:COUNt %d"%NumSegments)

    Instrument.write(":RUN")
    #Instrument.write(":WMEMory1:SAVE %s"%source)

    start1 = time.clock()
    segmented_data = []
    with open(r'C:\Users\User\Documents\Product\results\debug2.txt', 'wb') as f:
        for index in range(30):
            #start2=time.clock()
            Instrument.write(":ACQuire:SEGMented:INDex %d" % (index + 1))
            #VISAHandel.QuerySCPICmd(Instrument,":ACQuire:SEGMented:INDex %d"%(index+1))
            temp_data = fnGetScopeDataBytes()

            f.write(temp_data)

            #print(temp_data)

            j = 0
            busy = VISAHandel.QuerySCPICmd(Instrument, "*OPC?")
            while (busy == "0") and (j < 10):
                busy = VISAHandel.QuerySCPICmd(Instrument, "*OPC?")
                time.sleep(0.001)
                j += 1
            # stop2=time.clock()
            # print(stop2-start2)
            # segmented_data.append(temp_data)
    stop1 = time.clock()
    print("The all  Loop ", stop1 - start1)


    #Data = Extract_Byte_Data(temp_data)

    #print(Data)



def fnGetScopeDataBytes():

    Instrument.write("WAVeform:DATA?")


    temp_data = Instrument.read_raw()

    return(temp_data)


def Extract_Byte_Data(ByteData):

    ByteData = ByteData.strip()
    success=True
    index=1
    while success:
        try:
            header=ByteData[0:index].decode('utf-8')
            index += 1
        except:
            success = False
            index-=1

    success = True
    #i=0
    #while success
    if header[1:].isalnum():
        print(header)
    else:
        header=header[0:-1]
        index-=1

    data = ByteData[index+1:]

    #data_len = int(header[5:index])

    data_out = struct.unpack("B"*len(data), data)

    return(list(data_out))





if __name__ == '__main__':


    source = "CHANnel2";


    format = "BINary";
    length = 20000;
    FREQ = None;
    filename = r'\usb\Gold3'
    itterations=30

    plotData=False

    for i in range(itterations):
        savepath = r'C:\Debug\DATA_dummy_no_ni_wide%d.csv'%(i+1)
        main_get_data_via_Ethernet(source,format,length,filename,savepath,plotData)

    del Instrument
    #main_save_to_drive(source,format,length,FREQ,filename)
    #main_segmented(source=source)
