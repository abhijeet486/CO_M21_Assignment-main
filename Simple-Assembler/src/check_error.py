from assemble import ISA16bit


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
