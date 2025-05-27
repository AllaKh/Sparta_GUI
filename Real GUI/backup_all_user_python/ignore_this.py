def SampleFromScope(NumOfChirps,GSInfiniivision):
    
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
            time.sleep(1.5)
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
    return ScopeData1,ScopeData4,TimeScope