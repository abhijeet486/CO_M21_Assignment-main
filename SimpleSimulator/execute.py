
class execute:
    def __init__(self,memory,registers):
        self.mem = memory
        self.reg = registers

    def exec(self, inst, cycle):
        opcode = inst[:5]
        if opcode == "00000":
            ans = int(self.reg.registers[inst[10:13]],2) + int(self.reg.registers[inst[13:]],2)
            if(ans>255):
                ans = ans%255
                self.reg.registers['111']='0000000000001000'
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans) 
            return(False,1)
        elif opcode == "00001":
            ans = int(self.reg.registers[inst[10:13]],2) - int(self.reg.registers[inst[13:]],2)
            if(ans<0):
                ans = 0
                self.reg.registers['111']='0000000000001000'
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
            if(ans>255):
                ans = ans%255
                self.reg.registers['111']='0000000000001000'
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
            return(False,1)
        elif opcode == "00111":
            ans = int(self.reg.registers[inst[10:13]],2) // int(self.reg.registers[inst[13:]],2)
            self.reg.registers['000'] = '{0:016b}'.format(ans)
            ans = int(self.reg.registers[inst[10:13]],2) % int(self.reg.registers[inst[13:]],2)
            self.reg.registers['001'] = '{0:016b}'.format(ans)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01000":
            ans = self.reg.registers[inst[5:8]] >> int(inst[8:],2)
            self.reg.registers[inst[5:8]] = '{0:016b}'.format(ans)
            self.reg.registers['111']='0000000000000000'
        elif opcode == "01001":
            ans = self.reg.registers[inst[5:8]] << int(inst[8:],2)
            self.reg.registers[inst[5:8]] = '{0:016b}'.format(ans)
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
            self.reg.registers[inst[10:13]] = ~ self.reg.registers[inst[13:]]
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
            self.reg.registers['111']='0000000000000000'
            if(self.reg.registers['111'][13]=='1'):
                return(False, label - self.mem.pc)
        elif opcode == "10001":
            label = int(inst[8:],2)
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [label]
            self.reg.registers['111']='0000000000000000'
            if(self.reg.registers['111'][-2]=='1'):
                return(False,label - self.mem.pc)
        elif opcode == "10010":
            label = int(inst[8:],2)
            self.mem.x_scatter += [cycle]
            self.mem.y_scatter += [label]
            self.reg.registers['111']='0000000000000000'
            if(self.reg.registers['111'][-1]=='1'):
                return(False,label - self.mem.pc)
        elif opcode == "10011":
            self.reg.registers['111']='0000000000000000'
            return(True,1)
        
        return(False,1)

