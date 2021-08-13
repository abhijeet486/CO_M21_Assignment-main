

nonmem = 0
mem = 1


class ISA16bit:
    def __init__(self):
        self.opcode_table = { # inst : (opcode,type of instruction,number of operands, number of registers, immx)
            "add": ('00000',nonmem,'A',2,3,False),
            "sub": ('00001',nonmem,'A',2,3,False),
            "mov": [('00010',nonmem,'B',2,1,True),('00011',nonmem,'C',2,2,False)],
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
            'r0' : '0000000000000000',
            'r1' : '0000000000000000',
            'r2' : '0000000000000000',
            'r3' : '0000000000000000',
            'r4' : '0000000000000000',
            'r5' : '0000000000000000',
            'r6' : '0000000000000000',
            'FLAGS' :'0000000000000000'
            }
        self.registers_address = {
            'r0' : '000', 
            'r1' : '001',
            'r2' : '010',
            'r3' : '011',
            'r4' : '100',
            'r5' : '101',
            'r6' : '110',
            'FLAGS' : '111'
            }
        self.type = {
            'A': {"o":1, "u":2, "r1":1, "r2":1, "r3":1, "imm":0, "mem":0},
            'B': {"o":1, "u":0, "r1":1, "r2":0, "r3":0, "imm":8, "mem":0},
            'C': {"o":1, "u":5, "r1":1, "r2":1, "r3":0, "imm":0, "mem":0},
            'D': {"o":1, "u":0, "r1":1, "r2":0, "r3":0, "imm":0, "mem":8},
            'E': {"o":1, "u":3, "r1":0, "r2":0, "r3":0, "imm":0, "mem":8},
            'F': {"o":1,"u":11, "r1":0, "r2":0, "r3":0, "imm":0, "mem":0}
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
    def execute(self,str,type):
        w = str.split(" ")
        execute_table={
            "00000":"self.registers[w[1]]=int(self.registers[w[2]]) + int(self.registers[w[3]])",
            "00001":"if (self.registers[w[2]]>self.registers[w[3]]): self.registers[w[1]] =int(self.registers[w[2]])- int(self.registers[w[3]]) \nelse: self.registers['FLAGS']='0000000000001000'",
            "00010":"self.registers[w[1]]=w[2][1:]",
            "00011":"self.registers[w[1]]=self.registers[w[2]]",
            "00110":"self.registers[w[1]]=int(self.registers[w[2]])*int(self.registers[w[3]])",
            "00111":"self.registers['r0']=int(self.registers[w[2]])/int(self.registers[w[3]])\nself.registers['r1']=int(self.registers[w[2]]) % int(self.registers[w[3]])"
        }
        if(w[0]=="mov"):
            if(w[2] in ["r0","r1","r2","r3","r4","r5","r6","FLAGS"]):
                opcode = self.opcode_table[w[0]][1][0]
            else:
                opcode = self.opcode_table[w[0]][0][0]
        else:
            opcode = self.opcode_table[w[0]][0]
        exec(execute_table[opcode])
        
    def binary(self,str,type):
        w = str.split(" ")
        return(self.opcode_table[w[0]]+("0"*self.type[type]["u"]))
