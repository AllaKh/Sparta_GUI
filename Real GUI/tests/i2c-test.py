
import time,threading,sys
import time
import socket
import spartautils,convert
import msgpackrpc,time
import numpy as np





def rpc_client(host):



    #Connect to FPGA
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080),timeout=120)

    


    #i2cdata=  bytes([0x40,0x80,0x78,0x42,0x80,0x78,0x46,0x80,0x78])

    v = int(sys.argv[2])

    print("V is "+ str(v) +" mV" )

    d = int(round(v/0.3))

    h = 0x80 | ( (d>>8) & 0xF )
    l = (d)& 0xFF
    

    i2cdata = bytes([0x40,h,l])

    #print(print (''.join('{:02x}'.format(x) for x in i2cdata)))


    client.call('SendString',"I2c Test")
    client.call('SendI2C', 0x60    , i2cdata)


        
  
        


if __name__ == "__main__":

    
    rpc_client(sys.argv[1] )
    
    
