import os,sys  #needed to check the working directory
import numpy as np
import matplotlib.pyplot as plt
import visa
import SampleSigByClock as ssclk
import time
import scipy.io as sio

def SetupFromScope(ScopeAdress,TimeScale,TOffset,Chan1Offset,TrigCh1,Ch1Scale,Chan4Offset,TrigCh4,Ch4Scale,Chan2Offset=0,TrigCh2=0,Ch2Scale=0):
    Succses=0
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

    #Ch2
    if not Chan2Offset==0:
        GSInfiniivision.write(":CHANnel1:IMPedance ONEMeg")##  
        GSInfiniivision.write("[':TRIGGER:LEVEL 2,"+TrigCh2)
        GSInfiniivision.write(":CHANnel2:OFFSet "+Chan2Offset)
        GSInfiniivision.write(':CHANnel2:SCALe '+Ch2Scale)
        GSInfiniivision.write(':ACQUIRE:MODE RTIME')

    # CH4
    GSInfiniivision.write(":CHANnel4:IMPedance FIFT")
    GSInfiniivision.write("[':TRIGGER:LEVEL 4,"+TrigCh4)
    GSInfiniivision.write(":CHANnel4:OFFSet "+Chan4Offset)
    GSInfiniivision.write(':CHANnel4:SCALe '+Ch4Scale)
    Succses=1
    return GSInfiniivision

def SampleFromScope(NumOfChirps,GSInfiniivision,my_ques=0):
    
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
        GSInfiniivision.write('WAVeform:FORMAT WORD')
        GSInfiniivision.write('WAVEFORM:BYTEORDER LSBFirst')
        GSInfiniivision.write(':WAVEFORM:PREAMBLE?')
        GSInfiniivision.write('*OPC?')
        GSInfiniivision.write(':WAVeform:POINts 6250000')
        GSInfiniivision.write(':WAVeform:POINts:MODE RAW')
        if Cur_Chirp==0:
            time.sleep(2.4)
            Pre1=GSInfiniivision.query_ascii_values(':WAVEFORM:PREAMBLE?') # ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
        ## In above line, the waveform source is already set; no need to reset it.
        Yinc= float(Pre1[7]) # Y INCrement, Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
        YOrgin= float(Pre1[8]) # Y ORIGin, Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
        YRef= float(Pre1[9]) # Y REFerence, Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
      
        TempDataRaw=np.array(GSInfiniivision.query_binary_values(':WAVeform:SOURce CHANnel1;DATA?', "H", False))    
        TempData1=(( TempDataRaw - YRef)*Yinc+YOrgin)
        #yinc = GSInfiniivision.query(':WAVeform:YINCrement?')
        #YIncrement=float(yinc[1:-1])
        
        #TempData1=np.multiply(TempData,YIncrement)
        #plt.plot(TempData1)
        #plt.show()
        if np.shape(TempData1)==[]:
            np.disp('Grabbing Failed')
            Cur_Chirp=Cur_Chirp-1
        # CH4
        GSInfiniivision.write('WAV:SOURCE CHAN4')
        GSInfiniivision.write('WAVeform:FORMAT WORD')
        GSInfiniivision.write('WAVEFORM:BYTEORDER LSBFirst')
        GSInfiniivision.write(':WAVEFORM:PREAMBLE?')
        GSInfiniivision.write('*OPC?')
        GSInfiniivision.write(':WAVeform:POINts 6250000')
        GSInfiniivision.write(':WAVeform:POINts:MODE RAW')
        if Cur_Chirp==0:
            time.sleep(1)
            Pre4=GSInfiniivision.query_ascii_values(':WAVEFORM:PREAMBLE?') # ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
        ## In above line, the waveform source is already set; no need to reset it.
        Yinc= float(Pre4[7]) # Y INCrement, Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
        YOrgin= float(Pre4[8]) # Y ORIGin, Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
        YRef= float(Pre4[9]) # Y REFerence, Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
      
        TempDataRaw=np.array(GSInfiniivision.query_binary_values(':WAVeform:SOURce CHANnel4;DATA?', "H", False))    
        TempData4=(( TempDataRaw - YRef)*Yinc+YOrgin)
       
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
        print(" grabbed %d chirp" %Cur_Chirp)
    # TimeScope=np.asarray([t*xSampleTime for t in range(0,np.size(TempData1))])
    TimeScope=np.arange(np.size(TempData1))*xSampleTime#
    GSInfiniivision.write(":RUN")

    return ScopeData1,ScopeData4,TimeScope

