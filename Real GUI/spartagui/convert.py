
import sys
def GetSample(buf,t,pixel,option):
    index  = 128*24*(t//128) + 128*20 +  (t%128) + pixel*128 
   # print(index,len(buf))
    p0 = buf[ index*2 ]
    p1 = buf[ index*2 +1]
    if option == 1:
        
      p = p1*256 +p0
    else:  
        p = p1 +p0*256
    return p

def GetTDSample(buf,t,pixel):
    

    index = (t % 128) + (pixel // 15) * 128 + (t // 128)*(128 * 20 + 128 * 4) 
  
    p0 = buf[ index*2 ]
    p1 = buf[ index*2 +1]
    p = p1*256 +p0


    bitoffset = pixel % 15

    bit = 1 & (p >> bitoffset)
        
    
    return bit






def delta(p,start,t):
    
    tt= 0xFFFF & (start+t)
    p = p - tt
        
    return p#bin(p ^ tt).count("1")    

def ProcessTP(bytes,rng,opt_range,print_csv):
    
    #return    128*24*(time/128) + 128*20 +  (time%128) + pixel*128 ;,0

    print("qq",opt_range)
    for opt in opt_range:

       

        pd0=[]
        pd1=[]
        pd2=[]
        pd3=[]
        pd4=[]

        
        #rng = range(0,10)
        start = GetSample(bytes,0,1,opt)
        print( "Time,ch0-hex,ch0-dec,ch0-bin,ch1-hex,ch1-dec,ch1-bin,ch2-hex,ch2-dec,ch2-bin,ch3-hex,ch3-dec,ch3-bin,")
        for t in rng:
            
            p0 = GetSample(bytes,t,0,opt)
            p1 = GetSample(bytes,t,1,opt)
            p2 = GetSample(bytes,t,2,opt)
            p3 = GetSample(bytes,t,3,opt)

        # print(t,start,p0,p1,p2,p3)

            #p0 = delta(p0, start,t) 
            #p1 = delta(p1, start,t) 
            #p2 = delta(p2, start,t) 
            #p3 = delta(p3, start,t) 
            
        # print(t,start,p0,p1,p2,p3)

        # print(format(p0,'04x'),format(p1,'04x'),format(p2,'04x'),format(p3,'04x'))
            
            if print_csv:
                print( "{},{:04x},{:d},{:016b},{:04x},{:d},{:016b},{:04x},{:d},{:016b},{:04x},{:d},{:016b}".format(t,p0,p0,p0,p1,p1,p1,p2,p2,p2,p3,p3,p3))

            pd0.append(p0)
            pd1.append(p1)
            pd2.append(p2)
            pd3.append(p3)

            pd4.append( bin((p1 ^ start+t)).count("1"))
    
        #plt.figure()
        #plt.subplot(221)
        #plt.plot(rng,pd0,'.')
        #plt.subplot(222)
        #plt.plot(rng,pd1,'.')
    
        #plt.subplot(223)
        #plt.plot(rng,pd2,'.')
        #plt.subplot(224)
        #plt.plot(rng,pd3,'.')

        #print("opt",opt)

    #plt.show()
    return (pd0,pd1,pd2,pd3)

# def GetTDSample(buf,t,pixel):
#
#
#     index = (t % 128) + (pixel // 15) * 128 + (t // 128)*(128 * 20 + 128 * 4)
#
#     p0 = buf[ index*2 ]
#     p1 = buf[ index*2 +1]
#     p = p1*256 +p0
#
#
#     bitoffset = pixel % 15
#
#     bit = 1 & (p >> bitoffset)
#
#
#     return bit


if __name__ == "__main__":
    file = open(sys.argv[1], "rb")    
    bytes = file.read()    
    file.close()
    #time = 32*1024
    #blocks = time // 128

    #block_size = 128*2*24
    header_size = 12*4

    #ln = 32*1024*3*2+14*4

    rng = range(0,32*1024*2)
    ProcessTP(bytes[header_size:],rng,range(0,1),1)
    
