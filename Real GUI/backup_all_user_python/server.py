import inspect
import msgpackrpc
import threading

import socket,sys,time

"""
enum class RpcState{ Ready=0, Waiting = 1, Streaming =2 ,Stopping = 3};
"""

    

class FPGA(object):
    def __init__(self):
        self.clientsocket = None
        self.serversocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(("0.0.0.0", 9999))
        self.serversocket.listen(1)
        self.serversocket.settimeout(1)
        self.state = 0
        print("Init 9999",socket.gethostname())
        self.period = 60000000        
        self.regmap = dict = {0x1d0: 12,0x1D4:276}
        self.counter = 0
        
        
    def Streaming(self):

        print("Waiting for client")
        
        while self.running:
            try:
               
                (self.clientsocket, address) = self.serversocket.accept()
                
                break
            except socket.timeout: 
                print("accept timeout..")
                continue
            except  Exception as e:
                print("Strange..",str(e))

        if not self.running:
            print("Close thread")
            return

        print("Got it")
        
        while self.running:
        #accept connections from outside
            
            #print ("Got socket")
            #now do something with the clientsocket
            #in this case, we'll pretend this is a threaded server
            
            file = open(sys.argv[1], "rb")
            
            while self.running:
                chunk = file.read(65536)
                print("sleep",self.period/300000000)
                #time.sleep(self.period/300000000)
                
                if not chunk:
                     break  # EOF
                
                try:
                    self.clientsocket.send(chunk)
                except Exception as e:
                    print("exeption on send",str(e))
                    file.close()
                    return
                
            file.close()
            
    def StopStreaming(self):
        print( inspect.stack()[0][3] )
        if self.clientsocket != None :
            print("Shutdown socket")
            self.running = False
            self.clientsocket.settimeout(1)
            self.clientsocket.shutdown(socket.SHUT_RDWR)
            self.sT.join()
            print("THread stopped")
            self.clientsocket.close()
            self.clientsocket= None
            
        self.state = 0    
        print("Stopped")
        return 0
    def StartStreaming(self,start):
        print( inspect.stack()[0][3] )

        if self.state != 0:
            return -5
        
        self.sT = threading.Thread(target=FPGA.Streaming,args=[self])
        self.sT.daemon = True
        self.running = True
        self.state = 2
        self.sT.start()

        return 0
    def SendShiftRegister(self,sr):
        print( inspect.stack()[0][3] )
        fh = open('shiftregister.txt', 'w') 
        for i in sr:
            fh.write(format(i,'d')+'\n')
        fh.close()    
        if self.state != 0:
            return -5

        return 0    
    def SendIO(self,reg,mask):
        print( inspect.stack()[0][3],hex(reg),hex(mask) )
        if self.state != 0:
            return -5

        return 0    
    def SetPeriod(self,period):
        print( inspect.stack()[0][3] )
        if self.state != 0:
            return -5
        self.period = period

        return 0    
    def GetState(self):
        print( inspect.stack()[0][3] )
        return self.state   
    def GetVersionX(self):
        print( inspect.stack()[0][3] )
        return "1.0.1\n2.0.2"
    def ReadRegister(self,reg):
        if reg == 0x1D8:
            self.counter = self.counter+ 0.01*300000000
            return self.counter
        return self.regmap[reg];
        
def worker():
    server = msgpackrpc.Server(FPGA())
    #fpga = FPGA()
    #fpga.StartStreaming(1)
    server.listen(msgpackrpc.Address("localhost", 8080))
    server.start()
        
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage server.py filename")
        exit(1)

    t = threading.Thread(target=worker)
    t.daemon  = True
    t.start()
    import sys
    print("Press ENTER to exit")
    data = sys.stdin.readline()
    
    
    