def SampleFromScope_three_chan(NumOfChirps,GSInfiniivision,my_ques=0):
    
    # Grab the Data
    Reset_Perfomed=0
    Real_ind=0
    Cur_Chirp=0
    ScopeData1=[]
    ScopeData2=[]
    ScopeData4=[]
    while Cur_Chirp<NumOfChirps:
        if Reset_Perfomed:
            Cur_Chirp=1
            Reset_Perfomed=0
        
        GSInfiniivision.write("*OPC?")
        GSInfiniivision.write("*cls")
        GSInfiniivision.write(":single")
        GSInfiniivision.write('WAV:SOURCE CHAN1')
        GSInfiniivision.write('WAVeform:FORMAT WORD')
        GSInfiniivision.write('WAVEFORM:BYTEORDER LSBFirst')
        GSInfiniivision.write(':WAVEFORM:PREAMBLE?')
        GSInfiniivision.write('*OPC?')
        GSInfiniivision.write(':WAVeform:POINts 6250000')
        GSInfiniivision.write(':WAVeform:POINts:MODE RAW')
        if Cur_Chirp==0:
            time.sleep(2.4)
            Pre1=GSInfiniivision.query_ascii_values(':WAVEFORM:PREAMBLE?') # ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
        ## In above line, the waveform source is already set; no need to reset it.
        Yinc= float(Pre1[7]) # Y INCrement, Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
        YOrgin= float(Pre1[8]) # Y ORIGin, Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
        YRef= float(Pre1[9]) # Y REFerence, Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
      
        TempDataRaw=np.array(GSInfiniivision.query_binary_values(':WAVeform:SOURce CHANnel1;DATA?', "H", False))    
        TempData1=(( TempDataRaw - YRef)*Yinc+YOrgin)
        #yinc = GSInfiniivision.query(':WAVeform:YINCrement?')
        #YIncrement=float(yinc[1:-1])
        
        #TempData1=np.multiply(TempData,YIncrement)
        #plt.plot(TempData1)
        #plt.show()
        if np.shape(TempData1)==[]:
            np.disp('Grabbing Failed')
            Cur_Chirp=Cur_Chirp-1
            continue

        # CH2
        GSInfiniivision.write('WAV:SOURCE CHAN2')
        GSInfiniivision.write('WAVeform:FORMAT WORD')
        GSInfiniivision.write('WAVEFORM:BYTEORDER LSBFirst')
        GSInfiniivision.write(':WAVEFORM:PREAMBLE?')
        GSInfiniivision.write('*OPC?')
        GSInfiniivision.write(':WAVeform:POINts 6250000')
        GSInfiniivision.write(':WAVeform:POINts:MODE RAW')
        if Cur_Chirp==0:
            time.sleep(1)
            Pre2=GSInfiniivision.query_ascii_values(':WAVEFORM:PREAMBLE?') # ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
        ## In above line, the waveform source is already set; no need to reset it.
        Yinc= float(Pre2[7]) # Y INCrement, Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
        YOrgin= float(Pre2[8]) # Y ORIGin, Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
        YRef= float(Pre2[9]) # Y REFerence, Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
      
        TempDataRaw=np.array(GSInfiniivision.query_binary_values(':WAVeform:SOURce CHANnel2;DATA?', "H", False))    
        TempData2=(( TempDataRaw - YRef)*Yinc+YOrgin)
       
        #yinc = GSInfiniivision.query(':WAVeform:YINCrement?')
        #YIncrement=float(yinc[1:-1])
        #TempData4=np.multiply(TempData,YIncrement)
        if np.shape(TempData2)==[]:
            np.disp('Grabbing Failed')
            Cur_Chirp=Cur_Chirp-1
            continue
        # CH4
        GSInfiniivision.write('WAV:SOURCE CHAN4')
        GSInfiniivision.write('WAVeform:FORMAT WORD')
        GSInfiniivision.write('WAVEFORM:BYTEORDER LSBFirst')
        GSInfiniivision.write(':WAVEFORM:PREAMBLE?')
        GSInfiniivision.write('*OPC?')
        GSInfiniivision.write(':WAVeform:POINts 6250000')
        GSInfiniivision.write(':WAVeform:POINts:MODE RAW')
        if Cur_Chirp==0:
            time.sleep(1)
            Pre4=GSInfiniivision.query_ascii_values(':WAVEFORM:PREAMBLE?') # ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
        ## In above line, the waveform source is already set; no need to reset it.
        Yinc= float(Pre4[7]) # Y INCrement, Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
        YOrgin= float(Pre4[8]) # Y ORIGin, Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
        YRef= float(Pre4[9]) # Y REFerence, Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
      
        TempDataRaw=np.array(GSInfiniivision.query_binary_values(':WAVeform:SOURce CHANnel4;DATA?', "H", False))    
        TempData4=(( TempDataRaw - YRef)*Yinc+YOrgin)
       
        #yinc = GSInfiniivision.query(':WAVeform:YINCrement?')
        #YIncrement=float(yinc[1:-1])
        #TempData4=np.multiply(TempData,YIncrement)
        if np.shape(TempData4)==[]:
            np.disp('Grabbing Failed')
            Cur_Chirp=Cur_Chirp-1
            continue

        if Cur_Chirp==0:
            ScopeData1=TempData1[:,np.newaxis]
            ScopeData2=TempData2[:,np.newaxis]
            ScopeData4=TempData4[:,np.newaxis]
        else:
            ScopeData1=np.append(ScopeData1,TempData1[:,np.newaxis],axis=1)
            ScopeData2=np.append(ScopeData2,TempData2[:,np.newaxis],axis=1)
            ScopeData4=np.append(ScopeData4,TempData4[:,np.newaxis],axis=1)
            x_increment = GSInfiniivision.query(':WAVeform:XINCrement?')
            xSampleTime=float(x_increment[1:-1])
        Cur_Chirp=Cur_Chirp+1
        print(" grabbed %d chirp" %Cur_Chirp)
    # TimeScope=np.asarray([t*xSampleTime for t in range(0,np.size(TempData1))])
    TimeScope=np.arange(np.size(TempData1))*xSampleTime#
    GSInfiniivision.write(":RUN")

    return ScopeData1,ScopeData2,ScopeData4,TimeScope

