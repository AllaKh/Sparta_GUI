import time,threading,sys
import time
import socket
try:
    import spartautils,convert
except:
    pass

import msgpackrpc,time
import numpy as np
import pandas as pd

_debug=True

def CaptureFrames(s,n):
    a_ph = []
    a_td_data = []
    a_fd_data = []

    for i in range(0,n):
        (ph, td_data, fd_data ,a,b) = spartautils.ReadPacket(s)
        a_td_data.append(td_data)
        a_fd_data.append(fd_data)

    return ph,a_td_data,fd_data

def ProcesTestPacket(ph,a_td_data,fd_data,n,pix):

    for i in range( 0,n):
        td_data= a_td_data[i]
        print (td_data)
        sum=0
        for t in range(0, ph.td1_len):
            val = convert.GetTDSample(td_data, t, pix)
            sum = sum + val

        print("Frame ",i, " data ", sum/ph.td1_len*100.0 )

    return 0

def getTDData(ph,a_td_data,pix):

    td_data= a_td_data.tolist()
    data=[]
    for t in range(0, ph.td1_len):
        val = convert.GetTDSample(td_data, t, pix)
        data.append(val)

    return(data)


def getFDData(ph, a_fd_data, fd_data, n, pix):
    fd_data = a_fd_data.tolist()
    data = []
    for t in range(0, ph.td1_len):
        val = convert.GetTDSample(fd_data, t, pix)
        data.append(val)

    return (data)

def rpc_client(host,sessions_num=1,frames=1,savefile=r'C:\debug.csv',pixel=299):

    #Connect to FPGA

    #print("The Host adress is:",host)
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080),timeout=60)

    #To be on safe side , stop streaming
    client.call('StopStreaming') == 0

    #Set Period to 800ms
    client.call('SetPeriodUs',100000)  == 0

    client.call('SetSendNetDataMask',1)

    #for session in range(0,sessions_num):

    #print("Session ",session)

    #Connect data socket
    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 9999))
    #start streaming
    client.call('StartStreaming',1) == 0

    (ph,a_td_data,a_fd_data)=CaptureFrames(s,frames)

    #Stop Streaming
    client.call('StopStreaming') == 0

    #Close socket
    s.close()

    df = pd.DataFrame()
    for i in range(0,frames):
        data_td = getTDData(ph,a_td_data[i], pixel)
        df["TD_Frame%d"%i]=data_td
    #data_fd =

    if _debug:

        df.to_csv(savefile)

    return(df)
        #Process data, 5 frames, pixel 269
        #ProcesTestPacket(ph, a_td_data,a_fd_data, 5, 299)
        
  
        


if __name__ == "__main__":

    if len(sys.argv)>1:
        host=sys.argv[1]
        print("HOST:",host)
        sessions_num = int(sys.argv[2])
        print("Sessions:", sessions_num)
        frames = int(sys.argv[3])
        print("Frames::", frames)
        savefile = sys.argv[4]
        print("Saving to -->:", savefile)
    else:
        host="10.99.0.125"
        sessions_num=1
        frames = 1
        savefile=r'C:\Debug\fpga\td_data.csv'


    rpc_client(host,sessions_num,frames,savefile)

    
