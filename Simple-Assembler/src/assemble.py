import re

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
            "je": ('10010',mem,'E',1,0,True),
            "hlt": ('10011',nonmem,'F',0,0,False)
        }
        self.registers={
            'R0' : '0000000000000000',
            'R1' : '0000000000000000',
            'R2' : '0000000000000000',
            'R3' : '0000000000000000',
            'R4' : '0000000000000000',
            'R5' : '0000000000000000',
            'R6' : '0000000000000000',
            'FLAGS' :'0000000000000000'
            }
        self.registers_address = {
            'R0' : '000', 
            'R1' : '001',
            'R2' : '010',
            'R3' : '011',
            'R4' : '100',
            'R5' : '101',
            'R6' : '110',
            'FLAGS' : '111'
            }

    def type_check(self,str,t,var,label,pos):
        content = str.split(" ")
        if(t=="A"):
            if(content[1] in ["R0","R1","R2","R3","R4","R5","R6"] and (content[2] in ["R0","R1","R2","R3","R4","R5","R6"]) and (content[3] in ["R0","R1","R2","R3","R4","R5","R6"])):
                return(True)
            if("FLAGS" in str):
                print("Error: Illegal use of FLAGS register , line",pos)
            else:
                print("Error: Wrong syntax used for instructions , line ",pos)
            return(False)
        elif(t=="B"):
            if(len(content)==3 and content[1] in ["R0","R1","R2","R3","R4","R5","R6"]):
                try:
                    if(content[2][0]=="$"):
                        if("-" not in content[2] and int(content[2][1:])>=0 and int(content[2][1:])<=255):
                            return(True)
                        print("Error: Illegal Immediate values (less than 0 or more than 255) , line",pos)
                except:
                    pass
            if("FLAGS" in str):
                print("Error: Illegal use of FLAGS register , line",pos)
            print("Error: Wrong syntax used for instructions , line",pos)
            return(False)
        elif(t=="C"):
            if(len(content)==3):
                if(content[1] in ["R0","R1","R2","R3","R4","R5","R6"] and content[2] in ["R0","R1","R2","R3","R4","R5","R6","FLAGS"]):
                    return(True)
                if(content[1]=="FLAGS"):
                    print("Error: Illegal use of FLAGS register , line",pos)
            print("Error: Wrong syntax used for instructions , line",pos)
            return(False)
        elif(t=="D"):
            if("FLAGS" in str):
                    print("Error: Illegal use of FLAGS register , line",pos)
            if(len(content)==3):
                if(content[1] in ["R0","R1","R2","R3","R4","R5","R6"] and content[2] in var):
                    return(True)
                if(content[2] not in var):
                    print("Error: Use of undefined variables , line",pos)
            else:
                print("Error: Wrong syntax used for instructions , line",pos)
            return(False)
        elif(t=="E"):
            if(len(content)==2):
                if(content[1] in label):
                    return(True)
                else:
                    print("Error: Use of undefined labels , line ",pos)
            else:
                print("Error: Wrong syntax used for instructions , line ",pos)
            if("FLAGS" in str):
                    print("Error: Illegal use of FLAGS register , line",pos)
            return(False)
        elif(t=="F"):
            if(content[0]=="hlt"):
                return(True)
            print("Error: Wrong syntax used for instructions , line ",pos)
            return(False)


    def execute(self,str,vars):
        w = str.split(" ")
        execute_table={
            "00000":"self.registers[w[1]] = '{:016b}'.format(int(self.registers[w[2]],2) + int(self.registers[w[3]],2))",
            "00001":"if (self.registers[w[2]]>self.registers[w[3]]): self.registers[w[1]] = '{:016b}'.format(int(self.registers[w[2]],2)- int(self.registers[w[3]],2))\nelse: self.registers['FLAGS']='0000000000001000'",
            "00010":"self.registers[w[1]] = '{:016b}'.format(int(w[2][1:]))",
            "00011":"self.registers[w[1]] = self.registers[w[2]]",
            "00100":"self.registers[w[1]] = vars[w[2]][1]",
            "00101":"vars[w[2]][1] = self.registers[w[1]]",
            "00110":"self.registers[w[1]]='{:016b}'.format(int(self.registers[w[2]],2)*int(self.registers[w[3]],2))",
            "00111":"d=int(self.registers[w[1]],2)//int(self.registers[w[2]],2)\nr =int(self.registers[w[1]],2) % int(self.registers[w[2]],2)\nself.registers['R0']='{:016b}'.format(d)\nself.registers['R1']='{:016b}'.format(r)",
            "10011":"pass"
        }
        if(w[0]=="mov"):
            if(w[2] in ["R0","R1","R2","R3","R4","R5","R6","FLAGS"]):
                opcode = self.opcode_table[w[0]][1][0]
            else:
                opcode = self.opcode_table[w[0]][0][0]
        else:
            opcode = self.opcode_table[w[0]][0]
        exec(execute_table[opcode])
        #return updated variables
        return(vars)
    
    def binary(self,str,type,vars,label):
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
            s = self.opcode_table[w[0]][0] + self.registers_address[w[1]] + '{:08b}'.format(vars[w[2]][0])
        elif(type=='E'):
            s = self.opcode_table[w[0]][0] + ("0"*3) + '{:08b}'.format(int(label[w[1]]))
        elif(type=='F'):
            s = self.opcode_table[w[0]][0] + ("0"*11)
        return(s)

