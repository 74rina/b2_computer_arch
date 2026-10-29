# Parameters
BIT_W = 8                           # bit width of CPU
BIT_MASK = 2**BIT_W - 1             # Bit mask for BIT_W
BIT_FMAT = "0" + str(BIT_W) + "b"   # Output format string

# ALU selection signal definition
ALU_S_ADD = 0b000 #0
ALU_S_SUB = 0b001 #1
ALU_S_AND = 0b010 #2
ALU_S_OR  = 0b011 #3
ALU_S_XOR = 0b100 #4
ALU_S_SLL = 0b101 #5 (Shift Left Logical)
ALU_S_SRL = 0b110 #6 (Shift Right Logical)
ALU_S_SRA = 0b111 #7 (Shift Right Arithmetic)

# Output binary value with 2's complement
def printbit(v):
    print("0b" + format((v & BIT_MASK), BIT_FMAT) + " (" + str(v) + ")")

class Wire:
    """Class representing a signal with fixed bit width"""
    
    def __init__(self, value, bit_width=BIT_W):
        self.bit_width = bit_width
        self.mask = (1 << bit_width) - 1
        self.sign_bit = 1 << (bit_width - 1)
        # Mask value to specified bit width
        self._value = value & self.mask
    
    @property
    def unsigned(self):
        """Get as unsigned integer"""
        return self._value
    
    @property
    def signed(self):
        """Get as signed integer"""
        if self._value & self.sign_bit:
            return self._value - (1 << self.bit_width)
        return self._value

    @property
    def bstring(self):
        """Get as binary string"""
        bin = format(self._value, f'0{self.bit_width}b')
        return bin

    def get_bits(self, high, low):
        """Get specified bit range"""
        mask = (1 << (high - low + 1)) - 1
        return (self._value >> low) & mask
    
    def __add__(self, other):
        """Addition"""
        if isinstance(other, Wire):
            result = self.signed + other.signed
        else:
            result = self.signed + other
        return Wire(result, self.bit_width)
    
    def __sub__(self, other):
        """Subtraction"""
        if isinstance(other, Wire):
            result = self.signed - other.signed
        else:
            result = self.signed - other
        return Wire(result, self.bit_width)
    
    def __and__(self, other):
        """Bitwise AND"""
        if isinstance(other, Wire):
            result = self.unsigned & other.unsigned
        else:
            result = self.unsigned & other
        return Wire(result, self.bit_width)
    
    def __or__(self, other):
        """Bitwise OR"""
        if isinstance(other, Wire):
            result = self.unsigned | other.unsigned
        else:
            result = self.unsigned | other
        return Wire(result, self.bit_width)
    
    def __xor__(self, other):
        """Bitwise XOR"""
        if isinstance(other, Wire):
            result = self.unsigned ^ other.unsigned
        else:
            result = self.unsigned ^ other
        return Wire(result, self.bit_width)
    
    def __lshift__(self, shift):
        """Logical left shift"""
        if isinstance(shift, Wire):
            shift = shift.unsigned
        result = (self.unsigned << shift) & self.mask
        return Wire(result, self.bit_width)
    
    def logical_rshift(self, shift):
        """Logical right shift"""
        if isinstance(shift, Wire):
            shift = shift.unsigned
        result = self.unsigned >> shift
        return Wire(result, self.bit_width)
    
    def arithmetic_rshift(self, shift):
        """Arithmetic right shift"""
        if isinstance(shift, Wire):
            shift = shift.unsigned
        # Right shift as signed value
        result = self.signed >> shift
        return Wire(result, self.bit_width)

    def __rshift__(self, shift):
        """Arithmetic right shift"""
        if isinstance(shift, Wire):
            shift = shift.unsigned
        # Right shift as signed value
        result = self.signed >> shift
        return Wire(result, self.bit_width)

    def concat(self, other):
        """Arithmetic right shift"""
        if isinstance(other, Wire):
            return Wire(int(self.bstring + other.bstring, 2), self.bit_width + other.bit_width)
        else:
            print("Unsupported operation for concat")
            return 0

