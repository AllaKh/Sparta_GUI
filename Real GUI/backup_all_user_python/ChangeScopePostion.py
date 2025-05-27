import os,sys  #needed to check the working directory
import numpy as np
import visa

#Replace the VISA address shown here with the VISA address of your InfiniiVision.
#You'll find the VISA address within the IO Libraries installed on your PC.
VISA_ADDRESS = "TCPIP0::10.99.0.18::inst0::INSTR"
 
#Directory path to visa32.dll so it can be used by pyVISA
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # this uses pyvisa
## Open session using rm, which is the resource manager, and the visa address.
GSInfiniivision = rm.open_resource(VISA_ADDRESS)
## Set Global Timeout
GSInfiniivision.timeout = 10000
## Clear the instrument bus
GSInfiniivision.clear()
    
#Check Communication with the scope and print its name.
IDN = GSInfiniivision.query("*IDN?")
print(IDN)
# initilize the scope
GSInfiniivision.write(":TIMebase:SCALe 0.000094") # 94 usec scale
GSInfiniivision.write(":TIMebase:POSition 0.000933") #933 usec offset
GSInfiniivision.write(":FFT:DISPlay OFF") # fft off
GSInfiniivision.write(":ACQuire:TYPE NORMal")
GSInfiniivision.write(":WAVeform:POINts MAXimum")
GSInfiniivision.write(":CHANnel1:IMPedance FIFT")
GSInfiniivision.write(":CHANnel1:OFFSet 1.7")
GSInfiniivision.write(":acquire:points100000")
GSInfiniivision.write(':acquire:srate500000000')
GSInfiniivision.write("[':TRIGGER:LEVEL 1,2.0")
GSInfiniivision.write(':ACQUIRE:MODE RTIME')
GSInfiniivision.write('*OPC?')
GSInfiniivision.write(':TRIGger:MODE EDGE')
GSInfiniivision.write(':CHANnel1:SCALe 0.05')

# CH4
GSInfiniivision.write(":CHANnel1:IMPedance FIFT")
GSInfiniivision.write(":CHANnel1:OFFSet 0.1")
GSInfiniivision.write(':CHANnel4:SCALe 0.05')
# Grab the Data
Reset_Perfomed=0
Real_ind=0
Cur_Chirp=0
NumOfChirps=3
ScopeData1=[]
ScopeData4=[]
while Cur_Chirp<NumOfChirps:
    if Reset_Perfomed:
        Cur_Chirp=1
        Reset_Perfomed=0
    GSInfiniivision.write("*OPC?")
    GSInfiniivision.write("*cls")
    GSInfiniivision.write(":single")
    GSInfiniivision.write('WAV:SOURCE 1')
    GSInfiniivision.write(':WAVeform:POINts 6250000')
    TempData1=np.array(GSInfiniivision.query_values(":WAV:DATA?"))
    if np.shape(TempData1)==[]:
        np.disp('Grabbing Failed')
        Cur_Chirp=Cur_Chirp-1

    GSInfiniivision.write('WAV:SOURCE 4')
    GSInfiniivision.write(':WAVeform:POINts 6250000')
    TempData4=np.array(GSInfiniivision.query_values(":WAV:DATA?"))
    if np.shape(TempData4)==[]:
        np.disp('Grabbing Failed')
        Cur_Chirp=Cur_Chirp-1
    ScopeData1=np.append(TempData1,ScopeData1)
    ScopeData4=np.append(TempData4,ScopeData4)
    Cur_Chirp=Cur_Chirp+1



np.disp('Grab complete')