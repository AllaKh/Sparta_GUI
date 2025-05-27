import os,sys  #needed to check the working directory
import numpy as np
import matplotlib.pyplot as plt
import visa
import SampleSigByClock as ssclk

def SetupandSampleFromScope(NumOfChirps,ScopeAdress,TimeScale,TOffset,Chan1Offset,TrigCh1,Ch1Scale,Chan4Offset,TrigCh4,Ch4Scale):
    
    # Directory path to visa32.dll so it can be used by pyVISA
    rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # this uses pyvisa
    ## Open session using rm, which is the resource manager, and the visa address.
    GSInfiniivision = rm.open_resource(ScopeAdress)
    ## Set Global Timeout
    GSInfiniivision.timeout = 10000
    ## Clear the instrument bus
    GSInfiniivision.clear()      
    #Check Communication with the scope and print its name.
    IDN = GSInfiniivision.query("*IDN?")
    print(IDN)
    # initilize the scope
    GSInfiniivision.write(":TIMebase:SCALe "+ TimeScale) # 94 usec scale
    GSInfiniivision.write(":TIMebase:POSition "+TOffset) #933 usec offset
    GSInfiniivision.write(":FFT:DISPlay OFF") # fft off
    GSInfiniivision.write(":ACQuire:TYPE NORMal")
    GSInfiniivision.write(":WAVeform:POINts MAXimum")    
    GSInfiniivision.write(":acquire:points100000")
    GSInfiniivision.write(':acquire:srate500000000')    
    GSInfiniivision.write(':ACQUIRE:MODE RTIME')
    GSInfiniivision.write('*OPC?')
    GSInfiniivision.write(':TRIGger:MODE EDGE')
    GSInfiniivision.write(':TRIGger:EDGE:SOUrce EXTernal')
    GSInfiniivision.write(':TRIGger:SWEep NORMal')
    GSInfiniivision.write(':TRIGger:EDGE:SLOPe POS')

    #Ch1
    GSInfiniivision.write(":CHANnel1:IMPedance ONEMeg")##  
    GSInfiniivision.write("[':TRIGGER:LEVEL 1,"+TrigCh1)
    GSInfiniivision.write(":CHANnel1:OFFSet "+Chan1Offset)
    GSInfiniivision.write(':CHANnel1:SCALe '+Ch1Scale)
    GSInfiniivision.write(':ACQUIRE:MODE RTIME')


    # CH4
    GSInfiniivision.write(":CHANnel4:IMPedance FIFT")
    GSInfiniivision.write("[':TRIGGER:LEVEL 4,"+TrigCh4)
    GSInfiniivision.write(":CHANnel4:OFFSet "+Chan4Offset)
    GSInfiniivision.write(':CHANnel4:SCALe '+Ch4Scale)
    # Grab the Data
    Reset_Perfomed=0
    Real_ind=0
    Cur_Chirp=0
    ScopeData1=[]
    ScopeData4=[]
    while Cur_Chirp<NumOfChirps:
        if Reset_Perfomed:
            Cur_Chirp=1
            Reset_Perfomed=0
        
        GSInfiniivision.write("*OPC?")
        GSInfiniivision.write("*cls")
        GSInfiniivision.write(":single")
        GSInfiniivision.write('WAV:SOURCE CHAN1')
        GSInfiniivision.write('WAVeform:FORMAT BYTE')
        GSInfiniivision.write('WAVEFORM:BYTEORDER LSBFirst')
        GSInfiniivision.write(':WAVEFORM:PREAMBLE?')
        GSInfiniivision.write('*OPC?')
        GSInfiniivision.write(':WAVeform:POINts 6250000')
        GSInfiniivision.write(':WAVeform:POINts:MODE RAW')
        
        TempData1=np.array(GSInfiniivision.query_values(":WAV:DATA?"))
        yinc = GSInfiniivision.query(':WAVeform:YINCrement?')
        YIncrement=float(yinc[1:-1])
        
        #TempData1=np.multiply(TempData,YIncrement)
        plt.plot(TempData1)
        plt.show()
        if np.shape(TempData1)==[]:
            np.disp('Grabbing Failed')
            Cur_Chirp=Cur_Chirp-1

        GSInfiniivision.write('WAV:SOURCE CHAN4')
        GSInfiniivision.write('WAV:FORMAT WORD')
        GSInfiniivision.write('WAVEFORM:BYTEORDER MSBFirst')
        GSInfiniivision.write(':WAVEFORM:PREAMBLE?')
        GSInfiniivision.write('*OPC?')
        GSInfiniivision.write(':WAVeform:POINts 6250000')
        TempData4=np.array(GSInfiniivision.query_values(":WAV:DATA?"))
        plt.plot(TempData4)
        plt.show()
        #yinc = GSInfiniivision.query(':WAVeform:YINCrement?')
        #YIncrement=float(yinc[1:-1])
        #TempData4=np.multiply(TempData,YIncrement)
        if np.shape(TempData4)==[]:
            np.disp('Grabbing Failed')
            Cur_Chirp=Cur_Chirp-1
        if Cur_Chirp==0:
            ScopeData1=TempData1[:,np.newaxis]
            ScopeData4=TempData4[:,np.newaxis]
        else:
            ScopeData1=np.append(ScopeData1,TempData1[:,np.newaxis],axis=1)
            ScopeData4=np.append(ScopeData4,TempData4[:,np.newaxis],axis=1)
            x_increment = GSInfiniivision.query(':WAVeform:XINCrement?')
            xSampleTime=float(x_increment[1:-1])
        Cur_Chirp=Cur_Chirp+1
    TimeScope=[t*xSampleTime for t in range(0,np.size(TempData1))]
    return ScopeData1,ScopeData4,TimeScope





if __name__ == "__main__":
    ScopeAdress = "TCPIP0::10.99.0.18::inst0::INSTR"
    TScale="0.000160" #  sec
    TOffset="0.000820" #sec
    Chan1Offset="1.3" #v
    TrigCh1="2.0" #V
    Chan1Scale="0.5" #V
    Chan4Offset="0.1" #v
    TrigCh4="2.0" #V
    Chan4Scale="0.05" #V
    NumOfChirps=5
    data1,data4,TimeScope=SetupandSampleFromScope(NumOfChirps,ScopeAdress,TScale,TOffset,Chan1Offset,TrigCh1,Chan1Scale,Chan4Offset,TrigCh4,Chan4Scale)
    #plt.plot(data1)
    #plt.show()
    #plt.plot(data4)
    #plt.show()
    sim_size=100
    V_dat=np.random.rand(sim_size,1)>0.5
    piezo_dat=0
    clk_dat=np.sin(np.arange(sim_size))>0
    time_inc=TimeScope[100]-TimeScope[99]
    
    time_dat=np.arange(sim_size)*time_inc
    drop2data_offset=2
    good_inds=np.arange(np.shape(data1)[0])
    plot_flag=True
    ssclk.SampleSigByClock_fun(data1,data4,0,TimeScope,drop2data_offset,good_inds,time_inc,plot_flag)
    np.disp('Grab complete')