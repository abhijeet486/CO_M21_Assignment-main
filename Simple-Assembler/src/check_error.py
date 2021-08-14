from assemble import ISA16bit

def check_errors(instr,status):  #Error status
    x=ISA16bit()       
    #Error a
    for i in x.opcode_table:
        if instr[0]==i:
            return(False)
        else:
            status=True
            print("Typos in instruction name or register name")
            return("exit")
    #Error b    
    #Error c
    #Error d
    #Error e
    if instr[0]=="mov":
        for i in x.opcode_table("mov"):
            if i(-1)==True:
                if instr[-1]>=1 and instr[-1]<=255:
                    return(False)
                else:
                    print("Illegal Immediate values")
                    return("exit")
    else:
        for i in x.opcode_table:
            if instr[0]==i:
                if x.opcode_table[i][-1]==True:
                    if instr[-1]>=1 and instr[-1]<=255:
                        return(False)
                    else:
                        print("Illegal Immediate values")
                        return("exit")

#Error f
#error g 
def invalid_var_dec(instr,var):
    if var==True:
        if instr[0]=="var":
            print("Variables not declared at the beginning")
            return("exit")
    elif var==False:
        if instr[0]=="var":
            return(False)
    else:
        if instr[0]!="var":
            return(True)

#error h
def hlt_missing(instr,hlt_count):
    if hlt_count>1:
        print("hlt not being used as the last instruction/More than one hlt")
        return("exit")
    if hlt_count==0:
        if instr=="hlt":
            hlt_count+=1
            return(hlt_count)
        else:
            return(hlt_count)
    #if hlt_count==1:
        hlt_count+=1
        return(hlt_count) #Needs correction