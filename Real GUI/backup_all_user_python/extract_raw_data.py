#########################################################
##Extract time domain and FFT data from raw binary file##
###############  Elad Amrani ############################
#########################################################

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import operator
import math
import sys

plt.close("all")

#%%
def bitReverse(x,intSize):
    y = 0
    position = intSize - 1
    while position > 0:
        y += ( ( x & 1 ) << position )
        x >>= 1
        position -= 1
    y += x
    return y

#%%
def bitReversalPermutation(inputArray,intSize):
    N = len(inputArray)
    outputArray = [0] * N
    
    for i in range(0,N):
        outputArray[i] = inputArray[bitReverse(i,intSize-2)]
        
    return outputArray 

#%%
def rearrangeData(inputArray):
    N = len(inputArray)
    outputArray = [0] * N
    iterations = int(N/8)
    
    for i in range(0,iterations):
        for j in range(0,8):
            outputArray[i*8+j] = inputArray[i*8+7-j]

    return outputArray 
            
#%%
Fs = 48e6
TD_BD_SIZE = 655360                    # [Bytes]
NUM_FFT = (int)(sys.argv[2])
TD1_LEN = (int)(sys.argv[3])
TD2_LEN = (int)(sys.argv[4] if (len(sys.argv) == 4 and NUM_FFT == 2) else 32768)
df1 = Fs/TD1_LEN
df2 = Fs/TD2_LEN

TD1_LEN = (TD1_LEN >> 3) << 3
TD2_LEN = (TD1_LEN >> 3) << 3
TD_LEN = []
TD_LEN.append(TD1_LEN)     # Force value to be a multiple of 8. HW Constraint
TD_LEN.append(TD2_LEN)     # Force value to be a multiple of 8. HW Constraint
TOT_TD_LEN = (TD_LEN[0] + TD_LEN[1]) if (NUM_FFT == 2) else TD_LEN[0]
FFT1_IN_LEN = (int)(math.pow(2,math.ceil(math.log(TD1_LEN)/math.log(2))))
FFT2_IN_LEN = (int)(math.pow(2,math.ceil(math.log(TD1_LEN)/math.log(2))))
N = FFT2_IN_LEN if ((NUM_FFT == 2) and (FFT2_IN_LEN > FFT1_IN_LEN)) else FFT1_IN_LEN
LOG_N = (int)(math.log(N)/math.log(2))
total_td_buffer_size = math.ceil((TOT_TD_LEN * 320 / 8) / TD_BD_SIZE) * TD_BD_SIZE         # [Bytes]
one_fft_buffer_size = N / 4 * 2                                                            # [Bytes]

dt = 1/Fs
t = np.linspace(dt,N*dt,num=N)
df = Fs / N
k = np.linspace(df,Fs,num=N)
file_name = sys.argv[1]
raw_data = open(file_name,"rb")

