#!/usr/bin/env python3
import msgpackrpc
import sys,time
import socket
import spartautils
import convert
import matplotlib.pyplot as plt
from scipy import signal

def init(host):
    
    print("Connect to",host)
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080))
    client.call('StopStreaming')
    return client





def adc_test(host,use_adc,single):
    
    client = init(host)
    state = client.call('GetState')    
    print("State", state)

    client.call('StartStreaming',1)


    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 9999))
    (ph,td_data,fd_data,ld_data,lft_data) = spartautils.ReadPacket(s)
    #(ph,td_data,fd_data) = spartautils.ReadPacket(s)
    #(ph,td_data,fd_data) = spartautils.ReadPacket(s)
    
    
    #file = open('td.bin', 'wb')
    #file.write(td_data)
    #file.close()

    #last = convert.GetSample(td_data,1024*3*32-1,1,0)
    #print("Last {:x}".format(last))
        


    rng = range(0,ph.td1_len)
    # rng = range(0,32*1024*1)
    (pd0,pd1,pd2,pd3) = convert.ProcessTP(td_data,rng,range(1,2),0)
    #(l_rng,l_1,l_2,l_3)= GetLaserData(ld_data)
    
    if single:
        client.call('StopStreaming')
    else:    
       plt.ion()
       

    

    fig = plt.figure()
    
    ax0  = fig.add_subplot(221)
    sc0, = ax0.plot(rng,pd2,'.')
    ax0.set_ylim([0,65536])

    
    if single:
        a=plt.show()
    else:    
        i = 0
        while True:
            a= fig.canvas.draw()
            fig.canvas.flush_events()
            print("aa",a)
            (ph,td_data,fd_data,ld_data,lft_data) = spartautils.ReadPacket(s)
            (pd0,pd1,pd2,pd3) = convert.ProcessTP(td_data,rng,range(1,2),0)
           # (l_rng,l_1,l_2,l_3)= GetLaserData(ld_data)
            
            sc0.set_data(rng,pd2)
    
            ax0.set_ylim([min(pd2),max(pd2)])
            

           

            i=i+1
            if i>2:
                f=open("frame{}.txt".format(i),"w")
                for d in pd2:
                    f.write(str(d)+"\n")
                    #print(d)
                f.close()    
            #plt.show()   
            time.sleep(1)
            
       

    client.call('StopStreaming')
    
def GetLaserData(stream):
    import struct
    
    l =(6000 )

    rl=2000

    print(len(stream) )
    count = int(len(stream)/2)
    print(len(stream) ,count)
    s16 = struct.unpack('H'*count, stream)
    
    
    set1 = s16[l:l+rl]
    set2 = s16[2*l:2*l+rl]


    setx1=[]
    setx2=[]
    for i in set1:
        
        setx1.append( 255 - i)
    for i in set2:
        setx2.append( 255 - i)
        
        


    return (range(0,rl),s16[0:rl],setx1 ,setx2 )

if __name__ == "__main__":
   adc_test(sys.argv[1],True,False)