import sys
import re
from assemble import ISA16bit
import check_error

input = sys.stdin

#//////////////////////

def instr_limit(lines,temp_var):
    for i in lines.split("\n"):
        temp_var+=1
        if temp_var<=256:
            continue
        else:
            print("No of Instructions exceed ISA limit")

def variables(var_name,add_line,var_dict):
    var_dict[var_name]=bin(add_line)    

def convertion(instr,temp_var):
    variables={}
    if (instr.split()[0])=="var":
        variables(instr[1])
        temp_var+=1


#/////////////////

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
        IS.execute(str,type)
        return(True)
    return(False)

# add\tr1 r2 r3 -> add r1 r2 r3

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
    else: # " " or ""
        return (4)

def main():
    var_decl_done=False
    hlt_count = 0
    for lines in input:
        for line in lines.split("\n"):
            var_decl_done=check_error.invalid_var_dec(line,var_decl_done)
            hlt_count = 0
            line_type = check_line(line)
            if(line_type!=4):
                print(line+" ", line_type)    
            IS.registers["FLAGS"] = '0000000000000000'
            #for read in line.split(" "):
             #   ISA.__init__()
              #  ISA.type_check(read)

    
if __name__ == "__main__":
    IS = ISA16bit()
    IS.__init__()
    main()