for pixel in  range(0,4):    
    td1 = []
    td2 = []
    fd1 = []
    fd2 = []
    sum_td1 = np.zeros(300)
    sum_td2 = np.zeros(300)
    estimated_frequency = 24000/(pixel+2);             # [KHz]
    adc_fifo_offset = pixel % 20
    fft_fifo_offset = pixel // 20
    total_fft_buffer_size = NUM_FFT*one_fft_buffer_size * 300  # [Bytes]
    
    # Time domain
    for i in range(1,int(math.ceil((TOT_TD_LEN/128)+1))):
        raw_data.seek(int(256*adc_fifo_offset+(i-1)*256*20),0)
        for smpl in range(0,128):
            if (((i-1)*128+smpl) == TOT_TD_LEN) : # Break for loop early if we reached end of time domain data
                break
            data = ord(raw_data.read(1))
            data = data + (ord(raw_data.read(1))<<8)
            data = data & (1<<fft_fifo_offset)
            if ((((i-1)*128+smpl) >= TD1_LEN) and NUM_FFT == 2) :
                td2.append(data)
                sum_td2[pixel] += data
            else:
                td1.append(data)
                sum_td1[pixel] += data
             
    #td1 = rearrangeData(td1)
    #td2 = rearrangeData(td2)
    
    # Zero pad time domain if needed. (during operation this is done by HW)
    for i in range(TD1_LEN,N):
        td1.append(0)
    for i in range(TD2_LEN,N):
        td2.append(0)
    
        
    # Frequency domain 1
    for i in range(1,int((N/4/128)+1)):
        raw_data.seek(int(total_td_buffer_size+
                          NUM_FFT*one_fft_buffer_size*15*adc_fifo_offset+
                          fft_fifo_offset*256+
                          (i-1)*256*15),0)
        for smpl in range(0,128):
            data = ord(raw_data.read(1))
            data = data + (ord(raw_data.read(1))<<8)
            fd1.append(data)
            
    # Frequency domain 2
    for i in range(1,int((N/4/128)+1)):
        raw_data.seek(int(total_td_buffer_size+
                          NUM_FFT*one_fft_buffer_size*15*adc_fifo_offset+
                          fft_fifo_offset*256+
                          (i-1)*256*15+
                          one_fft_buffer_size*15),0)
        for smpl in range(0,128):
            data = ord(raw_data.read(1))
            data = data + (ord(raw_data.read(1))<<8)
            fd2.append(data)
    
    #fd1 = rearrangeData(fd1)
    fd1 = bitReversalPermutation(fd1,LOG_N)
    #fd2 = rearrangeData(fd2)
    fd2 = bitReversalPermutation(fd2,LOG_N)
    
    #Calculate PC FFT
    pc_fft1 = abs(fft(td1))
    pc_fft1[0] = 0 # Remove DC
    pc_fft2 = abs(fft(td2))
    pc_fft2[0] = 0 # Remove DC
    
    # Print result
    maxFreqIdx, maxFreqValue = max(enumerate(fd1), key=operator.itemgetter(1))
    maxFreq = (N/4 - maxFreqIdx) * df / 1000
    PCmaxFreqIdx, PCmaxFreqValue = max(enumerate(pc_fft1), key=operator.itemgetter(1))
    PCmaxFreq = PCmaxFreqIdx * df / 1000
    print("Pixel: #",pixel)
    print("FFT #1")
    #print("Estimated frequency: ",estimated_frequency, "KHz")
    #print("Actual frequency:    ", maxFreq,"KHz")
    #print("PC frequency:        ", PCmaxFreq,"KHz")
    print("Sum of TD elements:  ", sum_td1[pixel])
    print("")
    
    maxFreqIdx, maxFreqValue = max(enumerate(fd2), key=operator.itemgetter(1))
    maxFreq = (N/4 - maxFreqIdx) * df / 1000
    PCmaxFreqIdx, PCmaxFreqValue = max(enumerate(pc_fft2), key=operator.itemgetter(1))
    PCmaxFreq = PCmaxFreqIdx * df / 1000
    print("Pixel: #",pixel)
    print("FFT #2")
    #print("Estimated frequency: ",estimated_frequency, "KHz")
    #print("Actual frequency:    ", maxFreq,"KHz")
    #print("PC frequency:        ", PCmaxFreq,"KHz")
    print("Sum of TD elements:  ", sum_td2[pixel])
    print("Average Sum for Pixel ",pixel,":  ", 0.5*(sum_td1[pixel]+sum_td2[pixel]))
    print("")

#    # Plot FPGA FFT 1
#    plt.figure(pixel)
#    plt.plot(k[0:int(N/4)], fd1[::-1])
#    plt.xlabel('freq[Hz]')
#    plt.ylabel('Value')
#    plt.title("FPGA FFT 1")
#    plt.grid()
#    plt.show()
                
 # Plot time domain1
#plt.figure()
#plt.plot(t[0:len(td1)], td1,"o")
#plt.xlabel('time[s]')
#plt.ylabel('Value')
#plt.title("Time Domain 1")
#plt.show()

