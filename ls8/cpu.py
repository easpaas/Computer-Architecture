"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # register holds storage via a list
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc =  0
        self.running = False
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001

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

        # For now, we've just hardcoded a program: 
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8 -> call LDI with params R0 and 8 (ADDRESS: 0)
            0b00000000,     # R0    (ADDRESS: 1)
            0b00001000,     # binary value of 8  (ADDRESS: 2)
            0b01000111, # PRN R0 -> call PRN with param R0 (ADDRESS: 3)
            0b00000000,     # R0 (ADDRESS: 4)
            0b00000001, # HLT -> Halt (ADDRESS: 5)
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
                reg_num = self.ram[self.pc+1] # R0 = register 0
                value = self.ram[self.pc+2] # 8
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
                print(f"Did not understand that instruction: {ir} and address {self.pc}")
                sys.exit(1)