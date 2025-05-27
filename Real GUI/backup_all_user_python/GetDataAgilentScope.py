import os,sys
import struct
import re
import visa
import time
from os.path import join

rm = visa.ResourceManager()

ControllerID='0'
TCPIPAddress='10.99.0.114'

global Instrument

Instrument=rm.open_resource('TCPIP'+ControllerID+'::'+TCPIPAddress+"::inst"+ControllerID+"::INSTR")

print(Instrument)

def main_save_to_drive(source = "CHANnel1", format = "CSV",length=50000, FREQ=None ,folder="_",FilesNum=20):

    if FREQ is None:
        FREQ="NoInput"
        Instrument.write(":WGEN:OUTPut 0")
    else:
        Instrument.write(":WGEN:FREQuency %d" % FREQ)
        Instrument.write(":WGEN:OUTPut 1")

    Instrument.write(":SAVE:WAVeform:FORMat %s"%format)

    Instrument.write(":WAVeform:SOURce %s" % source)

    Instrument.write(":SAVE:WAVeform:LENGth %d" % length)

    #Instrument.write(":SAVE:WAVeform:FORMat %s" % format)

    for i in range(1,FilesNum+1,1):

        Instrument.write(":SINGle")
        if format=="CSV":
            filename = join(folder,'Sensor_250ohm_50Mgs_%s_iter%d.csv'%(FREQ, i))
        elif format=="BINary":

            filename = join(folder,'onebit_%s.bin'%str(i).zfill(4))

        time.sleep(5)# Time it takes scope to fill the memory
        Instrument.write(":SAVE:WAVeform '%s'" % filename)
        time.sleep(45)
        Instrument.write(":RUN")
        time.sleep(2)
        # j = 0
        # time.sleep(0.1)
        # busy =Instrument.query("*OPC?")
        # while(busy.strip() =="0") and (j < 50):
        #     busy = Instrument.query("*OPC?")
        #     time.sleep(0.15)
        #     j += 1
        #
        # #Instrument.write(":RUN")
        #
        # time.sleep(0.1)


def main_segmented(source = "CHANnel1", format = "BYTE"):

    Instrument.write(":WAVeform:FORMat %s"%format)
    #VISAHandel.QuerySCPICmd(Instrument, ":WAVeform:FORMat BYTE")

    Instrument.write(":WAVeform:SOURce %s"%source)

    start1 = time.clock()
    segmented_data = []
    for index in xrange(30):
        # start2=time.clock()
        Instrument.write(":ACQuire:SEGMented:INDex %d" % (index + 1))
        # VISAHandel.QuerySCPICmd(Instrument,":ACQuire:SEGMented:INDex %d"%(index+1))
        temp_data = fnGetScopeDataBytes(source="CHANnel2")

        time.sleep(0.002)
        # stop2=time.clock()
        # print(stop2-start2)
        # segmented_data.append(temp_data)
    stop1 = time.clock()
    print("The all  Loop ", stop1 - start1)

    Data = Extract_Byte_Data(temp_data)

    print(Data)



def fnGetScopeDataBytes():

    Instrument.write("WAVeform:DATA?")

    temp_data = Instrument.read_raw()

    return (temp_data)


def Extract_Byte_Data(ByteData):

    ByteData = ByteData.strip()

    sp_list = re.findall('[^A-Za-z0-9]', ByteData[0:50])

    index_8000 = ByteData.index(sp_list[0])

    index_bytedata = ByteData.index(sp_list[1])

    data_len = int(ByteData[index_8000 + 5:index_bytedata])

    data1 = struct.unpack("B" * data_len, ByteData[index_bytedata:])





if __name__ == '__main__':

    #

    #source = "CHANnel2"; format = "CSV"; length = 50000;FREQ=None;filename = '\usb\For_Dean_1';

    source = "CHANnel1";#No always necessary
    format = "BINary";
    length = 500000;#Not always usefull
    FREQ = None;
    FilesNum=400
    #filename = '\\usb\\Debug2'
    filename = '\\usb\\one_bit_dean'

    main_save_to_drive(source,format,length,FREQ,filename,FilesNum=FilesNum)
    #main_segmented(source=source)