def main_set(scope_dat_obj):

    Success=SetupFromScope(scope_dat_obj.ScopeAdress,scope_dat_obj.TScale,scope_dat_obj.TOffset,scope_dat_obj.Chan1Offset,scope_dat_obj.TrigCh1,scope_dat_obj.Chan1Scale,scope_dat_obj.Chan4Offset,scope_dat_obj.TrigCh4,scope_dat_obj.Chan4Scale)
    np.disp(Success)
    return Success

def main_grab(scope_dat_obj,my_ques=0):
    
    data1,data4,TimeScope=SampleFromScope(scope_dat_obj.num_of_chirps,scope_dat_obj.scope_handle)
    #plt.plot(data1)
    #plt.plot(data4)
    #plt.show()
    # sim_size=100
    #V_dat=np.random.rand(sim_size,1)>0.5
    # piezo_dat=0
    # clk_dat=np.sin(np.arange(sim_size))>0
    time_inc=TimeScope[100]-TimeScope[99]
    
    # time_dat=np.arange(sim_size)*time_inc
    drop2data_offset=2
    good_inds=np.arange(np.shape(data1)[0])
    plot_flag=False
    for k in np.arange(scope_dat_obj.num_of_chirps):
        SampledTemp=ssclk.SampleSigByClock_fun(np.squeeze(data1[:,k]),np.squeeze(data4[:,k]),0,TimeScope,drop2data_offset,good_inds,time_inc,plot_flag)
        print("fs is %d" %SampledTemp[2])
        if k==0:
            fsOrig=SampledTemp[2]
            SampledData=SampledTemp[0][:,np.newaxis] 
            time_dat=SampledTemp[1]
           
        else:
            if len(SampledTemp[1])>len(time_dat): # sometimes the sampled vector size is not equal to the length of the rest of the signals
                new_dat=SampledTemp[0][0:len(time_dat)]
            elif len(SampledTemp[1])<len(time_dat):
                new_dat=SampledTemp[0]
                time_dat=SampledTemp[1]
                SampledData=SampledData[0:len(time_dat),:]
                #cut data, update timedat
            else:
                new_dat=SampledTemp[0] # same size

            SampledData=np.append(SampledData,new_dat[:,np.newaxis],axis=1)

    np.disp('Grab complete')
    time_dat=SampledTemp[1]
    fs=SampledTemp[2]
    return SampledData,time_dat,fs

