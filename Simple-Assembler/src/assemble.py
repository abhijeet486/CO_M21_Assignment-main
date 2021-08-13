nonmem = 0
mem = 1


class ISA16bit:
    def __init__(self):
        self.opcode_table = { # inst : (opcode,type of instruction,number of operands, number of registers, immx)
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
        self.registers={
            'r1' : '0000000000000000',
            'r2' : '0000000000000000',
            'r3' : '0000000000000000',
            'r4' : '0000000000000000',
            'r5' : '0000000000000000',
            'r6' : '0000000000000000',
            'FLAGS' :'0000000000000000'
            }
        self.registers_address = {
            'r1' : '000', 
            'r2' : '001',
            'r3' : '010',
            'r4' : '011',
            'r5' : '100',
            'r6' : '101',
            'FLAGS' : '110'
            }
        self.type = {
            'A': {"o":5, "u":2, "r1":3, "r":3, "r3":3},
            'B': {"o":5, "r1":3, "imm":8},
            'C': {"o":5, "u":5, "r1":3,"r2":3},
            'D': {"o":5, "r1":3 ,"mem":8},
            'E': {"o":5, "u":3, "mem":8},
            'F': {"o":5,"u":11}
        }

    def update_register(self,r,value):
        self.registers[r] = value

    def type_check(self,str,t):
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
