from assemble import ISA16bit

def check_errors(instr):
    x=ISA16bit()
    status=False             #Error status
    #Error a
    for i in x.opcode_table:
        if instr[0]==i:
            continue
        else:
            status=True
            print("Typos in instruction name or register name")
            break
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

#error g 
def invalid_var_dec(instr,var):
    if var==True:
        if instr[0]=="var":
            print("Variables not declared at the beginning")
    elif var==False:
        if instr[0]=="var":
            pass
    else:
        if instr[0]!="var":
            var=True
            return(var)

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