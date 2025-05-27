import sys
import re

count=0
with open(sys.argv[1]) as fp:
    lines = fp.read().split("\n")
for line in lines:
    if line.startswith("Pix"):
        sp = line.split()
        f1 = float(sp[6])
        f2 = float(sp[10])
        if  abs(f1-f2) < float(sys.argv[2]):
            count=count-1
        count = count+1    
       # else:
       #     print( sp[1],sp[3])    

print("(comparevectors.py) Bad values {}".format(count))

# I am tolerant up to 15 errors
if count <=15 :
    count=0
exit( count)