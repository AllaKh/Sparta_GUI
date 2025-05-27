
#!/usr/bin/env python3
import msgpackrpc
import sys,time
import socket
import spartautils
import convert
import matplotlib.pyplot as plt
import threading
import struct
import numpy as np
class FlatUtil():
    def __init__(self,host,naive_connect):
        if naive_connect:
            self.client = self.naive_init(host)
        else:
            self.client = self.init(host)

        self.running = False
        self.host=host
        self.mct=None
        
        pass
    ################
    # save2File
    ################
    def save2File(self,mct_len, vco_len, mct_set, vco_set, frame, mLen, vLen):

        mctName = "mct_data_frame_"+str(frame)+".txt"
        vcoName = "vco_data_frame_"+str(frame)+".txt"

        mfile = open(mctName, "w")  
        mfile.write("Frame "+str(frame)+" mct samples "+str(mLen)+"\n")

        vfile = open(vcoName, "w") 
        vfile.write("Frame "+str(frame)+" vco samples "+str(vLen)+"\n")

        for i in range(0, mLen-1):
            mfile.write(str(i)+" "+str(mct_set[i])) 
            mfile.write("\n")

        for i in range(0, vLen-1):
            vfile.write(str(i)+" "+str(vco_set[i]))
            vfile.write("\n")    

        mfile.close()
        vfile.close()

    ################
    # GetLaserData
    ################
    def GetLaserData(self,stream):
        import struct

        # How is the data organized?
        # MCT vector Length (2B) | mct sample_X(2B) ...| VCO vector Length (2B) | vco sample_X(1B)....|

        # unpack the entire stream into a list of 
        # unsigned short (2 Bytes)
        count = int(len(stream)/2)
        s16 = struct.unpack('H'*count, stream)
        
        #Handle MCT first
        mct_len = s16[0]
        mct_set = s16[1:mct_len]
        #print("mct_len=",mct_len)

        #Handle VCO after MCT
        vco_len = s16[mct_len+1]
        #print("vco_len=",vco_len)
        vco_set = s16[int(mct_len+2):int( (mct_len+2+(vco_len/2)) )]

        #vco_len is a length of 1 Byte VCO vector

        #break vco_set into 1 Byte entries:
        vcoByteSet = []
        for i in range(0,int(vco_len/2)):  
            vcoByteSet.append(vco_set[i] & 0xFF)
            vcoByteSet.append((vco_set[i] & 0xFF00)>>8)

        return (range(1,mct_len), range(1,vco_len), mct_set, vcoByteSet, mct_len, vco_len)

    ################
    # Init
    ################
    def init(self,host):
        
        print("Connect to",host)
        client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080))
        client.call('StopStreaming')
        return client

    def naive_init(self,host):
        
        print("Connect to",host)
        client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080))
        # client.call('StopStreaming')
        return client

    def thread_function(self,s):   
        self.running = True
        while self.running:
            (ph,td_data,fd_data,ld_data,lft_data) = spartautils.ReadPacket(s)
            (mct_len, vco_len, mct_set, vcoByteSet, mLen, vLen)= self.GetLaserData(ld_data)
            self.vcoByteSet = list(vcoByteSet).copy()
            self.mctByteSet = list(mct_set).copy()
            #print ( type(mct_set))
        
    ####################
    # laser_buffer_test
    ####################
    def start(self ):
        import struct
        import time;

        #init
        client = self.client
        state = client.call('GetState')    
        print("State", state)

        client.call('SetSendNetDataMask',12)
        

        client.call('StartStreaming',1)

        
        
        # open socket to receive the packets
        s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, 9999))

        self.t = threading.Thread(target=self.thread_function, args=[s])
        self.t.daemon=True
        self.t.start()
        #read packet and extract laser buffer data
        
    def stop(self ):    
        self.running = False
        self.t.join()
        self.client.call('StopStreaming')
        
    def GetMctVector(self):
        return self.mctByteSet
    
    def GetVcoVector(self):
        return self.vcoByteSet
        
    def UpdateVCO(self,data):
        assert( max(data) < 256 )
            
        self.client.call('FreezeVCO',2)
        vcolen = len(data)
        v = struct.pack('B'*vcolen,*data)
        self.client.call('UpdateVCO',v)

    def UpdatePiezo(self,data):
        assert( max(data) < 65536 )
            
        
        piezoen = len(data)
        #v = struct.pack('I'*piezoen,*data)
        self.client.call('UpdatePiezo',data.tolist() )

        print (len(data.tolist()))
            
####################
# main
####################  

# import flatutil in your code as
# import flatutil

if __name__ == "__main__":
   fu = FlatUtil(sys.argv[1] )
   fu.start()
   time.sleep(5)
   print(fu.GetVcoVector())
   print(fu.GetMctVector())


   x1= np.linspace(1500,600,1226,dtype=np.int32)
   x2= np.linspace(600,600,1226,dtype=np.int32)
   x3= np.linspace(600,1500,1226,dtype=np.int32)
   v =  np.concatenate((x1,x2,x3))
   fu.UpdatePiezo(v)

    
   
   i = 0
   while 1:
    
    # a should be  list
    # unsigned int
    # less than 256
    a=[]
    for j in range(0,1300) :
        a.append((j+i)%256)
    i+=50    
    
    fu.UpdateVCO(a)
    time.sleep(1)
    print("update ",i)
   
   fu.stop()

