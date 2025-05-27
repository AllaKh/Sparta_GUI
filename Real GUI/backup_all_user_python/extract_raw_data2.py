#########################################################
##Extract time domain and FFT data from raw binary file##
###############  Elad Amrani ############################
#########################################################
#blabla
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import operator
import math
import sys
import os
from subprocess import call

call(["rm","raw*"])
call(["./loop.sh","9"])

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
#file_name = sys.argv[1]

sum_p1=0
sum_p2=0
sum_p3=0
sum_p0=0
file_counter=0
for filename in os.listdir("/spartaLinux"):
	if filename.endswith(".dat") and filename.startswith("raw"):
	        #print(filename)
		file_counter=file_counter+1;
		pass
    	else:
		continue
	print(filename)
	raw_data = open(filename,"rb")
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
		
			
	   
		# Print result
		print("Pixel: #",pixel)
		print("FFT #1")
		#print("Estimated frequency: ",estimated_frequency, "KHz")
		#print("Actual frequency:    ", maxFreq,"KHz")
		#print("PC frequency:        ", PCmaxFreq,"KHz")
		print("Sum of TD elements:  ", sum_td1[pixel])
		print("")
		
		print("Pixel: #",pixel)
		print("FFT #2")
		#print("Estimated frequency: ",estimated_frequency, "KHz")
		#print("Actual frequency:    ", maxFreq,"KHz")
		#print("PC frequency:        ", PCmaxFreq,"KHz")
		print("Sum of TD elements:  ", sum_td2[pixel])
		print("Average Sum for Pixel ",pixel,":  ", 0.5*(sum_td1[pixel]+sum_td2[pixel]))
		print("")
		if pixel==0:
			sum_p0=sum_p0+0.5*(sum_td1[pixel]+sum_td2[pixel])
		elif pixel==1:
			sum_p1=sum_p1+0.5*(sum_td1[pixel]+sum_td2[pixel])
		elif pixel==2:
			sum_p2=sum_p2+0.5*(sum_td1[pixel]+sum_td2[pixel])
		elif pixel==3:
			sum_p3=sum_p3+0.5*(sum_td1[pixel]+sum_td2[pixel])

print((sum_p0/file_counter/TD1_LEN-0.5)*2.0)
print((sum_p1/file_counter/TD1_LEN-0.5)*2.0)
print((sum_p2/file_counter/TD1_LEN-0.5)*2.0)
print((sum_p3/file_counter/TD1_LEN-0.5)*2.0)
print(sum_p0/file_counter)
print(sum_p1/file_counter)
print(sum_p2/file_counter)
print(sum_p3/file_counter)
#dir_path=os.path.dirname(os.path.realpath(___file___))
for filename in os.listdir("/spartaLinux"):
    if filename.endswith(".dat") and filename.startswith("raw"):
        print(filename)
	continue
    else:
	continue
	
#print(sum_td1, sum_td2)
