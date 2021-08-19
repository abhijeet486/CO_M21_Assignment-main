class programcounter:
    def __init__(self,value):
        self.pc = value

    def getval(self):
        return(self.pc)

    def dump(self):
        s = "{:08b}".format(self.pc)
        print(s,end=" ")

    def update(self,newvalue):
        self.pc = self.pc + newvalue