#!/usr/bin/env python3
import msgpackrpc
import sys,time
import socket
import spartautils
import convert
import matplotlib.pyplot as plt

def init(host):
    
    print("Connect to",host)
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080))
    client.call('StopStreaming')
    return client


def adc_setup(client):
    
    
    client.call('WriteRegister',0x60,0)

    client.call('AdcReset')

    client.call('AdcWriteRegister',0x42,0x8060)
    client.call('AdcWriteRegister',0x46,0x8800)
    client.call('AdcWriteRegister',0x25,0x10)
    client.call('AdcWriteRegister',0x26,0xB0B0)

    client.call('WriteRegister',0x60,1)

    n=0
    while n<100:
        reg = client.call('ReadRegister',0x1E0)
        if reg == 1:
           break
        n=n+1
        time.sleep(0.1)

    #print("waited for adc sync", n/10)
    
    client.call('AdcWriteRegister',0x26,0x1234<<2)
    
    time.sleep(0.2)
    
    return client.call('ReadRegister',0x1CC)



def adc_test(host,use_adc,single):
    
    client = init(host)
    state = client.call('GetState')    
    print("State", state)

    if use_adc:
        for i in range(0,100):
            reg = adc_setup(client)
            print("Attempt {},Pattern {:x} ".format(i,reg))
            if ( reg == 0x1234):
                break
        client.call('AdcWriteRegister',0x25,0x40)
        read = client.call('AdcReadRegister',0x46)
        print("read 0x46",format( read,'04x'))
            

    client.call('AdcWriteRegister',0x25,0x0)

    if single:
        client.call('StartStreamingSingle',1)
    else:
        client.call('StartStreaming',1)

    reg = client.call('ReadRegister',0x1E0)
    print("Sync done",reg)

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
    (l_rng,l_1,l_2,l_3)= GetLaserData(ld_data)
    
    if single:
        client.call('StopStreaming')
    else:    
       plt.ion()
       

    

    fig = plt.figure()
    
    ax0  = fig.add_subplot(221)
    sc0, = ax0.plot(rng,pd1,'.')
    ax0.set_ylim([0,65536])

    ax1 =  fig.add_subplot(222)
    sc1, = ax1.plot(l_rng,l_1,'.')

    ax2 =  fig.add_subplot(223)
    sc2, = ax2.plot(l_rng,l_2,'.')
    #ax2.set_ylim([0,256])

    ax3=fig.add_subplot(224)
    sc3, = ax3.plot(l_rng,l_3,'.')
    #ax3.set_ylim([0,256])

    if single:
        a=plt.show()
    else:    
        i = 0
        while True:
            a= fig.canvas.draw()
            print("aa",a)
            (ph,td_data,fd_data,ld_data,lft_data) = spartautils.ReadPacket(s)
            (pd0,pd1,pd2,pd3) = convert.ProcessTP(td_data,rng,range(1,2),0)
            (l_rng,l_1,l_2,l_3)= GetLaserData(ld_data)
            
            sc0.set_data(rng,pd1)
            sc1.set_data(l_rng,l_1)
            sc2.set_data(l_rng,l_2)
            sc3.set_data(l_rng,l_3)

            ax1.set_ylim([min(l_1),max(l_1)])
            ax2.set_ylim([min(l_2),max(l_2)])
            ax3.set_ylim([min(l_3),max(l_3)])


            print(  "Reg=",  client.call('ReadRegister',0x14)  )

            #i=i+1
            #if i==5:
            #     plt.show()   
            #     time.sleep(120)
            
       

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