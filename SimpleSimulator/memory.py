class memory:
    def __init__(self):
        self.mem = {}
        for i in range(0,256):
            self.mem["{0:08b}".format(i)] = "0000000000000000"


    def fetch(self,pc,cycle):
        inst = self.mem["{0:08b}".format(pc)]
        return(inst)