
from __future__ import division
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import numpy as np
#import matplotlib
from numpy import arange, sin, pi
from gi.repository import GObject as go
from configparser import SafeConfigParser
from threading import Thread
import time,threading,sys
import socket
import spartautils,convert
import msgpackrpc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import struct
from matplotlib.widgets import TextBox
import os
#from python_regs import regs
from itertools import chain

def submit(text):
    print(text)



it_num=0
frame_count=0




Fs=12*1000
Ts = 1.0/Fs; # sampling interval
t = np.arange(0,Fs,Fs/(16*1024)) # time vector 
client = None
            


def CaptureFrames(s,n):
    #a_ph = []
    a_td_data = []
    a_fd_data = []

    for i in range(0,n):
        (ph, td_data, fd_data ,a,b) = spartautils.ReadPacket(s)
        a_td_data.append(td_data)
        a_fd_data.append(fd_data)

    return ph,a_td_data,a_fd_data



def GetBinMax(vec,win):

    
    return np.max( vec[   win[0]   : win[-1]+1])

def ProcesTestPacket(ph,a_td_data,a_fd_data,win1,win2,win3):

    vec300=[]
    map1 = np.zeros(300)
    map2 = np.zeros(300)
    map3 = np.zeros(300)

    area = list(chain( win1,win2,win3 ))
    
    for i in range(0,300):
        vec = np.zeros(ph.fft_out_len,dtype=int)
        vec300.append(vec)
    

    for i in range( 0,len(a_fd_data)):
        #print('z',len(a_fd_data[i]))
        fd_data= struct.unpack('B'* (len(a_fd_data[i])),a_fd_data[i] )
        #print( fd_data[16384-1]  )
        #sys.exit(0)
        #print(i)
        for j in range(0,300):
            #spartautils.GetFPGAPixel(pm,bin1)
            vec = spartautils.GetFFTVector(fd_data,j,ph,area)
            #print( "pixel ",j," ",np.max(vec))
            vec300[j] = np.add(vec300[j],vec)

    for i in range(0,300):
            #spartautils.GetFPGAPixel(pm,bin1)
        #    vec = spartautils.GetFFTVector(fd_data,i,ph)
         #   vec300[i] = vec300[i]+vec
        
        vec300[i] /= len(a_fd_data)
        #print(i,GetBinMax(vec300[i],win1 ),GetBinMax(vec300[i],win2 ),GetBinMax(vec300[i],win3 ) )
        map1[i] = GetBinMax(vec300[i],win1 )
        map2[i] = GetBinMax(vec300[i],win2 )
        map3[i] = GetBinMax(vec300[i],win3 )

        
    return (map1,map2,map3)



def rpc_client(host,root,f,f2,canvas,bin1,bin2,bin3,window,pm):


    
    global client
    #normal,protected = spartautils.ReadSR(sys.argv[2])


    
    #To be on safe side , stop streaming
    client.call('StopStreaming') 

    #Set Period to 800ms
    client.call('SetPeriodUs',50000) 
    


    #Connect data socket
    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 9999))

    #client.call('SendShiftRegisterEx', normal, 0)


    #client.call('SendShiftRegisterEx', protected, 1)

    
    client.call('SetSendNetDataMask',0x2) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)
    client.call('SetPixel',-1)
    
    #fpga_pix= spartautils.GetFPGAPixel(pm,start_pixel)
    #print(start_pixel,fpga_pix)

   

    #start streaming
    client.call('StartStreaming',1) 

        



    print("avg_num",avg_num)
    (ph,a_td_data,a_fd_data)=CaptureFrames(s,10+avg_num)
    #print("a_fd_data",len(a_fd_data))

    #Stop Streaming
    client.call('StopStreaming') 

    #Close socket
    s.close()
    
    
    maxf=int(12000*ph.fft_out_len/ph.fft_in_len*4)
    
    bin1 = fr2bin(bin1,maxf,ph.fft_out_len)
    bin2 = fr2bin(bin2,maxf,ph.fft_out_len)
    bin3 = fr2bin(bin3,maxf,ph.fft_out_len)
        
    
    win1 =  range( max(0,bin1-window),min(16384,bin1+window+1)  )
    win2 =  range( max(0,bin2-window),min(16384,bin2+window+1)  )
    win3 =  range( max(0,bin3-window),min(16384,bin3+window+1)  )
       

    (map1,map2,map3)=ProcesTestPacket(ph,a_td_data[10:10+avg_num],a_fd_data[10:10+avg_num],win1,win2,win3)

    global session
    fw = open("fft_bin_"+str(session)+".csv","w")

    


    data = np.zeros((10,30))

    
    
    
    for  j in range(0,10):
        for i in range(0,30):
            pixel = int(pm[j][i])
            #print(pixel)
            data[9-j][i]=  map1[pixel]

            fw.write("{},{},{},{}\n".format(j*30+i,int(map1[pixel]),int(map2[pixel]),int(map3[pixel])) )

    fw.close()
    session+=1

    #data[9][3]=65535

   #ax = f.add_subplot()

    f.clear()
    ax = f.add_subplot(111)
    im = ax.pcolormesh(data, cmap=cm.gray, edgecolors='white', linewidths=1,
                   antialiased=True)
    f.colorbar(im)

    ax.patch.set(hatch='xx', edgecolor='black')
    
    ax.set_yticks(range(0,10,1), minor=False)

    headers = ['9','8','7','6','5','4','3','2','1','0']
    ax.set_yticklabels(headers)
    canvas.draw()
    #ax.tick_params(axis='y',which='minor',bottom='on')
    #plt.show()    
    #Process data, 5 frames, pixel 269
    
    #plt.show()
    

    #ProcesTestPacket(ph, a_td_data,a_fd_data, numframes, 269)

    #plt.show()    
  
        

