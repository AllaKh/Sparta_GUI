import re,sys
regex = r"\#define\s+(\S+)\s+(0[xX][0-9a-fA-F]+)"


def validate(name):
    f = open(name,"r")
    list ={}

    print("regs={")
    for line in f:

        match = re.search(regex, line)
        if match == None:
            continue
        
        #list[match.group(1)] = int(match.group(3),16)
        key  = "'"+match.group(1)+"'"
        value = match.group(2)
        print (key,":",value,",")
    f.close()
    print("}")
    

if __name__ == "__main__":
   a = validate(sys.argv[1])
   exit(a)