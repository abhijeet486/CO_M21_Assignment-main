import sys
import re
from assemble import ISA16bit

input = sys.stdin

def type_check(str,t):
    content = str.split(" ")
    if(t=="A"):
        if(content[1] in ["r0","r1","r2","r3","r4","r5","r6"] and (content[2] in ["r0","r1","r2","r3","r4","r5","r6"]) and (content[3] in ["r0","r1","r2","r3","r4","r5","r6"])):
            return(True)
        return(False)
    elif(t=="B"):
        if(len(content)==3 and content[1] in ["r0","r1","r2","r3","r4","r5","r6"]):
            try:
                if(content[2][0]=="$" and ("-" not in content[2]) and int(content[2][1:])>=0):
                    return(True)
            except:
                return(False)
        return(False)
    elif(t=="C"):
        if(len(content)==3):
            if(content[1] in ["r0","r1","r2","r3","r4","r5","r6"] and content[2] in ["r0","r1","r2","r3","r4","r5","r6"]):
                return(True)
        return(False)
    elif(t=="D"):
        if(len(content)==3):
            if(content[1] in ["r0","r1","r2","r3","r4","r5","r6"] and content[2]):
                return(True)
        return(False)
    elif(t=="E"):
        if(len(content)==2 and content[1]):
            return(True)
        return(False)
    elif(t=="F"):
        return(str=="hlt")

def check_inst(str):
    w = str.split(" ")
    type = IS.opcode_table[w[0]][2]
    return(IS.type_check(str,type))


def check_line(line):
    line = re.sub(r'(\\[a-zA-Z])+'," ",line)
    w = line.split(" ")
    if(re.match("[a-zA-z]+: ",line)):
        check_inst(" ".join(w[1:]))
    elif(re.match("\Avar [a-zA-Z]+",line)):
        return(3)
    elif(w[0] in IS.opcode_table):
        if(not check_inst(line)):
            print(" Error \n")
        else:
            return(2)
    else:
        return(4)

def main():
    for lines in input:
        for line in lines.split("\n"):
            line_type = check_line(line)
            if(line_type!=4):
                print(line+" ", line_type)
            #for read in line.split(" "):
             #   ISA.__init__()
              #  ISA.type_check(read)

if __name__ == "__main__":
    IS = ISA16bit()
    IS.__init__()
    main()