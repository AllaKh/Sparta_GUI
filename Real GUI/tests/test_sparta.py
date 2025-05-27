
import pytest,paramiko,time,threading,sys
import python_regs
import io


def out_thread(stdout,e,log):
    for line in iter(lambda: stdout.readline(2048), ""):
        log.write(line)
        if "Waiting for incoming connections" in line:
            e.set()
        if "spartaLinux already running, exiting" in line:
            e.set()


            




@pytest.fixture(scope="module")
def rpc_client(cmdopt,diropt):
    import msgpackrpc,time
    
    e = threading.Event()
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(cmdopt,username='root',password='')
    cmd = 'cd ' + diropt+ ' ;pwd;./spartaLinux --rpc'
    stdin,stdout,stderr = ssh.exec_command(cmd, get_pty=True)
    log = io.StringIO()
    sT = threading.Thread(target=out_thread,args=[stdout,e,log])
    sT.start()    
    startTime = time.time()
    e.wait(180)
    elapsedTime = time.time() - startTime
    print('Waited for spartaLinux ready {} ms'.format(   int(elapsedTime * 1000)))
    client =  msgpackrpc.Client(msgpackrpc.Address(cmdopt, 8080))
    assert client.call('StopStreaming') == 0
    assert client.call('SetPeriodUs',800000)  == 0
    yield client
    print("Stopping test")
    assert client.call('StopStreaming') == 0
    ssh.close()    
    print("ssh closed")
    print('-------------SPARTA.APP LOG BEGIN -------------------')
    print(log.getvalue())
    print('-------------SPARTA.APP LOG END -------------------')

#!  enum class RpcState{ Ready=0, Waiting = 1, Streaming =2 ,Stopping = 3};

#!This function is executed at the begining of each "test_xxxx"
@pytest.fixture(scope="function", autouse=True)
def printTestName(rpc_client, request):
    client = rpc_client
    print("--- Starting Test: "+request.function.__name__)
    client.call('SendString','(test_sparta.py) Starting Test: '+request.function.__name__)
    assert client.call('GetState') == 0
    client.call('SendString','(test_sparta.py) RpcState is READY')

def test_version(rpc_client,cmdopt):
    import time
    import socket
    import spartautils

    

    client = rpc_client

    
    ver = client.call('GetVersionX').decode('ascii')
    print("\n")
    print(ver)
    assert ver.find('dirty') == -1
    

#########################################################
#! test_R5_AysncCmdfollowedBySync 
#  This is a new test designed to check spartaSw 
#  ability to handle Async+sync command 
###########################################################
def test_R5_AysncCmdfollowedBySync(rpc_client,cmdopt):
    import threading
    client = rpc_client

    threadres=[1]
    t = threading.Thread(target=worker,args=[cmdopt,threadres])
    t.start()
    assert client.call('StartStreaming',1) == 0
    time.sleep(5)
    for s in range(1,5):
        assert client.call('SendIO',1,s) == 0
        print("************* SendIO - step ************************ ",s)
    time.sleep(3)
    assert client.call('StopStreaming') == 0
    t.join()

#!
#
def test_basic_connect(rpc_client):
    client = rpc_client

    assert client.call('GetState')      == 0 
    assert client.call('SendIO',1,1)    == 0
    sr=''
    for i in range(0,64):
        sr = sr +chr(i)

    
    result = client.call('SendShiftRegister',sr)
    assert (result == 0 ) or (result == -3 )
    assert client.call('StartStreaming',1)  == 0
    assert client.call('SendIO',1,1)        == 0
    assert client.call('StopStreaming')     == 0
            



def test_1000_calls(rpc_client):
    client = rpc_client
    
    for i in range(0,1000):
        assert client.call('GetState')      == 0 

    
def test_4_connects(rpc_client):
    client = rpc_client
        
    for i in range(0,4):
        assert client.call('StartStreaming',1)  == 0
        assert client.call('SendIO',1,1)        == 0
        assert client.call('StopStreaming')     == 0
        assert client.call('SendIO',1,1)        == 0
    
            
def worker(host,threadres):
    import socket,sys
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sys.stderr.write("here{}\n".format(host))
    s1.connect((host, 9999))
    #sys.stderr.write("connected\n")
    bytes_recd = 0
    while 1:
        chunk = s1.recv(65536)
        #sys.stderr.write(len(chunk))
        #sys.stderr.write("zz\n")
        if len(chunk) == 0:
                s1.close()
                threadres[0]=2
                break

