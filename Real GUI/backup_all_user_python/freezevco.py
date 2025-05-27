import sys
import msgpackrpc



  
        


if __name__ == "__main__":

    client =  msgpackrpc.Client(msgpackrpc.Address(sys.argv[1], 8080),timeout=120)
    
    
    if sys.argv[2] == 'start' :
        client.call('StopStreaming')
        client.call('StartStreaming',1)
        sys.exit(0)
    
    freeze = int(sys.argv[2])

    
    
    client.call('FreezeVCO',freeze)
    
    
    
