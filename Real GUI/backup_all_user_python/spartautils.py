"""
typedef struct
{
    int header_len;
    int version ;
    int frame;
    int pixels;
    int fft_out_len;
    int fft_in_len;
    int log_fft_in_len;
    int num_fft;
    int td1_len;
    int td2_len;
    int td3_len;
    int td_buf_len;


}PacketHeader;
#define HEADER_VER 0xAA55AA57

"""
from __future__ import print_function

from ctypes import *
from struct import *
import freq_table
import socket
import struct
import array
import sys
import convert
import time
import csv
import numpy as np

current_tm = lambda: int(round(time.time() * 1000))

#import numpy as np

class PacketHeaderC(Structure):
     _fields_ = [
        ('header_len',c_int),
        ('version',c_uint),
        ('frame',c_int),
        ('pixels',c_int),
        ('fft_out_len',c_int),
        ('fft_in_len',c_int),
        ('log_fft_in_len',c_int),
        ('num_fft',c_int),
        ('td1_len',c_int),
        ('td2_len',c_int),
        ('td3_len',c_int),
        ('total_lenght',c_int),
        ('status',c_int),
        ('timestamp',c_int),
        ('period',c_int),
        ('clock',c_int),
        ('segments',c_int),       
         ]

class lsrFlatTelemetry(Structure):
     _fields_ = [
        ('meanPower',c_int),
        ('flatness',c_double),
         ]

class Timer:
  def __init__(self):
    self.start = time.time()

  def restart(self):
    self.start = time.time()

  def get_time(self,string):
    end = time.time()
    end = end - self.start
    print("({}) Time elapsed: {:.3f}[mSec]" .format(string,(end*1000)) )


SEGMENT_ID_TD           = (1<<0)
SEGMENT_ID_FD           = (1<<1)
SEGMENT_ID_LD           = (1<<2)
SEGMENT_ID_FLATTENING   = (1<<3)

SEGMENT_HEADER_LEN = 12
	

def BufferedRead(buf_len,socket):
    offset=0
    
    msg = bytearray(buf_len)
    view = memoryview(msg)
    while buf_len > 0:
        nbytes = socket.recv_into(view,buf_len)
        buf_len = buf_len - nbytes
        view = view[nbytes:] 

    return msg


 
def FindSegment(data,id,maxsegs,header_len):
    for i in range(0,maxsegs):
        (h_id,h_offset,h_len)=unpack('iii',data[i*12:(i+1)*12])
        
        if h_len==0:
            continue

        if id == h_id :
            offset = h_offset -header_len  + SEGMENT_HEADER_LEN*maxsegs
            
            return data[ offset  :offset + h_len]   
    return None    

def ReadPacket(s):
    
    timer = Timer()

    ph = PacketHeaderC()
    #timer.restart()
    #ret = s.recv_into(ph)
    #timer.get_time("s.recv_into(ph)")
    ret= sizeof(PacketHeaderC)
    data = BufferedRead(ret,s)
    ph = PacketHeaderC.from_buffer(data)
    
    
    #if ret == 0:
    #    print("no data")
    #    return (None,None,None,None,None)
    #print("header version {:x},ret {} ".format(ph.version,ret ))     
    
    if ph.version != 0xAA55AA59:
        print("Bad header version {:x}".format(ph.version ))
        return (None,None,None,None,None)

    #print(("Frame #:{} tot_len:{} header_len:{} ret_val:{}".format(ph.timestamp,ph.total_lenght,ph.header_len,ret)))
    if ph.total_lenght != 0:
        #timer.restart()
        data = BufferedRead(ph.total_lenght-ret ,s)
        #timer.get_time("BufferedRead")
                
    else:
        print("no len")
        return(ph,None,None,None,None)

    #timer.restart()
    view = memoryview(data)
    #timer.get_time("memoryview")
    #print(current_tm())

    td_data  = FindSegment(view,SEGMENT_ID_TD,ph.segments,ph.header_len)
    fd_data  = FindSegment(view,SEGMENT_ID_FD,ph.segments,ph.header_len)
    ld_data  = FindSegment(view,SEGMENT_ID_LD,ph.segments,ph.header_len)
    lft_data = FindSegment(view,SEGMENT_ID_FLATTENING,ph.segments,ph.header_len)

    #print(current_tm())

    return (ph,td_data,fd_data,ld_data,lft_data)





def reverseBits( x, intSize):

    y=0
    for pos in range(intSize-1,-1,-1):
        y = y + ((x&1)<<pos)
        x = x>>1
        
    return y

def BuildLookupTable( fft_out_len):
    fft_lookup_table=[]
    for i in range(0,fft_out_len):
        ReversedIdx = reverseBits(i, fft_out_len.bit_length() - 1)
        actualIdx = fft_out_len - 1 - ReversedIdx
        fft_lookup_table.append(actualIdx)
    return fft_lookup_table


