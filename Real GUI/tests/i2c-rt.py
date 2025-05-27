
import time,threading,sys
import time
import socket
import spartautils,convert
import msgpackrpc,time
import numpy as np


def VtoH(value):
    return int(value*4096.0/2086.0)

def ToHex(d):
    h = 0x80 | ( (d>>8) & 0xF )
    l = (d)& 0xFF
    return h,l

def rpc_client(host):



    #Connect to FPGA
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080),timeout=120)

    vnormal    =   VtoH(int(sys.argv[2]))
    vprotected =   VtoH(int(sys.argv[3]))



    normal =    [0x42,ToHex(vnormal)[0],ToHex(vnormal)[1]]
    protected = [0x42,ToHex(vprotected)[0],ToHex(vprotected)[1] ]


    
    if sys.version_info[0] == 3:
        i2cdata_normal=  bytes(normal)
        i2cdata_protected=  bytes(protected)

    else:
        i2cdata_normal=  str(bytearray(normal))
        i2cdata_protected=  str(bytearray(protected))


   # client.call('SendString',"I2c Test")
    client.call('SendI2CX', 0x60    , i2cdata_normal,1)
    client.call('SendI2CX', 0x60    , i2cdata_protected,2)
    for v in i2cdata_normal:
      print (hex(v))
    for v in i2cdata_protected:
      print (hex(v))
    
        
  
        


if __name__ == "__main__":

    
    rpc_client(sys.argv[1] )
    
    