def test_streaming(rpc_client,cmdopt):
    import threading
    import time
    client = rpc_client
    
    
    for step in range(1,3):
        threadres=[1]
        t = threading.Thread(target=worker,args=[cmdopt,threadres])
        t.start()
        #worker(cmdopt,threadres)
        assert client.call('StartStreaming',1) == 0
        time.sleep(5)
        assert client.call('StopStreaming') == 0
        sr=''
        for i in range(0,64):
            sr = sr +chr(i)
        result = client.call('SendShiftRegister',sr)
        assert (result == 0 ) or (result == -3 )
        assert client.call('SendIO',1,1)        == 0
        t.join()
        assert threadres[0]==2
    

def test_streaming_pushback(rpc_client,cmdopt):
    import threading
    import time
    import socket

    
    for step in range(1,3):
        client = rpc_client

        sr=''
        for i in range(0,64):
            sr = sr +chr(i)
        result = client.call('SendShiftRegister',sr)
        assert (result == 0 ) or (result == -3 )
    
        s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
        s.connect((cmdopt, 9999))
    
        assert client.call('StartStreaming',1) == 0
        assert client.call('SendIO',1,1)       == 0
        time.sleep(5)
        assert client.call('StopStreaming')    == 0
        assert client.call('SendIO',1,1)       == 0
        s.close()

@pytest.mark.skip(reason="Disabled, need to fix GUI")
def test_flatteningTelemetry(rpc_client,cmdopt):
    import time
    import socket
    import spartautils
    import struct

    SEGMENT_ID_FLATTENING_SIZE = 16

    client = rpc_client
    lft = spartautils.lsrFlatTelemetry()

    lft.meanPower = 0xBAD
    lft.flatness  = 0xBAD

    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cmdopt, 9999))

    assert client.call('SetPeriodUs',20000) == 0

    #configure 'SendNetDataMask' >>> only FLATTENING segment in the packet
    client.call('SetSendNetDataMask',0x8) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)

    assert client.call('StartStreaming',1) == 0

    for i in range(0,100):

        (ph,td_data,fd_data,laser_data,lft_data) = spartautils.ReadPacket(s) 

        #verify the returned packet contains only FLATTENING data
        assert ph.status == 1
        assert ph.frame == i
        assert ph.total_lenght == (ph.header_len+ SEGMENT_ID_FLATTENING_SIZE)

        (lft.meanPower,lft.flatness) = struct.unpack('id', lft_data[0:SEGMENT_ID_FLATTENING_SIZE])

        print("meanPower: {} " .format(lft.meanPower))
        print("flatness: {} " .format(lft.flatness))

        client.call('SendString',"frame {} meanPower: {} " .format(ph.frame, lft.meanPower))
        client.call('SendString',"frame {} flatness: {} " .format(ph.frame, lft.flatness))

    #reset 'SendNetDataMask' to defaults >>> TD+FD+FLATTENING
    client.call('SetSendNetDataMask',0xB) # == 1011 => (msb) 1(FLATTENING), 0(LD), 1(FD), 1(TD) (lsb)
    assert client.call('StopStreaming') == 0
    assert client.call('SendIO',1,1)        == 0

    s.close()

def test_process_data(rpc_client,cmdopt):
    import time
    import socket
    import spartautils

    
    
    for step in range(1,3):
        client = rpc_client
        
        client.call('WriteRegister',0x4,2) #CONFIG_OFFSET
        assert client.call('SetPeriodUs',20000) == 0
        
        tolerance = 6
        
        for mode in (1,0):

            s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
            s.connect((cmdopt, 9999))
    
            client.call('WriteRegister',0x74,mode) #TRIPLETS_EN_OFFSET 
            assert client.call('StartStreaming',1) == 0
            assert client.call('SendIO',1,1)       == 0

            
            assert spartautils.ProcesPacket(s,6,5,mode,0) == 0

            assert client.call('StopStreaming') == 0
            assert client.call('SendIO',1,1)    == 0
        
        s.close()