# # Plot time domain1
# plt.figure()
# plt.plot(t[0:len(td2)], td2,"o")
# plt.xlabel('time[s]')
# plt.ylabel('Value')
# plt.title("Time Domain 2")
# plt.show()


# # Plot time domain1 zoom-in
# plt.figure()
# plt.plot(t[0:63], td1[0:63],"o")
# plt.xlabel('time[s]')
# plt.ylabel('Value')
# plt.title("Time Domain 1 Zoom-in")
# plt.show()


# # Plot PC FFT 1
# plt.figure(1)
# plt.subplot(131)
# plt.semilogx(k[0:int(N/4)+1], np.log10(pc_fft1[0:int(N/4)+1]))
# plt.xlabel('freq[Hz]')
# plt.ylabel('Value')
# plt.title("PC FFT 1")
# plt.grid()
# #plt.show()

# # Plot FPGA FFT 1
# plt.figure(1)
# plt.subplot(132)
# plt.plot(k[0:int(N/4)], fd1[::-1])
# plt.xlabel('freq[Hz]')
# plt.ylabel('Value')
# plt.title("FPGA FFT 1")
# plt.grid()
# # plt.show()

# # Plot FPGA FFT 1
# plt.figure(1)
# plt.subplot(133)
# plt.semilogx(k[0:int(N/4)], np.log10(fd2[::-1]))
# plt.xlabel('freq[Hz]')
# plt.ylabel('Value')
# plt.title("FPGA FFT 2")
# plt.grid()
# plt.show()

# # Plot PC FFT 1
# plt.figure(2)
# plt.subplot(131)
# plt.plot(k[0:int(N/4/12)+1], (pc_fft1[0:int(N/4/12)+1]))
# plt.xlabel('freq[Hz]')
# plt.ylabel('Value')
# plt.title("PC FFT 1")
# plt.grid()
# #plt.show()
# pc_fft_just_1M = pc_fft1[0:int(N/4/12)+1]
# snr_pc_fft = 20*np.log10((np.max((pc_fft_just_1M))/(np.sqrt(np.mean(np.square((pc_fft_just_1M)))))))
# print("PF FFT: ",snr_pc_fft)

# # Plot FPGA FFT 1
# plt.figure(2)
# plt.subplot(132)
# plt.plot(k[0:int(N/4)], (fd1[::-1]))
# plt.xlabel('freq[Hz]')
# plt.ylabel('Value')
# plt.title("FPGA FFT 1")
# plt.grid()
# # plt.show()

# # Plot FPGA FFT 1
# plt.figure(2)
# plt.subplot(133)
# plt.plot(k[0:int(N/4)], (fd2[::-1]))
# plt.xlabel('freq[Hz]')
# plt.ylabel('Value')
# plt.title("FPGA FFT 2")
# plt.grid()
# plt.show()

# if (NUM_FFT == 2):
#     # Plot time domain1
#     plt.figure()
#     plt.plot(t[0:len(td2)], td1,"o")
#     plt.xlabel('time[s]')
#     plt.ylabel('Value')
#     plt.title("Time Domain 2")
#     plt.show()
    
    
#     # Plot time domain2 zoom-in
#     plt.figure()
#     plt.plot(t[0:63], td2[0:63],"o")
#     plt.xlabel('time[s]')
#     plt.ylabel('Value')
#     plt.title("Time Domain 2 Zoom-in")
#     plt.show()
    
    
#     # Plot PC FFT 2 
#     plt.figure()
#     plt.semilogx(k[0:int(N/4)+1], pc_fft2[0:int(N/4)+1])
#     plt.xlabel('freq[Hz]')
#     plt.ylabel('Value')
#     plt.title("PC FFT 2")
#     plt.grid()
#     plt.show()
         
    
#     # Plot FPGA FFT 2
#     plt.figure()
#     plt.semilogx(k[0:int(N/4)], fd2[::-1])
#     plt.xlabel('freq[Hz]')
#     plt.ylabel('Value')
#     plt.title("FPGA FFT 2")
#     plt.grid()
#     plt.show()






