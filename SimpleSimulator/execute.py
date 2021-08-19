
class execute:
    def __init__(self,memory,registers):
        self.mem = memory
        self.reg = registers

    def exec(self, inst, cycle):
        execute_table={
            "00000":"self.registers[w[1]] = '{:016b}'.format(int(self.registers[w[2]],2) + int(self.registers[w[3]],2))",
            "00001":"if (self.registers[w[2]]>self.registers[w[3]]): self.registers[w[1]] = '{:016b}'.format(int(self.registers[w[2]],2)- int(self.registers[w[3]],2))\nelse: self.registers['111']='0000000000001000'",
            "00010":"self.registers[w[1]] = '{:016b}'.format(int(w[2][1:]))",
            "00011":"self.registers[w[1]] = self.registers[w[2]]",
            "00100":"self.registers[w[1]] = vars[w[2]][1]",
            "00101":"vars[w[2]][1] = self.registers[w[1]]",
            "00110":"self.registers[w[1]]='{:016b}'.format(int(self.registers[w[2]],2)*int(self.registers[w[3]],2))",
            "00111":"d=int(self.registers[w[1]],2)//int(self.registers[w[2]],2)\nr =int(self.registers[w[1]],2) % int(self.registers[w[2]],2)\nself.registers['R0']='{:016b}'.format(d)\nself.registers['R1']='{:016b}'.format(r)",
            "10011":"return("
        }
        if inst[:5] == "00000":
            ans = int(self.reg.registers[inst[10:13]],2) + int(self.reg.registers[inst[13:16]],2)
            if(ans>255):
                ans = ans%255
                self.reg.registers['111']='0000000000001000'
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
            return(False,1)
        if inst[:5] == "00001":
            ans = int(self.reg.registers[inst[10:13]],2) - int(self.reg.registers[inst[13:16]],2)
            if(ans<0):
                ans = 0
                self.reg.registers['111']='0000000000001000'
            self.reg.registers[inst[7:10]] = "{0:016b}".format(ans)
        return(False,1)
