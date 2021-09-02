import sys
import matplotlib.pyplot as plt
import numpy as np

class memory:
    def __init__(self):
        self.x_scatter = []
        self.y_scatter = []
        self.mem = {}
        for i in range(0,256):
            self.mem["{0:08b}".format(i)] = "0000000000000000"
        input = sys.stdin
        line_no = 0
        for lines in input.readlines():
            for line in lines.split("\n"):
                if(line!="" and line !=" "):
                    self.mem["{0:08b}".format(line_no)] = line
                    line_no +=1

    def fetch(self,pc,cycle):
        self.pc = pc
        inst = self.mem["{0:08b}".format(pc)]
        self.x_scatter+=[cycle]
        self.y_scatter+=[pc]
        return(inst)

    def dump(self):
        for i in self.mem:
            print(self.mem[i])
        self.scatterplot()

    def scatterplot(self):
        x = self.x_scatter
        y = self.y_scatter
        plt.scatter(x,y)
        plt.show()
        plt.savefig('Bounus_plot.png')
        pass
