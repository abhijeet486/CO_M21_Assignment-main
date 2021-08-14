import sys
import re
from assemble import ISA16bit
import check_error

input = sys.stdin

#input = open(r"Simple-Assembler/tests/error_test1","r")

var_dict = {}
labels = {}
hlt_count = 0
count_var = 0
pc = 0
inst_count = 0
temp_var = 0

#//////////////////////

def instr_limit():
    global inst_count,temp_var,labels
    for lines in input.readlines():
        for i in lines.split("\n"):
            i = re.sub(r'(\\[a-zA-Z])+'," ",i)
            if(i!=""):
                w = i.split(" ")
                if(w[0]!="var"):
                    inst_count+=1
                temp_var+=1
                if(temp_var>256):
                    print("Error : No of Instructions exceed ISA limit")
                    exit()
                if(i=="hlt" and hlt_count==1):
                    print("Error: hlt not being used as the last instruction , line",inst_count)
                    return(False)
                if(re.match(r"[a-zA-z0-9_]+: ([a-zA-Z0-9]+[ ]*)+",i)):
                    if(not check_inst(" ".join(w[1:]))):
                        print("Error : Typos in instruction name or register name , line",inst_count)
                        return(False)
                    else:
                        if(w[0][:-1] in  var_dict):
                            print("Error: Misuse of variables as labels, line",inst_count)
                            return(False)
                        else:
                            labels[w[0][:-1]] = inst_count - 1
                elif(re.match("\Avar ([a-zA-Z_]+)([0-9]*)$",i)):
                    if(check_error.is_valid_var_dec(w,labels,temp_var,temp_var-inst_count)):
                        var_dict[w[1]] = []
                elif(w[0] in IS.opcode_table):
                    if(not check_inst(i)):
                        print("Error : Typos in instruction name or register name , line",inst_count)
                        return(False)
                else:
                    print("Error : General Syntax Error, line",inst_count)
    if(hlt_count==0):
        print("Error : Missing hlt instruction")
        return(False)
    return(True)

def variable(var):
    global count_var,var_dict
    count_var +=1
    var_dict[var[1]] = [inst_count + count_var -1,'0000000000000000']


#/////////////////

def gettype(w):
    if(w[0]=='mov'):
        if(len(w)==3):
                if(w[2] in ['R0','R1','R2','R3','R4','R5','R6','FLAGS']):
                    type=IS.opcode_table[w[0]][1][2]
                elif(w[2][0]=='$'):
                    type=IS.opcode_table[w[0]][0][2]
    else:
        type = IS.opcode_table[w[0]][2]
    return(type)

def check_inst(str):
    global var_dict,hlt_count
    w = str.split(" ")
    type = gettype(w)
    if(IS.type_check(str,type,var_dict)):
        if(w[0]=="hlt"):
            hlt_count+=1
            return(hlt_count==1)
        return(True)
    print("Error: Wrong syntax used for instructions , line",pc-count_var)
    return(False)


def check_line(line):
    line = re.sub(r'(\\[a-zA-Z])+'," ",line)
    w = line.split(" ")
    if(re.match("[a-zA-z0-9_]+: ([a-zA-Z0-9]+[ ]*)+",line)):
        type = gettype(w[1:])
        print(IS.binary(" ".join(w[1:]),type,var_dict,labels))
        labels[w[0][:-1]] = pc - count_var - 1
        if(w[1]!="cmp" and w[1] in IS.opcode_table):
            IS.registers["FLAGS"] = '0000000000000000'
        return(1)
    elif(re.match("\Avar [a-zA-Z0-9_]*$",line)):
        variable(w)
        return(3)
    elif(w[0] in IS.opcode_table):
        type = gettype(w)
        print(IS.binary(line,type,var_dict,labels))
        if(w[0]!="cmp"):
            IS.registers["FLAGS"] = '0000000000000000'
        return(2)
    else:
        return (4)

def main():
    global pc
    flag = instr_limit()
    input.seek(0)
    while(flag):
            line = input.readline()
            line = line.split("\n")[0]
            if(line==""):break
            pc+=1
            line_type = check_line(line)
    input.close()

    
if __name__ == "__main__":
    IS = ISA16bit()
    IS.__init__()
    main()