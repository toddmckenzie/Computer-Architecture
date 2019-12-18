"""CPU functionality."""
 
import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #memory ??
        #registers ?? register = [0] * 8
        self.reg = [0] * 8 #8 slots
        self.ram = [0] * 256 #256 bytes of memory
        self.pc = 0
        self.branch = {}


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = []
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        file = open('ls8/examples/mult.ls8', 'r')
        for line in file:
            line = line.strip()
            line = line.split('#')
            program.append('0b' + str(line[0]))
            print('0b' + line[0])

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        


        # file.read()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIVD":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, val):
        self.ram[index] = val
        return self.ram[index]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        flag = True
        while flag:

            instruction_register = self.ram[self.pc]
            print(instruction_register)
            if instruction_register == LDI:
                reg_num = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[reg_num] = value
                self.pc += 3
            elif instruction_register == PRN:
                reg_num = self.ram_read(self.pc + 1)
                print(self.reg[reg_num])
                self.pc += 2
            elif instruction_register == MUL:
                reg_num1 = self.ram_read(self.pc + 1)
                reg_num2 = self.ram_read(self.pc + 2)
                self.alu(instruction_register, reg_num1, reg_num2)
            elif instruction_register == HLT:
                flag = False
                break
            else:
                self.pc += 1


            


cpu = CPU()

cpu.load()
cpu.run()


# print(cpu.ram_read())