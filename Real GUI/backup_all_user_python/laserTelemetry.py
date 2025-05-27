
#!/usr/bin/env python3
import msgpackrpc
import sys,time
import socket
import spartautils
import convert
import matplotlib.pyplot as plt


################
# save2File
################
def save2File(mct_len, vco_len, mct_set, vco_set, frame, mLen, vLen):

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
def GetLaserData(stream):
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
    print("mct_len=",mct_len)

    #Handle VCO after MCT
    vco_len = s16[mct_len+1]
    print("vco_len=",vco_len)
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
def init(host):
    
    print("Connect to",host)
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080))
    client.call('StopStreaming')
    return client

####################
# laser_buffer_test
####################
def laser_buffer_test(host, single):
    import struct
    import time;

    #init
    client = init(host)
    state = client.call('GetState')    
    print("State", state)

    client.call('SetSendNetDataMask',14)

    if single:
        client.call('StartStreamingSingle',1)
    else:
        client.call('StartStreaming',1)

    # open socket to receive the packets
    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 9999))

    #read packet and extract laser buffer data
    (ph,td_data,fd_data,ld_data,lft_data) = spartautils.ReadPacket(s)
    (mct_len, vco_len, mct_set, vcoByteSet, mLen, vLen)= GetLaserData(ld_data)
    
    if single:
        client.call('StopStreaming')
    else:    
       plt.ion()

       lftName = "lft_data_"+str(time.time())+".txt"
       lfile = open(lftName, "a")
       lfile.write("Index / MeanPower / Flatness")
       lfile.write("\n")
       frame = 0  


    #create plots
    fig = plt.figure()
    fig1 = plt.figure()

    ax1 =  fig.add_subplot(222,title="Laser MCT Samples")
    sc1, = ax1.plot(mct_len,mct_set,'-')

    displayIndex = 222
    #dispaly a point value - for example 
    ax1.annotate(str(mct_set[displayIndex]),xy=(displayIndex,mct_set[displayIndex]))

    ax2 =  fig1.add_subplot(223,title="Laser VCO Samples")
    sc2, = ax2.plot(vco_len,vcoByteSet,'-')
    ax2.annotate(str(vcoByteSet[displayIndex]),xy=(displayIndex,vcoByteSet[displayIndex]))


    if single:
        a=plt.show()
    else:    
        while True:
            a= fig.canvas.draw()
            b= fig1.canvas.draw()
            print(">>> processing frame: "+str(frame) )
            (ph,td_data,fd_data,ld_data,lft_data) = spartautils.ReadPacket(s)
            (mct_len, vco_len, mct_set, vcoByteSet, mLen, vLen)= GetLaserData(ld_data)

            lft = struct.unpack('id', lft_data)
            lfile.write(str(frame)+" "+str(lft[0])+" "+str(lft[1]))
            lfile.write("\n")

            save2File(mct_len, vco_len, mct_set, vcoByteSet,frame, mLen, vLen)
            frame = frame +1

            sc1.set_data(mct_len,mct_set)
            sc2.set_data(vco_len,vcoByteSet)       
            plt.pause(0.01)       

    client.call('StopStreaming')
    lfile.close()

####################
# main
####################  
if __name__ == "__main__":
   laser_buffer_test(sys.argv[1],False)