# ALU
def alu(A, B, S):
    # write your own code here
    if S == ALU_S_ADD:
        Y = A + B
    elif S == ALU_S_SUB:
        Y = A - B
    elif S == ALU_S_AND:
        Y = A & B
    elif S == ALU_S_OR:
        Y = A | B
    elif S == ALU_S_XOR:
        Y = A ^ B
    elif S == ALU_S_SLL:
        Y = A << B
    elif S == ALU_S_SRL:
        Y = A.logical_rshift(B)
    elif S == ALU_S_SRA:
        Y = A >> B
    else:
        print("Undefined selection signal")
        Y = Wire(0, BIT_W)

    return Y

# Memory read or write type signal definition
MEM_R = 0b0 #0 load data from memory
MEM_W = 0b1 #1 store data to memory

# Data Path operation type signal definition
DP_ALU = 0b00 #0 ALU operation in the datapath 
DP_MEM = 0b01 #1 Memory operation in the datapath

# Data-memory and Register-file definition
dmem = [Wire(0b0000_1001, BIT_W),
        Wire(0b0000_0100, BIT_W),
        Wire(0b0000_0101, BIT_W),
        Wire(0b0000_0010, BIT_W),
        Wire(0b0000_0000, BIT_W),
        Wire(0b0000_0000, BIT_W),
        Wire(0b0000_0000, BIT_W),
        Wire(0b0000_0000, BIT_W)]
reg  = [Wire(0b0000_0000, BIT_W)] * 4


# Data-memory access function
def dmem_access(maddr, mwe, Wdata):
    if (mwe):
        dmem[maddr.unsigned] = Wdata
        return 0
    else:
        return dmem[maddr.unsigned]

# Register file access functions
def reg_read(A1, A2):
    D1 = reg[A1.unsigned]
    D2 = reg[A2.unsigned]
    return D1, D2

def reg_write(A3, WE, WD3):
    if (WE and A3.unsigned != 0):
        reg[A3.unsigned] = WD3

# Datapath
def datapath(dp_type, op, a1, a2, a3, maddr):
    # ALU Operation
    if dp_type == DP_ALU:
        D1, D2 = reg_read(a1, a2)
        Y = alu(D1, D2, op)
        reg_write(a3, True, Y)

    # Memory Access
    elif dp_type == DP_MEM:
        if op == MEM_R:
            data = dmem_access(maddr, MEM_R, None)
            reg_write(a3, True, data)

        elif op == MEM_W:
            D1, _ = reg_read(a1, Wire(0, BIT_W))
            dmem_access(maddr, MEM_W, D1)

        else:
            print("Undefined memory operation")

    else:
        print("Undefined datapath operation")

# Main routine for test
if __name__ == "__main__":
    NA = 0
    val0 = Wire(0, BIT_W)
    val1 = Wire(1, BIT_W)
    val2 = Wire(2, BIT_W)
    val3 = Wire(3, BIT_W)
    val4 = Wire(4, BIT_W)
    datapath(DP_MEM,     MEM_R,   NA,   NA,  val1, val0) # reg[1] <- dmem[0]
    datapath(DP_MEM,     MEM_R,   NA,   NA,  val2, val1) # reg[2] <- dmem[1]
    datapath(DP_ALU, ALU_S_ADD, val1, val2,  val3,   NA) # reg[3] <- reg[1] + reg[2]
    datapath(DP_MEM,     MEM_R,   NA,   NA,  val1, val2) # reg[1] <- dmem[2]
    datapath(DP_MEM,     MEM_R,   NA,   NA,  val2, val3) # reg[2] <- dmem[3]
    datapath(DP_ALU, ALU_S_ADD, val1, val2,  val2,   NA) # reg[2] <- reg[1] + reg[2]
    datapath(DP_ALU, ALU_S_SUB, val3, val2,  val1,   NA) # reg[1] <- reg[3] - reg[2]
    datapath(DP_MEM,     MEM_W, val1,   NA,    NA, val4) # dmem[4] <- reg[1]

    print("Memory contents:")
    for i in dmem:
        printbit(i.signed)
    print("\nRegister contents:")
    for i in reg:
        printbit(i.signed)
