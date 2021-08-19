class Registers:
    def __init__(self):
        self.registers={
            '000' : '0000000000000000',
            '001' : '0000000000000000',
            '010' : '0000000000000000',
            '011' : '0000000000000000',
            '100' : '0000000000000000',
            '101' : '0000000000000000',
            '110' : '0000000000000000',
            '111' :'0000000000000000'
            }

    def dump(self):
        s = self.registers['000'] + " " + self.registers['001'] + " " + self.registers['010'] + " " + self.registers['011'] + " " + self.registers['100'] + " " + self.registers['101'] + " " + self.registers['110'] + " " + self.registers['111']
        print(s)