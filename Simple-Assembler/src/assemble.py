

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
            "00000":"self.registers[w[1]] = '{:016b}'.format(int(self.registers[w[2]],2) + int(self.registers[w[3]],2))",
            "00001":"if (self.registers[w[2]]>self.registers[w[3]]): self.registers[w[1]] = '{:016b}'.format(int(self.registers[w[2]],2)- int(self.registers[w[3]],2))\nelse: self.registers['FLAGS']='0000000000001000'",
            "00010":"self.registers[w[1]] = '{:016b}'.format(int(w[2][1:]))",
            "00011":"self.registers[w[1]] = self.registers[w[2]]",
            "00110":"self.registers[w[1]]='{:016b}'.format(int(self.registers[w[2]],2)*int(self.registers[w[3]],2))",
            "00111":"d=int(self.registers[w[1]],2)//int(self.registers[w[2]],2)\nr =int(self.registers[w[1]],2) % int(self.registers[w[2]],2)\nself.registers['r0']='{:016b}'.format(d)\nself.registers['r1']='{:016b}'.format(r)"
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
        if(type=='A'):
            s = self.opcode_table[w[0]][0] + ("0"*2) + self.registers_address[w[1]] + self.registers_address[w[2]] + self.registers_address[w[3]]
        elif(type=="B"):
            if(w[0]=="mov"):
                s = self.opcode_table[w[0]][0][0] + self.registers_address[w[1]] + '{:08b}'.format(int(w[2][1:]))
            else:
                s = self.opcode_table[w[0]][0] + self.registers_address[w[1]]  + '{:08b}'.format(int(w[2][1:]))
        elif(type=='C'):
            if(w[0]=='mov'):
                s = self.opcode_table[w[0]][1][0] + ("0"*5) + self.registers_address[w[1]] + self.registers_address[w[2]]
            else:
                s = self.opcode_table[w[0]][0] + ("0"*5) + self.registers_address[w[1]] + self.registers_address[w[2]] 
        elif(type=='D'):
            s = self.opcode_table[w[0]][0] + self.registers_address[w[1]] + '{:08b}'.format(int(w[2][1:]))
        elif(type=='E'):
            s = self.opcode_table[w[0]][0] + ("0"*3) + '{:08b}'.format(int(w[1][1:]))
        elif(type=='F'):
            s = self.opcode_table[w[0]][0] + ("0"*11)
        return(s)

