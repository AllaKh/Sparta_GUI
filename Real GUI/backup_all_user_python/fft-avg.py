
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

from gi.repository import GObject as go
from configparser import SafeConfigParser
import sys
import socket
import spartautils
import msgpackrpc
import matplotlib.pyplot as plt
import struct
import os
#from python_regs import regs


def submit(text):
    print(text)



it_num=0
frame_count=0




client = None
            

def CaptureFrame(s,client,root,ax,ax2,canvas,canvas2,i,points,points2,figure,figure2,vec):
   

   

    global it_num
    global frame_count

    
    

    (ph, td_data, fd_data ,a,b) = spartautils.ReadPacket(s)
    #print (len(td_data),i)
    
    t2 = np.arange(0,len(td_data))
    
    if vec is None:
        vec = np.zeros(len(fd_data)//2, dtype=float)

    count = len(fd_data)//2
    samples = struct.unpack('H'*count, fd_data)

    vec =np.add(vec,samples)

    td_samples = struct.unpack('B'*len(td_data), td_data)
    vec2 = np.zeros(len(td_data), dtype=float)
    sum=0.0
    for i in t2:
        sum+=td_samples[i]-0.5
        vec2[i] = sum
    
    #print(frame_count,avg_num)
    Fs=12*1000*ph.fft_out_len/(ph.fft_in_len)*4
    Fs=int(Fs)
    print("Fs",Fs,ph.fft_in_len)
    t = np.arange(0,Fs,Fs/(ph.fft_out_len)) # time vector 

    frame_count+=1
    if points == None:
        points, = ax.plot(t[:len(vec)],vec )
        points2, = ax2.plot(t2,vec2 )

        


    else:
    
        points2.set_data(t2,vec2)

        if frame_count >= avg_num:

            
            vec  /= (frame_count)

            
            
            print(it_num,avg_num)   
            points.set_data(t[:len(vec)],vec)
            
            
            ax.set_xlabel(str(i%300))

            vec = np.zeros(len(fd_data)//2, dtype=float)
            frame_count=0    
            it_num+=1
            #client.call('SetPixel',it_num%300)        

        
    
    canvas.draw()
    canvas2.draw()
   
    #toolbar = figure.canvas.toolbar #Get the toolbar handler
    #toolbar.update() #Update the toolbar memory
    #plt.show(block = False) #Show changes
    go.idle_add(CaptureFrame,s,client,root,ax,ax2,canvas,canvas2,10,points,points2,figure,figure2,vec)


def rpc_client(host,root,f,f2,canvas,canvas2,ax,ax2):


    
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

    
    client.call('SetSendNetDataMask',0x3) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)
    fpga_pix= spartautils.GetFPGAPixel(pm,start_pixel)
    print(start_pixel,fpga_pix)

    client.call('SetPixel',fpga_pix) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)

    #start streaming
    client.call('StartStreaming',1) 

    numframes =50000
    
    go.idle_add(   CaptureFrame,s,client,root,ax,ax2,canvas,canvas2,0,None,None,f,f2,None)

    #Stop Streaming
    #client.call('StopStreaming') == 0

    #Close socket
    #s.close()

    #Process data, 5 frames, pixel 269
    
    #plt.show()
    

    #ProcesTestPacket(ph, a_td_data,a_fd_data, numframes, 269)

    #plt.show()    
  
        



def destroy(e):
    sys.exit()

