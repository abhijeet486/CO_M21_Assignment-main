nonmem = 0
mem = 1
r1 = '0000000000000000'
r2 = '0000000000000000'
r3 = '0000000000000000'
r4 = '0000000000000000'
r5 = '0000000000000000'
r6 = '0000000000000000'
FLAGS = '0000000000000000'


class ISA:
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
        self.registers = {
            'r0' : '000', 
            'r1' : '001',
            'r2' : '010',
            'r3' : '011',
            'r4' : '100',
            'r5' : '101',
            'r6' : '110',
            'FLAGS' : '111'}
        self.type = {
            'A': {"o":5, "u":2, "r1":3, "r":3, "r3":3},
            'B': {"o":5, "r1":3, "imm":8},
            'C': {"o":5, "u":5, "r1":3,"r2":3},
            'D': {"o":5, "r1":3 ,"mem":8},
            'E': {"o":5, "u":3, "mem":8},
            'F': {"o":5,"u":11}
        }
    def type_check(self,inst):
        t = self.opcode_table[inst[0]][2]
        if(t=='A'):
            if(inst[7:9] in ['000','001','010','011','100','101','110','111'] and inst[10:12] in ['000','001','010','011','100','101','110','1111'] and inst[13:15] in ['000','001','010','011','100','101','110','1111']):
                return(True)
            else:
                return(False)
        elif(t=='B'):
            if(inst[8:10] in ['000','001','010','011','100','101','110','1111']):
                return(True)
            else:
                return(False)
        elif(t=='C'):
            if(True):
                return(True)
            else:
                return(False)
        else:
            return(False)
