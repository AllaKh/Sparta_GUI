
import pytest,paramiko,time,threading,sys
import time
import socket
import spartautils
import msgpackrpc,time


def rpc_client(host):

    

    
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080),timeout=120)
    client.call("SendI2C")
#   client.call('StopStreaming') == 0
#   client.call('SetPeriodUs',800000)  == 0
#
#   for b in range(0,100):
#       print("Test ",b)
#
#       s = socket.socket(
#       socket.AF_INET, socket.SOCK_STREAM)
#       s.connect((host, 9999))
#
#       client.call('StartStreaming',1) == 0
#
#
#       spartautils.ProcesTestPacket(s)
#
#       client.call('StopStreaming') == 0
#
#       s.close()

        
  
        


if __name__ == "__main__":

    
    rpc_client(sys.argv[1] )
    
    
