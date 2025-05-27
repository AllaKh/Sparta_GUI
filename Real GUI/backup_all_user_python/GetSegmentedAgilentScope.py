import os,sys
import struct
import re
import visa
import time

rm = visa.ResourceManager()

ControllerID='0'
TCPIPAddress='10.99.10.222'

global Instrument

Instrument=rm.open_resource('TCPIP'+ControllerID+'::'+TCPIPAddress+"::inst"+ControllerID+"::INSTR")

print(Instrument)

def main_save_to_drive(source = "CHANnel1", format = "BYTE"):

    Instrument.write(":WAVeform:FORMat %s" % format)

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

    source = "CHANnel2"

    main_segmented(source=source)

