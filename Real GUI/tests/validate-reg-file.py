import re,sys
regex = r"(\S*)\s*(0x[0-9a-fA-F]+)\s*(0x[0-9a-fA-F]+)[\s\n$]"


def validate(name):
    f = open(name,"r")
    list ={}
    for line in f:
        if line[0] == '/' :
            #print("Skip",line)
            continue
        match = re.search(regex, line)
        if match == None:
            continue
        
        list[match.group(1)] = int(match.group(3),16)
        #print (match.group(1),match.group(2),match.group(1))
    f.close()

    td1 = list["TD1_LEN"]
    td4 = list["TD4_LEN"]
    td5 = list["TD5_LEN"]
    td6 = list["TD6_LEN"]
    td7 = list["TD7_LEN"]

    sensor_prot_len = list["SEN_PROTECT_LEN_OFFSET"]

    expected_td = 65536 + td5+td6 +td7
    if sensor_prot_len != 0:
        expected_td= expected_td +sensor_prot_len + td5

    print ( "expected_td1",hex(expected_td),"Current td1",hex(td1),["Error","OK"][td1==expected_td])
    return [1,0][td1==expected_td]
    

if __name__ == "__main__":
   a = validate(sys.argv[1])
   exit(a)