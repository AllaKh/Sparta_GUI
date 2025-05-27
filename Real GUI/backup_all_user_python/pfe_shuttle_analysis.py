import numpy as np
import pandas as pd
from scipy import signal,fftpack
from copy import deepcopy
import matplotlib.pyplot as plt



def ExtractDataFromScopeDSO(df):

    #df.drop(df.index[0], inplace=True)

    df.dropna(inplace=True)

    NumDf = df.apply(pd.to_numeric, errors='ignore')

    LaserPos = np.abs(NumDf["trigger"].values)

    LaserPosRollMean = pd.rolling_mean(LaserPos, 10)

    LaserPosRollMean[np.isnan(LaserPosRollMean)] = 0

    MaxIdxFirst = np.where(LaserPos > np.max(LaserPosRollMean)/2.0)[0][10]

    MaxIdxSecond = MaxIdxFirst + np.where(LaserPosRollMean[MaxIdxFirst:] < np.max(LaserPos) * 2 / 3.0)[0][0]

    CompOut = NumDf["data"].values[MaxIdxFirst:MaxIdxSecond]

    return(CompOut)

def ExtractDataFromScopeDSOFile(df):

    df.drop(df.index[0], inplace=True)

    df.dropna(inplace=True)

    NumDf = df.apply(pd.to_numeric, errors='ignore')

    LaserPos = np.abs(NumDf["1"].values)

    LaserPosRollMean = pd.rolling_mean(LaserPos, 10)

    MaxIdxFirst = np.where(LaserPosRollMean > np.max(LaserPosRollMean) / 2.0)[0][10]

    MaxIdxSecond = MaxIdxFirst + np.where(LaserPosRollMean[MaxIdxFirst:] < np.max(LaserPos) * 2 / 3.0)[0][0]

    CompOut = NumDf["1"].values[MaxIdxFirst:MaxIdxSecond]

    return(CompOut)

def ExtractDataFromScope(data,clock,sample_edge="pos"):

    CLK = np.array(clock) #clock.values
    Data = np.array(data) #data.values

    myclk = np.ones(len(CLK))
    Threshold_clk = np.mean(CLK)

    myclk[np.where(CLK < Threshold_clk)] = 0

    diff_clk = np.diff(myclk)

    if sample_edge == "neg":
        # @Neg
        diff_clk[np.where(diff_clk > 0)[0]] = 0
        diff_clk = np.insert(diff_clk, 0, 0)
        diff_clk = abs(diff_clk)

    elif sample_edge == "pos":
        # @Pos
        diff_clk[np.where(diff_clk < 0)[0]] = 0
        diff_clk = np.insert(diff_clk, 0, 0)

    CompOut = Data[np.where(diff_clk > 0)]

    Threshold_data = np.mean(Data)

    CompOut[np.where(CompOut <= Threshold_data)[0]] = 0
    CompOut[np.where(CompOut > Threshold_data)[0]] = 1.

    return(CompOut)

