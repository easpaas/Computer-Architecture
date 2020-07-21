"""CPU functionality."""
import sys

class CPU:
    def __init__(self):
        """Construct a new CPU."""

        # register holds 8 bytes
        self.reg = [0] * 8
        self.ram = [0] * 256
        # Program Counter, index into ram 
        self.pc =  0
        self.running = False
        # Load binary
        self.LDI = 0b10000010
        # Print binary
        self.PRN = 0b01000111
        # Halt binary
        self.HLT = 0b00000001
        # Multiply binary
        self.MUL = 0b10100010

    #  accept the address to read and return the value stored there
    def ram_read(self, index):
        return self.ram[index]

    # accept a value to write, and the address to write it to 
    def ram_write(self, index, value):
        self.ram[index] = value

    def load(self):
        """Load a program into memory."""
        
        # At address 0...(memory controller accesses RAM via address)
        address = 0

        if len(sys.argv) != 2:
            print("usage: cpu.py ")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as filename:
                for line in filename:
                    try:
                        line = line.split("#",1)[0]
                        line = int(line, 10)  # int() is base 10 by default
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

        if op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        else: 
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""
        self.running = True
        
        while self.running:
            # IR instruction register, equal to current address in memory
            ir = self.ram[self.pc]

            if ir == self.LDI:  # -- > LDI R0, 8
                reg_num = self.ram_read[self.pc+1] # R0 = register 0
                value = self.ram_read[self.pc+2] # 8
                self.reg[reg_num] = value
                self.pc += 3

            elif ir == self.PRN:
                reg_num = self.ram[self.pc+1]
                print(self.reg[reg_num])
                self.pc += 2

            elif ir == self.HLT:
                self.running = False
                self.pc += 1
            
            # else instruction not understood
            else:
                print(f"Did not understand that instruction: {ir} at address {self.pc}")
                sys.exit(1)