def test_process_dataX(rpc_client,cmdopt,num_of_tests):
    import time
    import socket
    import spartautils

    
    
    for step in range(1,num_of_tests):
        print("test_process_dataX " + str(step))
        client = rpc_client
        
        client.call('WriteRegister',0x4,2) #CONFIG_OFFSET
        assert client.call('SetPeriodUs',20000) == 0
        
        tolerance = 6
        
        mode =0

        s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
        s.connect((cmdopt, 9999))
    
        client.call('WriteRegister',0x74,mode) #TRIPLETS_EN_OFFSET
        assert client.call('StartStreaming',1) == 0
        assert client.call('SendIO',1,1)       == 0

            
        assert spartautils.ProcesPacket(s,6,1,0,0) == 0

        assert client.call('StopStreaming') == 0
        assert client.call('SendIO',1,1)    == 0
        
        s.close()




def test_regs(rpc_client,cmdopt):
    import time
    import socket
    import spartautils

    

    client = rpc_client

    assert client.call('SetPeriodUs',20000) == 0
    
    assert client.call('ReadRegister',0x1D0) == 10
    assert client.call('ReadRegister',0x1D4) == 200
    
    #s = socket.socket(
    #socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((cmdopt, 9999))

    p1 = client.call('ReadRegister',0x1D8) 
    time.sleep(0.01)
    p2 = client.call('ReadRegister',0x1D8) 
    assert p1==p2
    


    #assert client.call('StartStreaming',1) == 0
    #assert client.call('SendIO',1,1)        == -5
    #time.sleep(1)
    #p1 = client.call('ReadRegister',0x1D8) 
    #time.sleep(0.1)
    #p2 = client.call('ReadRegister',0x1D8) 
    #delta = abs(p1-p2 ) / client.call('ReadRegister',0x1D4) /1000
    #assert p1!=p2
    #assert abs(delta-100)< 3

    #assert client.call('StopStreaming') == 0
    assert client.call('SendIO',1,1)    == 0
    #s.close()



def Compare(client,sample):

    clockx = client.call('GetFPGAClock')
    
    regs=[]
    for i in range(0,6):
         reg =  client.call('ReadRegister',0x44+4*i)/clockx
         regs.append( int(reg) )  
    reg =  client.call('ReadRegister',0x5C)
    regs.append( int(reg) )  

    #print("expected", sample)
    #print("real",regs)
    return sample == regs


def test_modes(rpc_client):
    client = rpc_client

    period = 20000
    assert client.call('GetState')      == 0 
    assert client.call('SetPeriodUs',period)      == 0 


    stop = client.call('ReadRegister',python_regs.regs['LSR_END_OFFSET']) //client.call('GetFPGAClock')
    wakeup = client.call('ReadRegister',python_regs.regs['TD5_LEN_OFFSET']) //48
    print("IC Wakeup is ",wakeup)
    
    mask = 0xF0
    
    start =  client.call('ReadRegister',0xC)// client.call('GetFPGAClock')
    
    assert client.call('SendIO',0,mask)    == 0
    assert Compare(client, [start,stop,start,50+start,start,wakeup+start,3])

    assert client.call('SendIO',0x10,mask)    == 0
    assert Compare(client, [start,stop,start,50+start,start,wakeup+start,1])

    assert client.call('SendIO',0x20,mask)    == 0
    assert Compare(client, [start,stop,start,50+start,start,wakeup+start,2])

    assert client.call('SendIO',0x30,mask) == 0
    assert Compare(client, [start,start,start,start,start,start,3])

    assert client.call('SendIO',0x40,mask)    == 0
    assert Compare(client, [start,stop,start,stop,start,wakeup+start,3])

    assert client.call('SendIO',0x50,mask)    == 0
    assert Compare(client, [start,stop,start,stop,start,wakeup+start,1])

    assert client.call('SendIO',0x60,mask)    == 0
    assert Compare(client, [start,stop,start,stop,start,wakeup+start,2])

    assert client.call('SendIO',0x70,mask)    == 0
    assert Compare(client, [start,stop,start,stop,start,stop,3])

    assert client.call('SendIO',0x80,mask)    == 0
    assert Compare(client, [start,stop,start,50+start,start,stop,3])

    assert client.call('SendIO',0x90,mask)    == 0
    assert Compare(client, [start,stop,start,50+start,start,stop,1])

    assert client.call('SendIO',0xA0,mask)    == 0
    assert Compare(client, [start,stop,start,50+start,start,stop,2])




