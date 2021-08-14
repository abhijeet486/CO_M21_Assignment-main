from assemble import ISA16bit

def check_errors(instr):
    x=ISA16bit()
    status=False             #Error status
    #Error a
    if instr[0] not in x.opcode_table:
        status=True
        print("Typos in instruction name or register name")
    #Error b    
    #Error c
    #Error d
    #Error e
    if instr[0]=="mov":
        for i in x.opcode_table("mov"):
            if i(-1)==True:
                if instr[-1]>=1 and instr[-1]<=255:
                    continue
                else:
                    print("Illegal Immediate values")
                    break
    else:
        for i in x.opcode_table:
            if instr[0]==i:
                if x.opcode_table[i][-1]==True:
                    if instr[-1]>=1 and instr[-1]<=255:
                        continue
                    else:
                        print("Illegal Immediate values")
                        break
    #Error f

def check_inst(str,IS,pc,temp_var):
    w = str.split(" ")
    if(w[0]=='mov'):
        if(len(w)==3):
                if(w[2] in ['R0','R1','R2','R3','R4','R5','R6','FLAGS']):
                    type=IS.opcode_table[w[0]][1][2]
                elif(w[2][0]=='$'):
                    type=IS.opcode_table[w[0]][0][2]
    else:
        type = IS.opcode_table[w[0]][2]
    if(IS.type_check(str,type)):
        return(True)
    print("Error: Wrong syntax used for instructions , line",pc-temp_var)
    return(False)

def is_valid_var_dec(w,labels,pc,count_var):
    flag = True
    if(w[1] in labels):
        print("Error: Misuse of labels as variables, line",pc-count_var)
        flag = False
    if(pc>count_var):
        print("Error: Variables not declared at the beginning , line",pc-count_var)
        flag = False
    return(flag)


#error h
def hlt_missing(instr,var):
    if var>1:
        print("hlt not being used as the last instruction/More than one hlt")
        return(0)
    elif var==0:
        if instr=="hlt":
            var+=1
            return(var)
        else:
            return(0)
    elif var>1:

        pass
    else:
        pass