def main_grab_three_chan(scope_handle,num_of_chirps,my_ques=0):
    
    data1,data2,data4,TimeScope=SampleFromScope_three_chan (num_of_chirps,scope_handle)
    #plt.plot(data1)
    #plt.plot(data4)
    #plt.show()
    # sim_size=100
    #V_dat=np.random.rand(sim_size,1)>0.5
    # piezo_dat=0
    # clk_dat=np.sin(np.arange(sim_size))>0
    time_inc=TimeScope[100]-TimeScope[99]
    
    # time_dat=np.arange(sim_size)*time_inc
    drop2data_offset=2
    good_inds=np.arange(np.shape(data1)[0])
    plot_flag=False
    for k in np.arange(num_of_chirps):
        SampledTemp=ssclk.SampleSigByClock_fun(np.squeeze(data1[:,k]),np.squeeze(data4[:,k]),0,TimeScope,drop2data_offset,good_inds,time_inc,plot_flag)
        print("fs is %d" %SampledTemp[2])
        if k==0:
            fsOrig=SampledTemp[2]
            SampledData=SampledTemp[0][:,np.newaxis] 
            time_dat=SampledTemp[1]
           
        else:
            if len(SampledTemp[1])>len(time_dat): # sometimes the sampled vector size is not equal to the length of the rest of the signals
                new_dat=SampledTemp[0][0:len(time_dat)]
            elif len(SampledTemp[1])<len(time_dat):
                new_dat=SampledTemp[0]
                time_dat=SampledTemp[1]
                SampledData=SampledData[0:len(time_dat),:]
                #cut data, update timedat
            else:
                new_dat=SampledTemp[0] # same size

            SampledData=np.append(SampledData,new_dat[:,np.newaxis],axis=1)

    np.disp('Grab complete')
    time_dat=SampledTemp[1]
    fs=SampledTemp[2]
    return SampledData,data2,time_dat,fs,TimeScope

if __name__ == "__main__":   
    ScopeAdress = "TCPIP0::10.99.0.18::inst0::INSTR"
    TScale="0.000160" #  sec
    TOffset="0.000790" #sec
    Chan1Offset="1.2" #1.3v
    TrigCh1="2.0" #V
    Chan1Scale="1.0" #V
    Chan2Offset="3.0" #v
    TrigCh2="2.0" #V
    Chan2Scale="0.5" #V
    Chan4Offset="0.11" #v
    TrigCh4="2.0" #V
    Chan4Scale="0.05" #V
    scope_handle=SetupFromScope(ScopeAdress,TScale,TOffset,Chan1Offset,TrigCh1,Chan1Scale,Chan4Offset,TrigCh4,Chan4Scale,Chan2Offset=Chan2Offset,TrigCh2=TrigCh2,Ch2Scale=Chan2Scale)
    np.disp(scope_handle)
    num_of_chirps=5
    SampledData,data2,time_dat,fs,TimeScope=main_grab_three_chan(scope_handle,num_of_chirps)
    fname_str=time.strftime("C:/to_mat_dat/to_mat_dat_%d_%b_%Y_%H_%M_%S", time.gmtime(time.time())) #time.asctime(time.gmtime(time.time()))
    print(type(SampledData),' ',type(SampledData[1][1]),' ',fs)
    # SampledData.tofile(fname_str+'_fs=%d.txt' % (fs),sep=',' ,format ='%d' ) 
    sio.savemat(fname_str+'_fs=%d.mat' % (fs), {'SampledData':SampledData,'data2':data2,'time_dat':time_dat,'TimeScope':TimeScope,'fs':fs})