def destroy(e):
    sys.exit()

if __name__ == "__main__":

   
    pm =spartautils.ReadPixelMap(os.path.join(os.path.dirname(__file__),"pixel_map.csv"))
    #print(int(pm[0][0]))
    
    configname = os.path.join(os.path.expanduser("~"),'config2.ini')
    config = SafeConfigParser()
    config.read(configname)

    session=0

    
    # 12M - 16*1024
    # F/12M*16*1024


    
    
    global avg_num,fpga_ip, bin1,bin2,bin3,window

    bin1=int(config.get('main', 'bin1', fallback="12000")) 
    bin2=int(config.get('main', 'bin2', fallback="8000")) 
    bin3=int(config.get('main', 'bin3', fallback="6000")) 
    avg_num=int(config.get('main', 'avg', fallback="10"))
    window=int(config.get('main', 'window', fallback="2"))
    fpga_ip=config.get('main', 'host', fallback="10.99.10.100")

    
    
    win = Gtk.Window()
    win.set_title("Embedding in TK")
    win.set_direction(Gtk.TextDirection.LTR)

    
    def close(a,b):
        
        print("Start shutdown")
        if client:
            client.call('StopStreaming')
            client.call('SetSendNetDataMask',0x3) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)
            client.call('SetPixel',-1) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)

        config = SafeConfigParser()
        config.add_section('main')
        
        config.set('main','avg',entryavg.get_text())
        config.set('main','host',entryip.get_text())
        config.set('main','bin1',entrybin1.get_text())
        config.set('main','bin2',entrybin2.get_text())
        config.set('main','bin3',entrybin3.get_text())
        config.set('main','window',entrywindow.get_text())
        
        with open( configname, 'w') as configfile:
            config.write(configfile)
            configfile.close()
        
        print("mainly done")
        Gtk.main_quit(a,b)

    vbox = Gtk.VBox()
    win.add(vbox)
    win.connect("delete-event", close)
    win.set_default_size(1200, 600)

   # Add canvas to vbox
    f = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvas(f)  # a Gtk.DrawingArea
    vbox.pack_start(canvas, True, True, 0)

    
    def on_key_event(event):
        print('you pressed %s' % event.key)
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)


    


    
        

    
    grid = Gtk.Grid()
    grid.set_direction(Gtk.TextDirection.LTR)
    
    labelbin1 = Gtk.Label()
    labelbin1.set_text("bin1 in Khz")
    grid.attach(labelbin1,0,0,1,1)
    entrybin1 = Gtk.Entry()
    entrybin1.set_text(str(bin1))
    grid.attach(entrybin1,1,0,1,1)

    labelbin2 = Gtk.Label()
    labelbin2.set_text("bin2 in Khz")
    grid.attach(labelbin2,2,0,1,1)
    entrybin2 = Gtk.Entry()
    entrybin2.set_text(str(bin2))
    grid.attach(entrybin2,3,0,1,1)

    labelbin3 = Gtk.Label()
    labelbin3.set_text("bin3 in Khz")
    grid.attach(labelbin3,4,0,1,1)
    entrybin3 = Gtk.Entry()
    entrybin3.set_text(str(bin3))
    grid.attach(entrybin3,5,0,1,1)


    labelavg = Gtk.Label()
    labelavg.set_text("Avg num")
    grid.attach(labelavg,6,0,1,1)

    entryavg = Gtk.Entry()
    entryavg.set_text(str(avg_num))
    grid.attach(entryavg,7,0,1,1)

    labelwindow = Gtk.Label()
    labelwindow.set_text("Window")
    grid.attach(labelwindow,8,0,1,1)

    entrywindow = Gtk.Entry()
    entrywindow.set_text(str(window))
    grid.attach(entrywindow,9,0,1,1)

    


    labelip = Gtk.Label()
    labelip.set_text("FPGA IP")
    grid.attach(labelip,0,1,1,1)

    entryip = Gtk.Entry()
    entryip.set_text(fpga_ip)
    grid.attach(entryip,1,1,1,1)


   

    def fr2bin(fr,maxF,fft_out):
        return int(fr*fft_out/maxF)
    
    
    def connect(s):
        global client
        global avg_num,bin1,bin2,bin3,window
        bin1=int(entrybin1.get_text())
        bin2=int(entrybin2.get_text())
        bin3=int(entrybin3.get_text())
        window=int(entrywindow.get_text())


        
        avg_num=int(entryavg.get_text())

        #if client == None:
        client =  msgpackrpc.Client(msgpackrpc.Address(entryip.get_text(), 8080),timeout=120)


        

        
       
        rpc_client(entryip.get_text(),win,f,None,canvas,bin1,bin2,bin3,window,pm)
    
    buttonip = Gtk.Button.new_with_label("Capture")
    buttonip.connect("clicked", connect)
    grid.attach(buttonip, 2,1,1,1)

    

    
    

    vbox.pack_start(grid,False, False, 0)

    

    #plt.ion()
    
    #ax = f.add_subplot(111)
    #ax.set_ylim(0, 128*1024)
    #ax.set_xlim(0, 13000)

    
    #ax2 = f2.add_subplot(111)
    #ax2.set_xlim(0, 100000)
    #ax2.set_ylim(-5000,50000)


    win.show_all()
    Gtk.main()
    
    #rpc_client(sys.argv[1] )
    
    