def bytearrat2array(ba):
    a = array.array('H')
    for i in range(0,len(ba)/2):
        l = ba[i*2]
        h = ba[i*2+1]
        a.append(h<<8 + l)
    return a

def GetFFTPixel( buf,pixel,  time, fft_out_len, cur_fft, num_fft):
    offset = (time % 128) +  (pixel %15) *128 +  (time//128) *128*15   +(pixel//15)*15*fft_out_len*num_fft +  15*fft_out_len*cur_fft
    #print "a",offset ,pixel,  time, fft_out_len, cur_fft, num_fft
    n = int(buf[ offset *2 ]) + int(buf[ offset*2+1  ]) * 256
    return n



  
  


            

#BuildLookupTable(dpCache.fft_out_len,dpCache.log_fft_in_len,fft_lookup_table)

def calc(buf,pix,nfft,fft_out_len,num_fft,fft_in_len,fft_lookup_table):
    maxVal = 0
    maxValIdx = 0
    for smpl in range(0,fft_out_len) :
        tmpVal =  GetFFTPixel(buf, pix,  fft_lookup_table[smpl],fft_out_len,nfft,num_fft)
        if tmpVal > maxVal:
            
            maxVal    = tmpVal
            maxValIdx = smpl
            
    actualFreq = maxValIdx * 48000.0 / fft_in_len
    return actualFreq
                
def GetGenFreq(pix,nfft,mode):
    if mode == 1:
        return  24000.0 / (freq_table.get_pixel_freq(pix,nfft)+2)
    else:
        return  24000.0 / (pix+2)


def calcFreqAndCompare300Pixels(fd_data,td_data,ph,fft_lookup_table,mode,tolerance,dump):

    bad=0
    count=0

    for pix in range(0,300):
        actualFreq = calc(fd_data,pix,0,ph.fft_out_len,ph.num_fft,ph.fft_in_len,fft_lookup_table)
        genFreq = GetGenFreq(pix,ph.frame %3 ,mode)
        #print ("Pix {} Gen {} actual{}".format(pix,int(genFreq),int(actualFreq)))
        count=count+1
        if abs(genFreq-actualFreq) > tolerance:
            bad=bad+1
            print ("Pix {} Gen {} actual{}, mode {}".format(pix,int(genFreq),int(actualFreq),mode))
        
        if dump ==1:
            ftd = open("td_frame_"+str(frame)+"_pix_"+str(pix)+".csv","w")    
            ffd = open("fd_frame_"+str(frame)+"_pix_"+str(pix)+".csv","w")
            print("Dumping TD")
            for  t in range(0,ph.fft_in_len):
                print(convert.GetTDSample(td_data,t,pix),file=ftd)
            print("Dumping FD")
            for  t in range(0,ph.fft_out_len):
                print(GetFFTPixel(fd_data,pix,  fft_lookup_table[t],ph.fft_out_len,0,1),file=ffd)
            ftd.close()
            ffd.close()    

    return bad, count


fft_lookup_table=[]

def ProcesPacket(s,tolerance,n,mode,dump):

    a_ph=[]
    a_td_data=[]
    a_fd_data=[]
    #a_lft_data = []
    timer = Timer()
    timer2 = Timer()
    print("ProcesPacket - Starting")
    for frame in range(0,n):
        #timer.restart()
        (ph,td_data,fd_data,laser_data,lft_data) = ReadPacket(s)
        #timer.get_time("ReadPacket Done")
    
        #assert ph.frame == frame
        a_ph.append(ph)
        a_td_data.append(td_data)
        a_fd_data.append(fd_data)
        #a_lft_data.append(lft_data)

    print("Done receiving {} Frames".format(n))
    timer2.get_time("ProcesPacket")

    global fft_lookup_table
    if len(fft_lookup_table) == 0:
        fft_lookup_table = BuildLookupTable(ph.fft_out_len)
        
    bad=0
    count=0

    if (n > 5): #more than 5 frames - check ONLY the last one
        ph= a_ph[n-1]
        td_data = a_td_data[n-1]
        fd_data = a_fd_data[n-1]

        bad, count = calcFreqAndCompare300Pixels(fd_data,td_data,ph,fft_lookup_table,mode,tolerance,dump)
        print("checked Frame {}: {} bad from {}".format(n,bad,count))

    else:
        print("loop on calcFreqAndCompare300Pixels Per Frame - Starting ")
        for frame in range(0,n):
            ph= a_ph[frame]
            td_data = a_td_data[frame]
            fd_data = a_fd_data[frame]

            for fft in range(0,1):
                timer.restart()
                bad, count = calcFreqAndCompare300Pixels(fd_data,td_data,ph,fft_lookup_table,mode,tolerance,dump)
                timer.get_time("calcFreqAndCompare300Pixels - Done")

        print("{} bad from {}".format(bad,count))
        timer2.get_time("ProcesPacket Done")
    return bad



def ProcesTestPacket(s):

    a_ph=[]
    a_td_data=[]
    a_fd_data=[]

    
    (ph,td_data,fd_data,laser_data,lft_data) = ReadPacket(s)
        #assert ph.frame == frame
    
    for pix in range(0,300):
    #for pix in range(0,20):
        sum=0
        for t in range(0,ph.fft_in_len):
            val= convert.GetTDSample(td_data,t,pix)
            sum = sum + val
        
        if sum != 65536:
            if pix not in (25,65,75,105,155,195,225,265,275):
                print("Pix " + str(pix) + " sum " + str(sum)    ) 
        
        #if pix == 4:
           # if sum <= 10000 or sum > 11000:
         #       print("Pix " + str(pix) + " sum " + str(sum)    ) 

    return 0



def ValidateAndPackSR(sr, sr_valid):
    reg8 = 0
    bit = 0


    out = np.zeros(64,dtype=int)
    for  i in range(0,512):
        if sr_valid[i] != 1:
            return None

        reg8 = reg8 | (sr[i] << bit);
        bit= bit+1
        if bit == 8:
            out[i//8]  = reg8
            reg8 = 0
            bit = 0

    return out

def print_hex(h):
    return format(h, '02x')+" "


def ReadSR(name,override_list=[]):

    sr_valid = np.zeros(512,dtype=int)
    sr = np.zeros(512,dtype=int)
    sr2 = np.zeros(512,dtype=int)

    with open(name) as csvfile:


        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row)
            if row['Parameter name'] != '' and row['SR<bit:'] != '' :

                
                name = row['Parameter name']
                
                
                start = int(row['SR<bit:'])
                end = int(row['bit>'])
                # print(row)
                normal = int(row['Normal'])
                protected = int(row['Protected'])
                
                for e in override_list:
                    if name == e[0] :
                        normal = e[1]
                        protected = e[2]
                        print('Found override candidate ',name,' Normal ', normal, ' protected ',protected) 
                

                for  i  in range(start,end+1):
                    if sr_valid[i] == 1:
                      return None

                    sr[i] = normal & 1
                    normal >>= 1
                    sr_valid[i] = 1

                    sr2[i] = protected & 1
                    protected >>= 1;

    out_normal    = ValidateAndPackSR(sr,sr_valid)
    out_protected = ValidateAndPackSR(sr2, sr_valid)

    if 0:
        for i in range(0,8):
            print(  print_hex(out_normal[i*8+0]),print_hex(out_normal[i*8+1]),print_hex(out_normal[i*8+2]),print_hex(out_normal[i*8+3]),print_hex(out_normal[i*8+4]),print_hex(out_normal[i*8+5]),print_hex(out_normal[i*8+6]),print_hex(out_normal[i*8+7]) )

        print("-------------------")
        for i in range(0, 8):
            print(print_hex(out_protected[i * 8 + 0]), print_hex(out_protected[i * 8 + 1]), print_hex(out_protected[i * 8 + 2]),
                  print_hex(out_protected[i * 8 + 3]), print_hex(out_protected[i * 8 + 4]), print_hex(out_protected[i * 8 + 5]),
                  print_hex(out_protected[i * 8 + 6]), print_hex(out_protected[i * 8 + 7]))

    sr = bytearray(64)
    sr2= bytearray(64)
    for i in range(0, 64):
        sr[i] = out_normal[i]
        sr2[i] = out_protected[i]

    return sr,sr2


def ReadPixelMap(filename):	
    file = open(filename, "rU")
    reader = csv.reader(file)

    
    a = []

    for row in reader:
        a.append (row)
    
    
    file.close()
    return a

def GetFPGAPixel(pm,physical_pixel):

    line = physical_pixel // 30
    col = physical_pixel % 30
    return int(pm[line][col])
    


def GetFFTVector(buf,pix,ph,area):

    vec = np.zeros(ph.fft_out_len, dtype=float)

    global fft_lookup_table
    if len(fft_lookup_table) == 0:
        fft_lookup_table = BuildLookupTable(ph.fft_out_len)
    
    
    for smpl in area :
        #print("smpl",smpl)
        if smpl < len(fft_lookup_table):
            tmpVal =  GetFFTPixel(buf, pix,  fft_lookup_table[smpl],ph.fft_out_len,0,1)
            vec[smpl]= tmpVal            
    
    
    return vec


if __name__ == "__main__":

    
    #s = socket.socket(
    #socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((sys.argv[1], 9999))
    
    #while(1):
    #(ph,td_data,fd_data,ld_data) = ReadPacket(s)
    #print(ph.frame)    
    #ProcesPacket(s,4,10,1,0)
    ReadSR(sys.argv[1])



