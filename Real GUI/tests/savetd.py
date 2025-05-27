import msgpackrpc
import sys,time
import socket
import spartautils
import convert

def init(host):
    
    print("Connect to",host)
    client =  msgpackrpc.Client(msgpackrpc.Address(host, 8080))
    client.call('StopStreaming')
    return client


def save_td(host):
    
    client = init(host)
    state = client.call('GetState')    
    print("State", state)

    
    client.call('StartStreamingSingle',1)

    
    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 9999))
    (ph,td_data,fd_data) = spartautils.ReadPacket(s)
    client.call('StopStreaming')
    

    #last = convert.GetSample(td_data,1024*3*32-1,1,0)
    #print("Last {:x}".format(last))
    

    file = open('td.bin', 'wb')
    file.write(ph)
    file.write(td_data)
    file.write(fd_data)
    file.close()


    


if __name__ == "__main__":
   save_td(sys.argv[1])