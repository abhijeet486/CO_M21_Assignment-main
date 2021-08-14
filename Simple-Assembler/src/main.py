import sys
import re
from assemble import ISA16bit
import check_error

#input = sys.stdin

input = open(r"automatedTesting/tests/assembly/hardBin/test1","r")

var_dict = {}
labels = {}
hlt_count = 0
count_var = 0
pc = 0
inst_count = 0
temp_var = 0

#//////////////////////

def instr_limit():
    global inst_count,temp_var
    for lines in input.readlines():
        for i in lines.split("\n")[:-1]:
            if(i[:4]!="var "):
                inst_count+=1
            temp_var+=1
            if temp_var>256:
                print("No of Instructions exceed ISA limit")
                exit()

def variables(var):
    global count_var,var_dict
    count_var +=1
    var_dict[var[1]] = [inst_count + count_var,'0000000000000000']

def convertion(instr,count_var):
    variables={}
    if (instr.split()[0])=="var":
        variables(instr[1])
        count_var+=1


#/////////////////

def check_inst(str):
    global var_dict,hlt_count
    w = str.split(" ")
    if(w[0]=='mov'):
        if(len(w)==3):
                if(w[2] in ['R0','R1','R2','R3','R4','R5','R6','FLAGS']):
                    type=IS.opcode_table[w[0]][1][2]
                elif(w[2][0]=='$'):
                    type=IS.opcode_table[w[0]][0][2]
    else:
        type = IS.opcode_table[w[0]][2]
    if(IS.type_check(str,type,var_dict)):
        if(w[0]=="hlt" and hlt_count!=0):
            print("Error: hlt not being used as the last instruction ,line ",pc-count_var )
            return(False)
        var_dict = IS.execute(str,var_dict)
        print(IS.binary(str,type,var_dict))
        return(True)
    print("Error: Wrong syntax used for instructions , line",pc-count_var)
    return(False)


def check_line(line):
    line = re.sub(r'(\\[a-zA-Z])+'," ",line)
    w = line.split(" ")
    if(re.match("[a-zA-z]+: ([a-zA-Z0-9]+ )+",line)):
        if(not check_inst(" ".join(w[1:]))):
            print("Error : Typos in instruction name or register name , line",pc-count_var)
            return(4)
        else:
            labels[w[0][:-1]]=pc
            if(w[1]!="cmp" and w[1] in IS.opcode_table):
                IS.registers["FLAGS"] = '0000000000000000'
            return(1)
    elif(re.match("\Avar [a-zA-Z0-9_]*$",line)):
        if(check_error.is_valid_var_dec(w,labels,pc,count_var)):
            variables(w)
            return(3)
        else:
            return(4)
    elif(w[0] in IS.opcode_table):
        if(not check_inst(line)):
            print("Error : Typos in instruction name or register name , line",pc-count_var)
            return(4)
        else:
            if(w[0]!="cmp"):
                IS.registers["FLAGS"] = '0000000000000000'
            return(2)
    else:
        return (4)

def main():
    global pc
    instr_limit()
    input.seek(0)
    while(True):
            #var_decl_done = check_error.invalid_var_dec(line,var_decl_done)
            #hlt_count = 0
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