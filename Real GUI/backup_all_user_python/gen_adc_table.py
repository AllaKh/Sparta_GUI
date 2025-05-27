def GetBit(val,bit):
    ret = 1&(val >>bit)
   
    return 1&(val >>bit)


print("{")
for i in range(0,256):
    
    n = (i & 0xF)<<4
    #print(n)
    b0 = GetBit(i,5)#<<0
    b1 = GetBit(i,7)<<1
    b2= GetBit(i,6)<<2
    b3= GetBit(i,4)<<3

   
    n = n +  b0 + b1 + b2 + b3
   
    print("0x{:02x},".format(n),end='')
    if i %16 == 0:
        print(" ")
print("}")