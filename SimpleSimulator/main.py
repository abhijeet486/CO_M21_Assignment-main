from memory import memory
from programcounter import programcounter
from Registers import Registers
from execute import execute


def main():
    MEM = memory()
    Reg = Registers()
    PC = programcounter(0)
    exe = execute(MEM,Reg)
    halted = False
    cycle = 0
    while not halted:
        inst = MEM.fetch(PC.getval(),cycle)
        halted,nextPC = exe.exec(inst,cycle)
        PC.dump()
        Reg.dump()
        PC.update(nextPC)
        cycle+=1
    MEM.dump()

if __name__=="__main__":
    main()