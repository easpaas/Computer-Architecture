"""CPU functionality."""
import sys

class CPU:
    def __init__(self):
        """Construct a new CPU."""

        # register holds 8 bytes
        self.reg = [0] * 8
        # 256 bytes of memory
        self.ram = [0] * 256
        # Program Counter, index into ram 
        self.pc =  0

    #  accept the address to read and return the value stored there
    def ram_read(self, address):
        return self.ram[address]

    # accept a value to write, and the address to write it to 
    def ram_write(self, address, value):
        self.ram[address] = value

    # Load a value in register
    def LDI(self, a, value):
        self.reg[a] = value

    # Print value at register index  
    def PRN(self, a):
        print(self.reg[a])

    # Halt the CPU
    def HLT(self):
        sys.exit()

    def POP(self, a):
        addr_to_pop_from = self.reg[7]
        value = self.ram_read(addr_to_pop_from)

        reg_num = self.ram_read(self.pc + 1)
        self.reg[reg_num] = value
        
        self.reg[7] += 1

    def PUSH(self, reg):
        self.reg[7] -= 1

        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]

        addr_to_push_to = self.reg[7]
        self.ram_write(value, addr_to_push_to)

    def MUL(self, a, b):
        self.alu('MUL', a, b)
    
    def ADD(self, regA, regB):
        self.alu('ADD', regA, regB)

    def CALL(self, reg): 
        return_addr = self.pc + 2

        self.reg[7] -= 1
        addr_to_push_to = self.reg[7]
        self.ram_write(return_addr,addr_to_push_to)

        reg_num = self.ram_read(self.pc + 1)
        subroutine_addr = self.reg[reg_num]

        self.pc = subroutine_addr

    def RET(self):
        addr_to_pop_from = self.reg[7]
        return_addr = self.ram_read(addr_to_pop_from)
        self.reg[7] += 1

        self.pc = return_addr

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
                        line = int(line, 2)  # int() is base 10 by default
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
        elif op == "MUL":
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
        running = True

        dispatch_table = {
            '0b10000010': self.LDI,
            '0b01000111': self.PRN,
            '0b00000001': self.HLT,
            '0b01000101': self.PUSH,
            '0b01000110': self.POP,
            '0b10100010': self.MUL,
            '0b10100000': self.ADD,
            '0b01010000': self.CALL, 
            '0b00010001': self.RET
        }
        
        while running:
            ir = self.ram_read(self.pc)
            # operand 1
            op1 = self.ram_read(self.pc+1)
            # operand 2
            op2 = self.ram_read(self.pc+2)

            binStr = format(ir, '#010b')
            args = binStr[2:4]
            alu_op = binStr[4]
            set_pc = binStr[5]
            inst_id = binStr[6:]

            if binStr in dispatch_table:
                function = dispatch_table[binStr]
                if args == "00": 
                    function()
                    if set_pc == '0': 
                        self.pc += 1
                elif args == "01": 
                    function(op1)
                    if set_pc == '0': 
                        self.pc += 2
                elif args == "10": 
                    function(op1, op2)
                    if set_pc == '0':
                        self.pc += 3

            # else:
            #     print(f"Did not understand that instruction: {ir} at address {self.pc}")
            #     sys.exit(1)
