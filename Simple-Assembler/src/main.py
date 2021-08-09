import sys
import ISA

input = sys.stdin

def main():
    for lines in input:
        for line in lines.split("\n"):
            for read in line.split(" "):
                print(read)

if __name__ == "__main__":
    main()