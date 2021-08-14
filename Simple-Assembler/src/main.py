import sys
import re
from assemble import ISA16bit

input = sys.stdin
hlt_count = 0

def check_inst(str):
    w = str.split(" ")
    if(w[0]=='mov'):
        if(len(w)==3):
                if(w[2] in ['r0','r1','r2','r3','r4','r5','r6','FLAGS']):
                    type=IS.opcode_table[w[0]][1][2]
                elif(w[2][0]=='$'):
                    type=IS.opcode_table[w[0]][0][2]
    else:
        type = IS.opcode_table[w[0]][2]
    if(IS.type_check(str,type)):
        IS.execute(str)
        print(IS.binary(str,type))
        return(True)
    return(False)


def check_line(line):
    line = re.sub(r'(\\[a-zA-Z])+'," ",line)
    w = line.split(" ")
    if(re.match("[a-zA-z]+: ([a-zA-Z0-9]+ )+",line)):
        if(not check_inst(" ".join(w[1:]))):
            print(" Error \n")
        else:
            if(w[1]!="cmp" and w[1] in IS.opcode_table):
                IS.registers["FLAGS"] = '0000000000000000'
            return(1)
    elif(re.match("\Avar [a-zA-Z]+",line)):
        return(3)
    elif(w[0] in IS.opcode_table):
        if(not check_inst(line)):
            print(" Error \n")
        else:
            if(w[0]!="cmp"):
                IS.registers["FLAGS"] = '0000000000000000'
            return(2)
    else:
        return (4)

def main():
    for lines in input:
        for line in lines.split("\n"):
            line_type = check_line(line)
            if(line_type!=4):
                print(line+" ", line_type)

if __name__ == "__main__":
    IS = ISA16bit()
    IS.__init__()
    main()