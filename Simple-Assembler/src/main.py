import sys
from ISA import ISA

input = sys.stdin

def main():
    for lines in input:
        for line in lines.split("\n"):
            for read in line.split(" "):
                ISA.__init__()
                ISA.type_check(read)

if __name__ == "__main__":
    main()