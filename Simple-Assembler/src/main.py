import sys
import re

mem = 1
nonmem = 0
opcode_table = { # inst : (opcode,type of instruction,number of operands, number of registers, immx)
            "add": ('00000',nonmem,'A',2,3,False),
            "sub": ('00001',nonmem,'A',2,3,False),
            "mov": ('00010',nonmem,'B',2,1,True),
            "mov": ('00011',nonmem,'C',2,2,False),
            "ld": ('00100',mem,'D',2,1,False),
            "st": ('00101',mem,'D',2,1,False),
            "mul": ('00110',nonmem,'A',2,3,False),
            "div": ('00111',nonmem,'C',2,2,False),
            "rs": ('01000',nonmem,'B',2,1,True),
            "ls": ('01001',nonmem,'B',2,1,True),
            "xor": ('01010',nonmem,'A',2,3,False),
            "or": ('01011',nonmem,'A',2,3,False),
            "and": ('01100',nonmem,'A',2,3,False),
            "not": ('01101',nonmem,'C',1,2,False),
            "cmp": ('01110',nonmem,'C',2,2,False),
            "jmp": ('01111',mem,'E',1,0,True),
            "jlt": ('10000',mem,'E',1,0,True),
            "jgt": ('10001',mem,'E',1,0,True),
            "jeq": ('10010',mem,'E',1,0,True),
            "hlt": ('10011',nonmem,'F',0,0,False)
        }

input = sys.stdin

def type_check(str,t):
    content = str.split(" ")
    if(t=="A"):
        if(len(set(content[1:]))<3):
            return(False)
        if(content[1] in ["r0","r1","r2","r3","r4","r5","r6"] and (content[2] in ["r0","r1","r2","r3","r4","r5","r6"]) and (content[3] in ["r0","r1","r2","r3","r4","r5","r6"])):
            return(True)
        else:
            return(False)
    elif(t=="F"):
        return(str=="hlt")

def check_inst(str):
    w = str.split(" ")
    type = opcode_table[w[0]][2]
    return(type_check(str,type))


def check_line(line):
    line = re.sub(r'(\\[a-zA-Z])+'," ",line)
    w = line.split(" ")
    if(re.match("[a-zA-z]+: ",line)):
        check_inst(" ".join(w[1:]))
    elif(re.match("\Avar [a-zA-Z]+",line)):
        return(3)
    elif(w[0] in opcode_table):
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
    main()