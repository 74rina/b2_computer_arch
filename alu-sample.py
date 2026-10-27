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

# Main routine for test
if __name__ == "__main__":
    A = Wire(0b0000_0110, BIT_W); B = Wire(0b0011_0010, BIT_W);
    S = ALU_S_ADD; printbit(alu(A, B, S).signed)
    S = ALU_S_SUB; printbit(alu(A, B, S).signed)
    S = ALU_S_AND; printbit(alu(A, B, S).signed)
    S = ALU_S_OR;  printbit(alu(A, B, S).signed)
    S = ALU_S_XOR; printbit(alu(A, B, S).signed)
    
    A = Wire(0b1000_0110, BIT_W); B = Wire(0b0000_0010, BIT_W);
    S = ALU_S_SLL; printbit(alu(A, B, S).signed)
    S = ALU_S_SRL; printbit(alu(A, B, S).signed)
    S = ALU_S_SRA; printbit(alu(A, B, S).signed)

