
class execute:
    def __init__(self,memory,registers):
        self.mem = memory
        self.reg = registers

    def exec(self, inst, cycle):
        opcode = inst[:5]
        if opcode == "00000":
            ans = int(self.reg.registers[inst[10:13]],2) + int(self.reg.registers[inst[13:]],2)
            if(ans>65535):
                ans = ans%65536
                self.reg.registers['111']='0000000000001000'
            else:
                self.reg.registers['111']='0000000000000000'
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans) 
            return(False,1)
        elif opcode == "00001":
            ans = int(self.reg.registers[inst[10:13]],2) - int(self.reg.registers[inst[13:]],2)
            if(ans<0):
                ans = 0
                self.reg.registers['111']='0000000000001000'
            else:
                self.reg.registers['111']='0000000000000000'
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
        elif opcode=="00010":
            self.reg.registers[inst[5:8]] = '{:016b}'.format(int(inst[8:],2))
            self.reg.registers['111']='0000000000000000'
        elif opcode =="00011":
            self.reg.registers[inst[10:13]] = self.reg.registers[inst[13:]]
            self.reg.registers['111']='0000000000000000'
        elif opcode == "00100":
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [int(inst[8:],2)]
            self.reg.registers[inst[5:8]] = self.mem.mem[inst[8:]]
            self.reg.registers['111']='0000000000000000'
        elif opcode == "00101":
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [int(inst[8:],2)]
            self.mem.mem[inst[8:]] = self.reg.registers[inst[5:8]]
            self.reg.registers['111']='0000000000000000'
        elif opcode == "00110":
            ans = int(self.reg.registers[inst[10:13]],2) * int(self.reg.registers[inst[13:]],2)
            if(ans>65535):
                ans = ans%65536
                self.reg.registers['111']='0000000000001000'
            else:
                self.reg.registers['111']='0000000000000000'
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
            return(False,1)
        elif opcode == "00111":
            ans = int(self.reg.registers[inst[10:13]],2) // int(self.reg.registers[inst[13:]],2)
            self.reg.registers['000'] = '{0:016b}'.format(ans)
            ans = int(self.reg.registers[inst[10:13]],2) % int(self.reg.registers[inst[13:]],2)
            self.reg.registers['001'] = '{0:016b}'.format(ans)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01000":
            ans = "{0:016b}".format(int(self.reg.registers[inst[5:8]],2) >> int(inst[8:],2))
            self.reg.registers[inst[5:8]] = ans
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01001":
            ans = "{0:016b}".format(int(self.reg.registers[inst[5:8]],2) << int(inst[8:],2))
            self.reg.registers[inst[5:8]] = ans
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01010":
            ans = int(self.reg.registers[inst[10:13]],2) ^ int(self.reg.registers[inst[13:]],2)
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01011":
            ans = int(self.reg.registers[inst[10:13]],2) | int(self.reg.registers[inst[13:]],2)
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01100":
            ans = int(self.reg.registers[inst[10:13]],2) & int(self.reg.registers[inst[13:]],2)
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01101":
            ans = 65535 - int(self.reg.registers[inst[13:]],2)
            self.reg.registers[inst[10:13]] = "{0:016b}".format(ans)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01110":
            op1 = self.reg.registers[inst[10:13]]
            op2 = self.reg.registers[inst[13:]]
            if op1<op2:
                self.reg.registers['111'] = '0000000000000100'
            elif op2<op1:
                self.reg.registers['111'] = '0000000000000010'
            else:
                self.reg.registers['111'] = '0000000000000001'
        elif opcode == "01111":
            label = int(inst[8:],2)
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [label]
            self.reg.registers['111']='0000000000000000'
            return(False,label - self.mem.pc)
        elif opcode == "10000":
            label = int(inst[8:],2)
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [label]
            if(self.reg.registers['111'][13]=='1'):
                self.reg.registers['111']='0000000000000000'
                return(False, label - self.mem.pc)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "10001":
            label = int(inst[8:],2)
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [label]
            if(self.reg.registers['111'][14]=='1'):
                self.reg.registers['111']='0000000000000000'
                return(False,label - self.mem.pc)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "10010":
            label = int(inst[8:],2)
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [label]
            if(self.reg.registers['111'][15]=='1'):
                self.reg.registers['111']='0000000000000000'
                return(False,label - self.mem.pc)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "10011":
            self.reg.registers['111']='0000000000000000'
            return(True,1)
        return(False,1)

