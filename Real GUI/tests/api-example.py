
import time,threading,sys
import time
import socket
import spartautils,convert
import msgpackrpc,time
import numpy as np



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


def rpc_client(host):

    normal,protected = spartautils.ReadSR(sys.argv[2])


    #Connect to FPGA
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080),timeout=120)

    #To be on safe side , stop streaming
    client.call('StopStreaming') == 0

    #Set Period to 800ms
    client.call('SetPeriodUs',800000)  == 0
    

    #Do 2 session
    for session in range(0,2):
        print("Session ",session)

        #Connect data socket
        s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 9999))

        client.call('SendShiftRegisterEx', normal, 0)


        client.call('SendShiftRegisterEx', protected, 1)


        #start streaming
        client.call('StartStreaming',1) == 0

        #Capture 5 frames
        (ph,a_td_data,a_fd_data)=CaptureFrames(s,5)

        #Stop Streaming
        client.call('StopStreaming') == 0

        #Close socket
        s.close()

        #Process data, 5 frames, pixel 269
        ProcesTestPacket(ph, a_td_data,a_fd_data, 5, 269)
        
  
        


if __name__ == "__main__":

    
    rpc_client(sys.argv[1] )
    
    
