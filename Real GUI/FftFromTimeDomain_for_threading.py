import numpy as np
import matplotlib.pyplot as plt
import SetupFromScope as scope
import time 

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
    # freq=(fs/2)/np.arange(halflength)
    binf=fs/2/halflength
    freq=binf*np.arange(halflength)

    return fft_dat,fftabs,fftmean,fftstd,fftmax,freq

def grab_fft_main(fft_in_dat):
    (SampledData,time_dat,fs)= scope.main_grab(fft_in_dat.scope_dat)
    print('np.type(SampledData)')

    fname_str=time.strftime("C:/onebit_data/onebitdata_%d_%b_%Y_%H_%M_%S", time.gmtime(time.time())) #time.asctime(time.gmtime(time.time()))
    print(type(SampledData),' ',type(SampledData[1][1]),' ',fs)
    SampledData.tofile(fname_str+'_fs=%d.txt' % (fs),sep=',' ,format ='%d' ) 

    # np.savetxt(fname_str+'_fs=%d.txt' % (fs),SampledData, fmt='%x',delimiter=',') 
    print('after save ', np.shape(SampledData),SampledData[1][1])

    (fft_dat,fftabs,fftmean,fftstd,fftmax,freq)=FftFromTimeDomain(SampledData,fs)
    print('after FftFromTimeDomain')
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