def SNRCalc(vin,fin=None,Fs=48e6,window="hann",nfft=None,N=1,fdc=500,LowFreq=5e3,HighFreq=20e6,cleanDC=False,plotData=False,showPlot=False):

    if window=="hann":
        ps_bins=3
        dc_bins=6
    elif window=="boxcar":
        ps_bins=0
        dc_bins = 1
    elif window=="blackman":
        ps_bins=1
        dc_bins = 3

    Ts=1./Fs
    M = len(vin)
    #x = np.linspace(0, M * Ts, M)

    if nfft is None:
        FreqBin = Fs / M
        xf=np.arange(0, Fs, Fs / M)
    else:
        FreqBin = Fs / nfft
        xf = np.arange(0, Fs, Fs / nfft)
    if cleanDC:
        vin=vin-np.mean(vin)

    if nfft is None:
        w = signal.get_window(window, M)
        enbw = M * np.sum(w ** 2) / (np.sum(w) ** 2)
        f, sxx = signal.periodogram(vin,Fs,w,nfft=None,scaling='spectrum')
        # yf = fftpack.fft(vin)
    else:
        w = signal.get_window(window, nfft)
        enbw = nfft * np.sum(w ** 2) / (np.sum(w) ** 2)
        f, sxx = signal.periodogram(vin, Fs, w, nfft=None, scaling='spectrum')
        # yf = fftpack.fft(vin,n=nfft)
    NoiseFloor_theoretical_dBFS =-1*( 6.02 * N + 1.76 + 10 * np.log10(M / (2 * enbw)))
    print("Theoretical Noise Floor  in dBFS is :",NoiseFloor_theoretical_dBFS)
    _sxx = deepcopy(sxx)

    #Find the peak exluding dc and lower freqs
    LowFreqIndex  =  np.where(f > LowFreq)[0][0];
    #print("Low_Index:",LowFreqIndex)
    HighFreqIndex =  np.where(f > HighFreq)[0][0];
    #print("High_Index:", HighFreqIndex)

    if fin is None:
        fundIdx = LowFreqIndex+np.argmax(_sxx[LowFreqIndex:HighFreqIndex])
    else:
        pass


    #print("The fundamental index is: ",fundIdx)
    freq_max = f[fundIdx]
    print("The estimated fundamental frequency is:", f[fundIdx])
    fundFreq = f[fundIdx]
    if plotData:
        fig = plt.figure(figsize=[18, 8])
        ##### Plot the fft #####
        ax = plt.subplot(121)
        pt, = ax.plot(f, 10*np.log10(sxx), lw=2.0, c='b')
        p = plt.Rectangle((Fs / 2, 0), Fs / 2, ax.get_ylim()[1], facecolor="grey", fill=True, alpha=0.75, hatch="/",zorder=3)
        ax.add_patch(p)
        #ax.set_xlim((ax.get_xlim()[0], Fs))
        ax.set_title('FFT', fontsize=16, fontweight="bold")
        ax.set_ylabel('FFT magnitude (power)')
        ax.set_xlabel('Frequency (Hz)')
        plt.legend((p,),('mirrowed',))
        ax.grid()
        ##### Close up on the graph of fft#######
        # This is the same histogram above, but truncated at the max frequence + an offset.
        ax2 = fig.add_subplot(122)
        ax2.plot(f[fundIdx-30:fundIdx+30],10*np.log10(sxx[fundIdx-30:fundIdx+30]), lw=2.0, c='b')
        ax2.set_xticks(f)
        #ax2.set_xlim(freq_max-FreqBin*30,freq_max+FreqBin*30)
        ax2.set_title('FFT close-up', fontsize=16, fontweight="bold")
        ax2.set_ylabel('FFT magnitude (power) - log')
        ax2.set_xlabel('Frequency (Hz)')
        #ax2.hold(True)
        ax2.grid()
        plt.yscale('log')
    #DC power
    dcIndex = np.where(f >fdc)[0][0];
    Pdc=np.sum(_sxx[0:dcIndex]);
    #Signal Power
    ps_bins_right=ps_bins;
    while (fundIdx+ps_bins>len(sxx)) and (ps_bins_right>=1):
        ps_bins_right-=1;
    if ((fundIdx+ps_bins)>len(sxx)):
        Ps=np.sum(sxx[fundIdx-ps_bins:fundIdx]);
    else:
        Ps=np.sum(sxx[(fundIdx-ps_bins):(fundIdx+ps_bins_right)]);
    #Zeroing the signal power
    sxx[(fundIdx-ps_bins):(fundIdx+ps_bins_right+1)]=0;
    # Zeroing DC
    sxx[0:dcIndex + 1] = 0  # min(sxx)
    #Noise and Distortion at Narrow
    Pnd = np.sum(sxx[fundIdx-20:fundIdx+20])
    SNR = 10*np.log10(Ps/Pnd)

    return(_sxx,f,SNR,Pnd,Ps,Pdc)

def main():


    pass

if __name__ == "__main__":

    path = r'C:\Users\User\Documents\Python Scripts'

    main()
