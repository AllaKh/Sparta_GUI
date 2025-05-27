import numpy as np
import matplotlib.pyplot as plt
import SetupandSampleFromScope as SetupandSampleFromScope
def FftFromTimeDomain(SensorTdata,fs):
    

    fft_dat=np.fft.fft(np.asarray(SensorTdata),axis=0)
    [fftLength,NumOfChirpsM]=np.shape(fft_dat) # Numof Chirps -1
    halflength=int(np.round(fftLength/2))
    fftabs=np.abs(np.asarray(fft_dat[0:halflength,:]))
    fftmean=np.mean(np.asarray(fftabs),axis=1)
    fftstd=np.std(np.asarray(fft_dat[0:halflength,:]),axis=1)
    
    fftsorted=np.sort(fftabs,axis=1)
    if NumOfChirpsM >2:
        fftmax=np.std(fftsorted[:,NumOfChirpsM-3:NumOfChirpsM],axis=1)
    else :
        fftmax=fftsorted[:,NumOfChirpsM]
    freq=(fs/2)/np.arange(halflength)
    binf=fs/2/halflength
    freq=binf*np.arange(halflength)

    return fft_dat,fftabs,fftmean,fftstd,fftmax,freq

if __name__ == "__main__":
   (SampledData,time_dat,fs)= SetupandSampleFromScope.main_grab(5)
   (fft_dat,fftabs,fftmean,fftstd,fftmax,freq)=FftFromTimeDomain(SampledData,500e6)
   #plt.plot(freq,fftmean)
   #plt.plot(freq,fftabs[:,1])
   #plt.show()
   plt.plot(freq,fftstd)
   #plt.plot(freq,fftmax)
   plt.show()