def test_sensor_protection(rpc_client,cmdopt):
    import time
    import socket
    import spartautils


    

    client = rpc_client


    client.call('ResetFPGA','register_file.txt')


    client.call('WriteRegister',0x4,2) #CONFIG_OFFSET
    assert client.call('SetPeriodUs',20000) == 0
        
    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cmdopt, 9999))
    
    assert client.call('StartStreaming',1) == 0
    
    #client.call('WriteRegister',python_regs.regs['SEN_PROTECT_LEN_OFFSET'],0) 
        
    for i in range(0,4):        
         (ph,td_data,fd_data,laser_data,lft_data) = spartautils.ReadPacket(s) 
         assert ph.status == 0
         assert ph.frame == i
         #assert ph.timestamp == i
    
    assert client.call('StopStreaming') == 0
    assert client.call('SendIO',1,1)        == 0

    s.close()


    client.call('ResetFPGA','register_file-sp.txt')

    #client.call('WriteRegister',python_regs.regs['SEN_PROTECT_LEN_OFFSET'],0x7080)  
    client.call('WriteRegister',python_regs.regs['TEST3_MAX_THRESHOLD_OFFSET'],0x0fffffff)  
    client.call('WriteRegister',python_regs.regs['TEST3_MIN_THRESHOLD_OFFSET'],0x0000)  
    client.call('WriteRegister',python_regs.regs['MUL_LSB_THRESHOLD_OFFSET'],0x0)  
    client.call('WriteRegister',python_regs.regs['MUL_MSB_THRESHOLD_OFFSET'],0x0)  


    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cmdopt, 9999))
    assert client.call('StartStreaming',1) == 0

    for i in range(0,4):        
         (ph,td_data,fd_data,laser_data,lft_data) = spartautils.ReadPacket(s) 
         assert ph.status == 1
         assert ph.frame == i
         #assert ph.timestamp == i

    
    assert client.call('StopStreaming') == 0
    assert client.call('SendIO',1,1)        == 0 
    s.close()


   # client.call('WriteRegister',python_regs.regs['SEN_PROTECT_LEN_OFFSET'],0x7080)  
    client.call('WriteRegister',python_regs.regs['TEST3_MAX_THRESHOLD_OFFSET'],0x0000)  
    client.call('WriteRegister',python_regs.regs['TEST3_MIN_THRESHOLD_OFFSET'],0x00003fff)  
    client.call('WriteRegister',python_regs.regs['MUL_LSB_THRESHOLD_OFFSET'],0xFFFFFFFF)  
    client.call('WriteRegister',python_regs.regs['MUL_MSB_THRESHOLD_OFFSET'],0xFF)  

    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cmdopt, 9999))
    assert client.call('StartStreaming',1) == 0

    for i in range(0,4):        
        (ph,td_data,fd_data,laser_data,lft_data) = spartautils.ReadPacket(s) 
        assert ph.status == 2
        assert ph.frame == 0
        #assert ph.timestamp == i

        
    
    assert client.call('StopStreaming') == 0
    assert client.call('SendIO',1,1)        == 0 
    s.close()
    time.sleep(1)
    #recovery
    client.call('ResetFPGA','register_file.txt')



def test_shift_register_api(rpc_client,cmdopt):
    client = rpc_client

    assert client.call('GetState')      == 0 
    assert client.call('SendIO',1,1)    == 0
    sr=''
    for i in range(0,64):
        sr = sr +chr(i)

    
    result = client.call('SendShiftRegister',sr)
    assert (result == 0 ) or (result == -3 )
            
    result = client.call('SendShiftRegisterEx',sr,0)
    assert (result == 0 ) or (result == -3 )
    
    result = client.call('SendShiftRegisterEx',sr,1)
    assert (result == 0 ) or (result == -3 )



#!
#
def test_trippleBufferSanity(rpc_client, cmdopt):
    import socket
    import spartautils

    client = rpc_client
    triplets_en = 1

    client.call('WriteRegister',0x4,2)
    assert client.call('SetPeriodUs',50000) == 0

    tolerance = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cmdopt, 9999))

    client.call('WriteRegister',0x74,triplets_en)
    assert client.call('StartStreaming',1)  == 0
    assert client.call('GetState')          == 2 # Streaming = 2

    assert spartautils.ProcesPacket(s,6,300,triplets_en, 0) == 0

    assert client.call('StopStreaming') == 0
    assert client.call('GetState')      == 0 # Ready=0

    s.close()


    
