import sys
import msgpackrpc



  
        


if __name__ == "__main__":

    client =  msgpackrpc.Client(msgpackrpc.Address(sys.argv[1], 8080),timeout=120)
    client.call('SetInitialVCO',int(sys.argv[2]))
    
    
    