if __name__ == "__main__":

   
    pm =spartautils.ReadPixelMap(os.path.join(os.path.dirname(__file__),"pixel_map.csv"))
    #print(int(pm[0][0]))
    
    configname = os.path.join(os.path.expanduser("~"),'config.ini')
    config = SafeConfigParser()
    config.read(configname)

    

    
    
    global start_pixel,avg_num,fpga_ip, gen_start, gen_end

    start_pixel=int(config.get('main', 'pixel', fallback="200")) 
    avg_num=int(config.get('main', 'avg', fallback="10"))
    fpga_ip=config.get('main', 'host', fallback="10.99.10.100")

    
    gen_start = 0
    gen_end = 200* 2000

    win = Gtk.Window()
    win.set_title("Embedding in TK")
    win.set_direction(Gtk.TextDirection.LTR)

    plt.ion()
    f = Figure(figsize=(5, 4), dpi=100)
    f2 = Figure(figsize=(5, 4), dpi=100)


    #a = f.add_subplot(1, 1, 1)
    #t = np.arange(0.0, 3.0, 0.01)
    #s = np.sin(2*np.pi*t)
    #a.plot(t, s)
    
    def close(a,b):
        
        print("Start shutdown")
        if client:
            client.call('StopStreaming')
            client.call('SetSendNetDataMask',0x3) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)
            client.call('SetPixel',-1) # ==1000 => (msb) 1(FLATTENING), 0(LD), 0(FD), (0)TD (lsb)

        config = SafeConfigParser()
        config.add_section('main')
        config.set('main','pixel',entrypixel.get_text())
        config.set('main','avg',entryavg.get_text())
        config.set('main','host',entryip.get_text())
        
        with open( configname, 'w') as configfile:
            config.write(configfile)
            configfile.close()
        
        print("manly done")
        Gtk.main_quit(a,b)

    vbox = Gtk.VBox()
    win.add(vbox)
    win.connect("delete-event", close)
    win.set_default_size(1200, 600)

   # Add canvas to vbox
    canvas = FigureCanvas(f)  # a Gtk.DrawingArea
    vbox.pack_start(canvas, True, True, 0)

    

    # Create toolbar
    toolbar = NavigationToolbar(canvas, win)
    toolbar.set_direction(Gtk.TextDirection.LTR)
    vbox.pack_start(toolbar, False, False, 0)

    canvas2 = FigureCanvas(f2)  # a Gtk.DrawingArea
    vbox.pack_start(canvas2, True, True, 0)

    
    toolbar2 = NavigationToolbar(canvas2, win)
    toolbar2.set_direction(Gtk.TextDirection.LTR)
    vbox.pack_start(toolbar2, False, False, 0)

    
    
    def on_key_event(event):
        print('you pressed %s' % event.key)
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)


    


    def retrieve_input(s):
        global avg_num
        inputValue=int(entrypixel.get_text())
        
        
        fpga_pix= spartautils.GetFPGAPixel(pm,inputValue)
        print(inputValue,fpga_pix)

        client.call('SetPixel',fpga_pix)
        inputValue=entryavg.get_text()
        print(inputValue)
        avg_num=int(inputValue)

        #client.call('WriteRegister',regs['GEN_START_OFFSET'],int(entrystart.get_text()))
        #client.call('WriteRegister',regs['GEN_END_OFFSET'],int(entryend.get_text()))


    
    grid = Gtk.Grid()
    grid.set_direction(Gtk.TextDirection.LTR)
    
    label = Gtk.Label()
    label.set_text("Pixel")
    grid.attach(label,0,0,1,1)

    entrypixel = Gtk.Entry()
    entrypixel.set_text(str(start_pixel))
    grid.attach(entrypixel,1,0,1,1)

    labelavg = Gtk.Label()
    labelavg.set_text("Avg num")
    grid.attach(labelavg,2,0,1,1)

    entryavg = Gtk.Entry()
    entryavg.set_text(str(avg_num))
    grid.attach(entryavg,3,0,1,1)


    buttonset = Gtk.Button.new_with_label("Set")
    buttonset.connect("clicked", retrieve_input)
    grid.attach(buttonset, 4,0,1,1)


    labelip = Gtk.Label()
    labelip.set_text("FPGA IP")
    grid.attach(labelip,0,2,1,1)

    entryip = Gtk.Entry()
    entryip.set_text(fpga_ip)
    grid.attach(entryip,1,2,1,1)


   # labelstart = Gtk.Label()
   # labelstart.set_text("Gen tart")
   # grid.attach(labelstart,0,3,1,1)

   # entrystart = Gtk.Entry()
   # entrystart.set_text(str(gen_start))
   # grid.attach(entrystart,1,3,1,1)

   # labelend = Gtk.Label()
   # labelend.set_text("Gen Len")
   # grid.attach(labelend,0,4,1,1)

   # entryend = Gtk.Entry()
   # entryend.set_text(str(gen_end))
  #  grid.attach(entryend,1,4,1,1)


    
    
    def connect(s):
        global client
        if client == None:
            client =  msgpackrpc.Client(msgpackrpc.Address(entryip.get_text(), 8080),timeout=120)
            rpc_client(entryip.get_text(),win,f,f2,canvas,canvas2,ax,ax2)
    
    buttonip = Gtk.Button.new_with_label("Connect")
    buttonip.connect("clicked", connect)
    grid.attach(buttonip, 2,2,1,1)

    

    
    

    vbox.pack_start(grid,False, False, 0)

    

    #plt.ion()
    
    ax = f.add_subplot(111)
    ax.set_ylim(0, 128*1024)
    ax.set_xlim(0, 13000)

    
    ax2 = f2.add_subplot(111)
    ax2.set_xlim(0, 100000)
    ax2.set_ylim(-5000,50000)


    win.show_all()
    Gtk.main()
    
    #rpc_client(sys.argv[1] )
    
    
