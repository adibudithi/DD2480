from .constants import (
    Classref, Constant, Double, Fieldref, Float, Integer, InterfaceMethodref,
    Long, Methodref, String,
)


# From: https://en.wikipedia.org/wiki/Java_bytecode_instruction_listings
# Reference" http://docs.oracle.com/javase/specs/jvms/se7/html/jvms-6.html#jvms-6.2

##########################################################################
# 6.2. Opcodes
##########################################################################


class Opcode:
    opcodes = None

    def __init__(self):
        self.references = []
        self.starts_line = None

    def __repr__(self):
        return '<%s%s>' % (self.__class__.__name__, self.__arg_repr__())

    def __arg_repr__(self):
        return ''

    def __len__(self):
        return 1

    @classmethod
    def read(cls, reader, dump=None):
        code = reader.read_u1()
        # Create an index of all known opcodes.
        if Opcode.opcodes is None:
            Opcode.opcodes = {}
            for name in globals():
                klass = globals()[name]
                try:
                    if name != 'Opcode' and issubclass(klass, Opcode):
                        Opcode.opcodes[klass.code] = klass
                except TypeError:
                    pass
        instance = Opcode.opcodes[code].read_extra(reader, dump)
        if dump:
            reader.debug("    " * dump, '%3d: %s' % (reader.offset, instance))
        return instance

    @classmethod
    def read_extra(cls, reader, dump=None):
        return cls()

    def write(self, writer):
        writer.write_u1(self.code)
        self.write_extra(writer)

    def write_extra(self, writer):
        pass

    def resolve(self, constant_pool):
        pass

    @property
    def stack_effect(self):
        return self.produce_count - self.consume_count

    def process(self, context):
        return True


class AALOAD(Opcode):
    # Load onto the stack a reference from an array
    # Stack: arrayref, index → value
    code = 0x32

    def __init__(self):
        super(AALOAD, self).__init__()

    @property
    def consume_count(self):
        return 2

    @property
    def produce_count(self):
        return 1


class AASTORE(Opcode):
    # Store into a reference in an array
    # Stack: arrayref, index, value →
    code = 0x53

    def __init__(self):
        super(AASTORE, self).__init__()

    @property
    def consume_count(self):
        return 3

    @property
    def produce_count(self):
        return 0


class ACONST_NULL(Opcode):
    # Push a null reference onto the stack
    # Stack: → null
    code = 0x01

    def __init__(self):
        super(ACONST_NULL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ALOAD(Opcode):
    # Load a reference onto the stack from a local variable #index
    # Args(1): index
    # Stack: → objectref
    code = 0x19

    def __init__(self, var):
        super(ALOAD, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ALOAD_0(Opcode):
    # Load a reference onto the stack from local variable 0
    # Stack: → objectref
    code = 0x2a

    def __init__(self):
        super(ALOAD_0, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ALOAD_1(Opcode):
    # Load a reference onto the stack from local variable 1
    # Stack: → objectref
    code = 0x2b

    def __init__(self):
        super(ALOAD_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ALOAD_2(Opcode):
    # Load a reference onto the stack from local variable 2
    # Stack: → objectref
    code = 0x2c

    def __init__(self):
        super(ALOAD_2, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ALOAD_3(Opcode):
    # Load a reference onto the stack from local variable 3
    # Stack: → objectref
    code = 0x2d

    def __init__(self):
        super(ALOAD_3, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ANEWARRAY(Opcode):
    # Create a new array of references of length count and component type identified
    # by the class reference index (indexbyte1 << 8 + indexbyte2) in the constant
    # pool
    # Args(2): indexbyte1, indexbyte2
    # Stack: count → arrayref
    code = 0xbd

    def __init__(self, class_name):
        super(ANEWARRAY, self).__init__()
        self.klass = Classref(class_name)

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.klass.name

    @classmethod
    def read_extra(cls, reader, dump=None):
        klass = reader.read_u2()
        return cls(reader.constant_pool[klass].name.bytes.decode('mutf-8'))

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.klass))

    def resolve(self, constant_pool):
        self.klass.resolve(constant_pool)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class ARETURN(Opcode):
    # Return a reference from a method
    # Stack: objectref → [empty]
    code = 0xb0

    def __init__(self):
        super(ARETURN, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ARRAYLENGTH(Opcode):
    # Get the length of an array
    # arrayref → length
    code = 0xbe

    def __init__(self):
        super(ARRAYLENGTH, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class ASTORE(Opcode):
    # Store a reference into a local variable #index
    # Args(1): index
    # Stack: objectref →
    code = 0x3a

    def __init__(self, var):
        super(ASTORE, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ASTORE_0(Opcode):
    # Store a reference into local variable 0
    # Stack: objectref →
    code = 0x4b

    def __init__(self):
        super(ASTORE_0, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ASTORE_1(Opcode):
    # Store a reference into local variable 1
    # Stack: objectref →
    code = 0x4c

    def __init__(self):
        super(ASTORE_1, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ASTORE_2(Opcode):
    # Store a reference into local variable 2
    # Stack: objectref →
    code = 0x4d

    def __init__(self):
        super(ASTORE_2, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ASTORE_3(Opcode):
    # Store a reference into local variable 3
    # Stack: objectref →
    code = 0x4e

    def __init__(self):
        super(ASTORE_3, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ATHROW(Opcode):
    # Throws an error or exception (notice that the rest of the stack is cleared,
    # leaving only a reference to the Throwable)
    # Stack: objectref → [empty], objectref
    code = 0xbf

    def __init__(self):
        super(ATHROW, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 0


class BALOAD(Opcode):
    # Load a byte or Boolean value from an array
    # Stack: arrayref, index → value
    code = 0x33

    def __init__(self):
        super(BALOAD, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 3


class BASTORE(Opcode):
    # Store a byte or Boolean value into an array
    # Stack: arrayref, index, value →
    code = 0x54

    def __init__(self):
        super(BASTORE, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 3


class BIPUSH(Opcode):
    # Push a byte onto the stack as an integer value
    # Args(1) byte
    # Stack: → value
    code = 0x10

    def __init__(self, const):
        super(BIPUSH, self).__init__()
        self.const = const

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' ' + repr(self.const)

    @classmethod
    def read_extra(cls, reader, dump=None):
        const = reader.read_s1()
        return cls(const)

    def write_extra(self, writer):
        writer.write_s1(self.const)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class BREAKPOINT(Opcode):
    # Reserved for breakpoints in Java debuggers; should not appear in any class file
    code = 0xca

    def __init__(self):
        super(BREAKPOINT, self).__init__()


class CALOAD(Opcode):
    # Load a char from an array
    # Stack: arrayref, index → value
    code = 0x34

    def __init__(self):
        super(CALOAD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class CASTORE(Opcode):
    # Store a char into an array
    # Stack: arrayref, index, value →
    code = 0x55

    def __init__(self):
        super(CASTORE, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 3


class CHECKCAST(Opcode):
    # Checks whether an objectref is of a certain type, the class reference of which
    # is in the constant pool at index (indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: objectref → objectref
    code = 0xc0

    def __init__(self, class_name):
        super(CHECKCAST, self).__init__()
        self.klass = Classref(class_name)

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % (self.klass)

    @classmethod
    def read_extra(cls, reader, dump=None):
        class_name = reader.constant_pool[reader.read_u2()].name.bytes.decode('mutf-8')
        return cls(class_name)

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.klass))

    def resolve(self, constant_pool):
        self.klass.resolve(constant_pool)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class D2F(Opcode):
    # Convert a double to a float
    # Stack: value → result
    code = 0x90

    def __init__(self):
        super(D2F, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class D2I(Opcode):
    # Convert a double to an int
    # Stack: value → result
    code = 0x8e

    def __init__(self):
        super(D2I, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class D2L(Opcode):
    # Convert a double to a long
    # Stack: value → result
    code = 0x8f

    def __init__(self):
        super(D2L, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class DADD(Opcode):
    # Add two doubles
    # Stack: value1, value2 → result
    code = 0x63

    def __init__(self):
        super(DADD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DALOAD(Opcode):
    # Load a double from an array
    # Stack: arrayref, index → value
    code = 0x31

    def __init__(self):
        super(DALOAD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DASTORE(Opcode):
    # Store a double into an array
    # Stack: arrayref, index, value →
    code = 0x52

    def __init__(self):
        super(DASTORE, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 3


class DCMPG(Opcode):
    # Compare two doubles
    # Stack: value1, value2 → result
    code = 0x98

    def __init__(self):
        super(DCMPG, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DCMPL(Opcode):
    # Compare two doubles
    # Stack: value1, value2 → result
    code = 0x97

    def __init__(self):
        super(DCMPL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DCONST_0(Opcode):
    # Push the constant 0.0 onto the stack
    # Stack: → 0.0
    code = 0x0e

    def __init__(self):
        super(DCONST_0, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DCONST_1(Opcode):
    # Push the constant 1.0 onto the stack
    # Stack:  → 1.0
    code = 0x0f

    def __init__(self):
        super(DCONST_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DDIV(Opcode):
    # Divide two doubles
    # Stack: value1, value2 → result
    code = 0x6f

    def __init__(self):
        super(DDIV, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DLOAD(Opcode):
    # Load a double value from a local variable #index
    # Args(1): index
    # Stack: → value
    code = 0x18

    def __init__(self, var):
        super(DLOAD, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DLOAD_0(Opcode):
    # Load a double from local variable 0
    # Stack: → value
    code = 0x26

    def __init__(self, var):
        super(DLOAD_0, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DLOAD_1(Opcode):
    # Load a double from local variable 1
    # Stack: → value
    code = 0x27

    def __init__(self):
        super(DLOAD_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DLOAD_2(Opcode):
    # Load a double from local variable 2
    # Stack: → value
    code = 0x28

    def __init__(self):
        super(DLOAD_2, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DLOAD_3(Opcode):
    # Load a double from local variable 3
    # Stack: → value
    code = 0x29

    def __init__(self):
        super(DLOAD_3, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DMUL(Opcode):
    # Multiply two doubles
    # Stack: value1, value2 → result
    code = 0x6b

    def __init__(self):
        super(DMUL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DNEG(Opcode):
    # Negate a double
    # Stack: value → result
    code = 0x77

    def __init__(self):
        super(DNEG, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class DREM(Opcode):
    # Get the remainder from a division between two doubles
    # value1, value2 → result
    code = 0x73

    def __init__(self):
        super(DREM, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DRETURN(Opcode):
    # Return a double from a method
    # Stack:value → [empty]
    code = 0xaf

    def __init__(self):
        super(DRETURN, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class DSTORE(Opcode):
    # Store a double value into a local variable #index
    # Args(1): index
    # Stack: value →
    code = 0x39

    def __init__(self, var):
        super(DSTORE, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class DSTORE_0(Opcode):
    # Store a double into local variable 0
    # Stack: value →
    code = 0x47

    def __init__(self):
        super(DSTORE_0, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class DSTORE_1(Opcode):
    # Store a double into local variable 1
    # Stack: value →
    code = 0x48

    def __init__(self):
        super(DSTORE_1, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class DSTORE_2(Opcode):
    # Store a double into local variable 2
    # Stack: value →
    code = 0x49

    def __init__(self):
        super(DSTORE_2, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class DSTORE_3(Opcode):
    # Store a double into local variable 3
    # Stack: value →
    code = 0x4a

    def __init__(self):
        super(DSTORE_3, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class DSUB(Opcode):
    # Subtract a double from another
    # Stack: value1, value2 → result
    code = 0x67

    def __init__(self):
        super(DSUB, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class DUP(Opcode):
    # Duplicate the value on top of the stack
    # value → value, value
    code = 0x59

    def __init__(self):
        super(DUP, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class DUP_X1(Opcode):
    # Insert a copy of the top value into the stack two values from the top. value1
    # and value2 must not be of the type double or long.
    # Stack: value2, value1 → value1, value2, value1
    code = 0x5a

    def __init__(self):
        super(DUP_X1, self).__init__()

    @property
    def produce_count(self):
        return 3

    @property
    def consume_count(self):
        return 2


class DUP_X2(Opcode):
    # Insert a copy of the top value into the stack two (if value2 is double or long
    # it takes up the entry of value3, too) or three values (if value2 is neither
    # double nor long) from the top
    # Stack: value3, value2, value1 → value1, value3, value2, value1
    code = 0x5b

    def __init__(self):
        super(DUP_X2, self).__init__()

    @property
    def produce_count(self):
        return 4

    @property
    def consume_count(self):
        return 3


class DUP2(Opcode):
    # Duplicate top two stack words (two values, if value1 is not double nor long; a
    # single value, if value1 is double or long)
    # Stack: {value2, value1} → {value2, value1}, {value2, value1}
    code = 0x5c

    def __init__(self):
        super(DUP2, self).__init__()

    @property
    def produce_count(self):
        return 4

    @property
    def consume_count(self):
        return 2


class DUP2_X1(Opcode):
    code = 0x5d

    def __init__(self):
        super(DUP2_X1, self).__init__()
# value3, {value2, value1} → {value2, value1}, value3, {value2, value1}
# Duplicate two words and insert beneath third word (see explanation above)

    @property
    def produce_count(self):
        return 4

    @property
    def consume_count(self):
        return 3


class DUP2_X2(Opcode):
    # Duplicate two words and insert beneath fourth word
    # Stack: {value4, value3}, {value2, value1} → {value2, value1}, {value4, value3}, {value2, value1}
    code = 0x5e

    def __init__(self):
        super(DUP2_X2, self).__init__()

    @property
    def produce_count(self):
        return 6

    @property
    def consume_count(self):
        return 4


class F2D(Opcode):
    # Convert a float to a double
    # Stack: value → result
    code = 0x8d

    def __init__(self):
        super(F2D, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class F2I(Opcode):
    # Convert a float to an int
    # Stack: value → result
    code = 0x8b

    def __init__(self):
        super(F2I, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class F2L(Opcode):
    # Convert a float to a long
    # Stack: value → result
    code = 0x8c

    def __init__(self):
        super(F2L, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class FADD(Opcode):
    # Add two floats
    # value1, value2 → result
    code = 0x62

    def __init__(self):
        super(FADD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class FALOAD(Opcode):
    # Load a float from an array
    # Stack: arrayref, index → value
    code = 0x30

    def __init__(self):
        super(FALOAD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class FASTORE(Opcode):
    # Store a float in an array
    # Stack: arrayref, index, value →
    code = 0x51

    def __init__(self):
        super(FASTORE, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 3


class FCMPG(Opcode):
    # Compare two floats
    # Stack: value1, value2 → result
    code = 0x96

    def __init__(self):
        super(FCMPG, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class FCMPL(Opcode):
    # Compare two floats
    # Stack: value1, value2 → result
    code = 0x95

    def __init__(self):
        super(FCMPL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class FCONST_0(Opcode):
    # Push 0.0f on the stack
    # Stack: → 0.0f
    code = 0x0b

    def __init__(self):
        super(FCONST_0, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FCONST_1(Opcode):
    # Push 1.0f on the stack
    # Stack: → 1.0f
    code = 0x0c

    def __init__(self):
        super(FCONST_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FCONST_2(Opcode):
    # Push 2.0f on the stack
    # Stack: → 2.0f
    code = 0x0d

    def __init__(self):
        super(FCONST_2, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FDIV(Opcode):
    # Divide two floats
    # Stack: value1, value2 → result
    code = 0x6e

    def __init__(self):
        super(FDIV, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class FLOAD(Opcode):
    # Load a float value from a local variable #index
    # Args(1): index
    # Stack: → value
    code = 0x17

    def __init__(self, var):
        super(FLOAD, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FLOAD_0(Opcode):
    # Load a float value from local variable 0
    # Stack: → value
    code = 0x22

    def __init__(self):
        super(FLOAD_0, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FLOAD_1(Opcode):
    # Load a float value from local variable 1
    # Stack: → value
    code = 0x23

    def __init__(self):
        super(FLOAD_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FLOAD_2(Opcode):
    # Load a float value from local variable 2
    # Stack: → value
    code = 0x24

    def __init__(self):
        super(FLOAD_2, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FLOAD_3(Opcode):
    # Load a float value from local variable 3
    # Stack: → value
    code = 0x25

    def __init__(self):
        super(FLOAD_3, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class FMUL(Opcode):
    # Multiply two floats
    # Stack: value1, value2 → result
    code = 0x6a

    def __init__(self):
        super(FMUL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class FNEG(Opcode):
    # Negate a float
    # Stack: value → result
    code = 0x76

    def __init__(self):
        super(FNEG, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class FREM(Opcode):
    # Get the remainder from a division between two floats
    # Stack: value1, value2 → result
    code = 0x72

    def __init__(self):
        super(FREM, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class FRETURN(Opcode):
    # Return a float
    # Stack: value → [empty]
    code = 0xae

    def __init__(self):
        super(FRETURN, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class FSTORE(Opcode):
    # Store a float value into a local variable #index
    # Args(1): index
    # Stack: value →
    code = 0x38

    def __init__(self, var):
        super(FSTORE, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class FSTORE_0(Opcode):
    # Store a float value into local variable 0
    # Stack: value →
    code = 0x43

    def __init__(self):
        super(FSTORE_0, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class FSTORE_1(Opcode):
    # Store a float value into local variable 1
    # Stack: value →
    code = 0x44

    def __init__(self):
        super(FSTORE_1, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class FSTORE_2(Opcode):
    # Store a float value into local variable 2
    # Stack: value →
    code = 0x45

    def __init__(self):
        super(FSTORE_2, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class FSTORE_3(Opcode):
    # Store a float value into local variable 3
    # Stack: value →
    code = 0x46

    def __init__(self):
        super(FSTORE_3, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class FSUB(Opcode):
    # Subtract two floats
    # Stack: value1, value2 → result
    code = 0x66

    def __init__(self):
        super(FSUB, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class GETFIELD(Opcode):
    # Get a field value of an object objectref, where the field is identified by
    # field reference in the constant pool index (index1 << 8 + index2)
    # Args(2): index1, index2
    # Stack: objectref → value
    code = 0xb4

    def __init__(self, class_name, field_name, descriptor):
        super(GETFIELD, self).__init__()
        self.field = Fieldref(class_name, field_name, descriptor)

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s.%s (%s)' % (self.field.class_name, self.field.name, self.field.name_and_type.descriptor)

    @classmethod
    def read_extra(cls, reader, dump=None):
        field = reader.constant_pool[reader.read_u2()]
        return cls(
            field.class_name,
            field.name,
            field.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.field))

    def resolve(self, constant_pool):
        self.field.resolve(constant_pool)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class GETSTATIC(Opcode):
    # Get a static field value of a class, where the field is identified by field
    # reference in the constant pool index (index 1 << 8 + index2)
    # Args(2): index1, index2
    # Stack: → value
    code = 0xb2

    def __init__(self, class_name, field_name, descriptor):
        super(GETSTATIC, self).__init__()
        self.field = Fieldref(class_name, field_name, descriptor)

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s.%s (%s)' % (self.field.class_name, self.field.name, self.field.name_and_type.descriptor)

    @classmethod
    def read_extra(cls, reader, dump=None):
        field = reader.constant_pool[reader.read_u2()]
        return cls(
            field.class_name,
            field.name,
            field.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.field))

    def resolve(self, constant_pool):
        self.field.resolve(constant_pool)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class GOTO(Opcode):
    # Goes to another instruction at branchoffset (signed short constructed from
    # unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: [no change]
    code = 0xa7

    def __init__(self, offset):
        super(GOTO, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 0


class GOTO_W(Opcode):
    # Goes to another instruction at branchoffset (signed int constructed from
    # unsigned bytes branchbyte1 << 24 + branchbyte2 << 16 + branchbyte3 << 8 +
    # branchbyte4)
    # Args(4): branchbyte1, branchbyte2, branchbyte3, branchbyte4
    # Stack: [no change]
    code = 0xc8

    def __init__(self, offset):
        super(GOTO_W, self).__init__()
        self.offset = offset

    def __len__(self):
        return 5

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s4()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s4(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 0


class I2B(Opcode):
    # Convert an int into a byte
    # Stack: value → result
    code = 0x91

    def __init__(self):
        super(I2B, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class I2C(Opcode):
    # Convert an int into a character
    # Stack: value → result
    code = 0x92

    def __init__(self):
        super(I2C, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class I2D(Opcode):
    # Convert an int into a double
    # Stack: value → result
    code = 0x87

    def __init__(self):
        super(I2D, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class I2F(Opcode):
    # Convert an int into a float
    # Stack: value → result
    code = 0x86

    def __init__(self):
        super(I2F, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class I2L(Opcode):
    # Convert an int into a long
    # Stack: value → result
    code = 0x85

    def __init__(self):
        super(I2L, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class I2S(Opcode):
    # Convert an int into a short
    # Stack: value → result
    code = 0x93

    def __init__(self):
        super(I2S, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class IADD(Opcode):
    # Add two ints
    # Stack: value1, value2 → result
    code = 0x60

    def __init__(self):
        super(IADD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class IALOAD(Opcode):
    # Load an int from an array
    # Stack: arrayref, index → value
    code = 0x2e

    def __init__(self):
        super(IALOAD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class IAND(Opcode):
    # Perform a bitwise and on two integers
    # Stack: value1, value2 → result
    code = 0x7e

    def __init__(self):
        super(IAND, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class IASTORE(Opcode):
    # Store an int into an array
    # Stack: arrayref, index, value →
    code = 0x4f

    def __init__(self):
        super(IASTORE, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 3


class ICONST_M1(Opcode):
    # Load the int value -1 onto the stack
    # Stack: → -1
    code = 0x02

    def __init__(self):
        super(ICONST_M1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ICONST_0(Opcode):
    # Load the int value 0 onto the stack
    # Stack: → 0
    code = 0x03

    def __init__(self):
        super(ICONST_0, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ICONST_1(Opcode):
    # Load the int value 1 onto the stack
    # Stack: → 1
    code = 0x04

    def __init__(self):
        super(ICONST_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ICONST_2(Opcode):
    # Load the int value 2 onto the stack
    # Stack: → 2
    code = 0x05

    def __init__(self):
        super(ICONST_2, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ICONST_3(Opcode):
    # Load the int value 3 onto the stack
    # Stack: → 3
    code = 0x06

    def __init__(self):
        super(ICONST_3, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ICONST_4(Opcode):
    # Load the int value 4 onto the stack
    # Stack: → 4
    code = 0x07

    def __init__(self):
        super(ICONST_4, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ICONST_5(Opcode):
    # Load the int value 5 onto the stack
    # Stack: → 5
    code = 0x08

    def __init__(self):
        super(ICONST_5, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class IDIV(Opcode):
    # Divide two integers
    # Stack: value1, value2 → result
    code = 0x6c

    def __init__(self):
        super(IDIV, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class IF_ACMPEQ(Opcode):
    # If references are equal, branch to instruction at branchoffset (signed short
    # constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0xa5

    def __init__(self, offset):
        super(IF_ACMPEQ, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IF_ACMPNE(Opcode):
    # If references are not equal, branch to instruction at branchoffset (signed
    # short constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0xa6

    def __init__(self, offset):
        super(IF_ACMPNE, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IF_ICMPEQ(Opcode):
    # If ints are equal, branch to instruction at branchoffset (signed short
    # constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0x9f

    def __init__(self, offset):
        super(IF_ICMPEQ, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IF_ICMPGE(Opcode):
    # If value1 is greater than or equal to value2, branch to instruction at
    # Iranchoffset (signed short constructed from unsigned bytes branchbyte1 << 8 +
    # branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0xa2

    def __init__(self, offset):
        super(IF_ICMPGE, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IF_ICMPGT(Opcode):
    # If value1 is greater than value2, branch to instruction at branchoffset
    # (signed short constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0xa3

    def __init__(self, offset):
        super(IF_ICMPGT, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IF_ICMPLE(Opcode):
    # If value1 is less than or equal to value2, branch to instruction at
    # Iranchoffset (signed short constructed from unsigned bytes branchbyte1 << 8 +
    # branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0xa4

    def __init__(self, offset):
        super(IF_ICMPLE, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IF_ICMPLT(Opcode):
    # If value1 is less than value2, branch to instruction at branchoffset (signed
    # short constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0xa1

    def __init__(self, offset):
        super(IF_ICMPLT, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IF_ICMPNE(Opcode):
    # If ints are not equal, branch to instruction at branchoffset (signed short
    # constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value1, value2 →
    code = 0xa0

    def __init__(self, offset):
        super(IF_ICMPNE, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class IFEQ(Opcode):
    # If value is 0, branch to instruction at branchoffset (signed short constructed
    # from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0x99

    def __init__(self, offset):
        super(IFEQ, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IFGE(Opcode):
    # If value is greater than or equal to 0, branch to instruction at branchoffset
    # (signed short constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0x9c

    def __init__(self, offset):
        super(IFGE, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IFGT(Opcode):
    # If value is greater than 0, branch to instruction at branchoffset (signed
    # short constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0x9d

    def __init__(self, offset):
        super(IFGT, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IFLE(Opcode):
    # If value is less than or equal to 0, branch to instruction at branchoffset
    # (signed short constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0x9e

    def __init__(self, offset):
        super(IFLE, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IFLT(Opcode):
    # If value is less than 0, branch to instruction at branchoffset (signed short
    # constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0x9b

    def __init__(self, offset):
        super(IFLT, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IFNE(Opcode):
    # If value is not 0, branch to instruction at branchoffset (signed short
    # constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0x9a

    def __init__(self, offset):
        super(IFNE, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IFNONNULL(Opcode):
    # If value is not null, branch to instruction at branchoffset (signed short
    # constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0xc7

    def __init__(self, offset):
        super(IFNONNULL, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IFNULL(Opcode):
    # If value is null, branch to instruction at branchoffset (signed short
    # constructed from unsigned bytes branchbyte1 << 8 + branchbyte2)
    # Args(2): branchbyte1, branchbyte2
    # Stack: value →
    code = 0xc6

    def __init__(self, offset):
        super(IFNULL, self).__init__()
        self.offset = offset

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.offset

    @classmethod
    def read_extra(cls, reader, dump=None):
        offset = reader.read_s2()
        return cls(offset)

    def write_extra(self, writer):
        writer.write_s2(self.offset)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class IINC(Opcode):
    # Increment local variable #index by signed byte const
    # Args(2): index, const
    # Stack: [No change]
    code = 0x84

    def __init__(self, index, const):
        super(IINC, self).__init__()
        self.index = index
        self.const = const

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s %s' % (self.index, self.const)

    @classmethod
    def read_extra(cls, reader, dump=None):
        index = reader.read_u1()
        const = reader.read_u1()
        return cls(index, const)

    def write_extra(self, writer):
        writer.write_u1(self.index)
        writer.write_u1(self.const)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 0


class ILOAD(Opcode):
    # Load an int value from a local variable #index
    # Args(1): index
    # Stack: → value
    code = 0x15

    def __init__(self, var):
        super(ILOAD, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ILOAD_0(Opcode):
    # Load a reference onto the stack from local variable 0
    # Stack: → value
    code = 0x1a

    def __init__(self):
        super(ILOAD_0, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ILOAD_1(Opcode):
    # Load a reference onto the stack from local variable 1
    # Stack: → value
    code = 0x1b

    def __init__(self):
        super(ILOAD_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ILOAD_2(Opcode):
    # Load a reference onto the stack from local variable 2
    # Stack: → value
    code = 0x1c

    def __init__(self):
        super(ILOAD_2, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class ILOAD_3(Opcode):
    # Load a reference onto the stack from local variable 3
    # Stack: → value
    code = 0x1d

    def __init__(self):
        super(ILOAD_3, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class IMPDEP1(Opcode):
    # Reserved for implementation-dependent operations within debuggers; should not
    # appear in any class file
    code = 0xfe

    def __init__(self):
        super(IMPDEP1, self).__init__()


class IMPDEP2(Opcode):
    # Reserved for implementation-dependent operations within debuggers; should not
    # appear in any class file
    code = 0xff

    def __init__(self):
        super(IMPDEP2, self).__init__()


class IMUL(Opcode):
    # Multiply two integers
    # Stack: value1, value2 → result
    code = 0x68

    def __init__(self):
        super(IMUL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class INEG(Opcode):
    # Negate int
    # Stack: value → result
    code = 0x74

    def __init__(self):
        super(INEG, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class INSTANCEOF(Opcode):
    # Determines if an object objectref is of a given type, identified by class
    # reference index in constant pool (indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: objectref → result
    code = 0xc1

    def __init__(self, class_name):
        super(INSTANCEOF, self).__init__()
        self.klass = Classref(class_name)

    def __arg_repr__(self):
        return ' %s' % self.klass.class_name

    def __len__(self):
        return 3

    @classmethod
    def read_extra(cls, reader, dump=None):
        klass = reader.constant_pool[reader.read_u2()]
        return cls(
            klass.name.bytes.decode('mutf-8'),
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.klass))

    def resolve(self, constant_pool):
        self.klass.resolve(constant_pool)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


def _compose_descriptor(descriptor, args, returns):
    if descriptor is not None:
        if not (args is None and returns is None):
            raise TypeError("Cannot specify both a descriptor and args/returns")
        return descriptor

    return '(%s)%s' % (
        ''.join(a for a in args),
        returns
    )


class INVOKEDYNAMIC(Opcode):
    # Invokes a dynamic method and puts the result on the stack (might be void); the
    # method is identified by method reference index in constant pool (indexbyte1 <<
    # 8 + indexbyte2)
    # Args(4): indexbyte1, indexbyte2, 0, 0
    # Stack: [arg1, [arg2 ...]] → result
    code = 0xba

    def __init__(self, class_name, method_name, descriptor=None, args=None, returns=None):
        super(INVOKEDYNAMIC, self).__init__()
        descriptor = _compose_descriptor(descriptor, args, returns)
        self.method = Methodref(class_name, method_name, descriptor)

    def __arg_repr__(self):
        return ' %s.%s %s' % (self.method.class_name, self.method.name, self.method.name_and_type.descriptor)

    def __len__(self):
        return 5

    @classmethod
    def read_extra(cls, reader, dump=None):
        method = reader.constant_pool[reader.read_u2()]
        reader.read_u2()
        return cls(
            method.klass.name.bytes.decode('mutf-8'),
            method.name_and_type.name.bytes.decode('mutf-8'),
            method.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.method))
        writer.write_u2(0)

    def resolve(self, constant_pool):
        self.method.resolve(constant_pool)

    @property
    def produce_count(self):
        return 0 if self.method.name_and_type.descriptor.bytes[-1] == ord('V') else 1

    @property
    def consume_count(self):
        return 1 + len(self.method.descriptor.parameters)


class INVOKEINTERFACE(Opcode):
    # Invokes an interface method on object objectref and puts the result on the
    # stack (might be void); the interface method is identified by method reference
    # index in constant pool (indexbyte1 << 8 + indexbyte2)
    # Args(4): indexbyte1, indexbyte2, count, 0
    # Stack: objectref, [arg1, arg2, ...] → result
    code = 0xb9

    def __init__(self, class_name, method_name, descriptor=None, args=None, returns=None):
        super(INVOKEINTERFACE, self).__init__()
        descriptor = _compose_descriptor(descriptor, args, returns)
        self.method = InterfaceMethodref(class_name, method_name, descriptor)

    def __arg_repr__(self):
        return ' %s.%s %s' % (self.method.class_name, self.method.name, self.method.name_and_type.descriptor)

    def __len__(self):
        return 5

    @classmethod
    def read_extra(cls, reader, dump=None):
        method = reader.constant_pool[reader.read_u2()]
        reader.read_u1()  # Count (can be interpolated from parameters)
        reader.read_u1()  # Blank value
        return cls(
            method.class_name,
            method.name,
            method.name_and_type.descriptor.bytes.decode('mutf-8'),
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.method))
        writer.write_u1(len(self.method.descriptor.parameters) + 1)
        writer.write_u1(0)

    def resolve(self, constant_pool):
        self.method.resolve(constant_pool)

    @property
    def produce_count(self):
        return 0 if self.method.name_and_type.descriptor.bytes[-1] == ord('V') else 1

    @property
    def consume_count(self):
        return 1 + len(self.method.descriptor.parameters)


class INVOKESPECIAL(Opcode):
    # Invoke instance method on object objectref and puts the result on the stack
    # (might be void); the method is identified by method reference index in
    # constant pool (indexbyte1 << 8 + indexbyte2)
    # Args (2): indexbyte1, indexbyte2
    # Stack: objectref, [arg1, arg2, ...] → result
    code = 0xb7

    def __init__(self, class_name, method_name, descriptor=None, args=None, returns=None):
        super(INVOKESPECIAL, self).__init__()
        descriptor = _compose_descriptor(descriptor, args, returns)
        self.method = Methodref(class_name, method_name, descriptor)

    def __arg_repr__(self):
        return ' %s.%s %s' % (
            self.method.klass.name,
            self.method.name_and_type.name,
            self.method.name_and_type.descriptor
        )

    def __len__(self):
        return 3

    @property
    def class_name(self):
        return self.method.class_name

    @property
    def method_name(self):
        return self.method.method_name

    @property
    def descriptor(self):
        return self.method.descriptor

    @classmethod
    def read_extra(cls, reader, dump=None):
        method = reader.constant_pool[reader.read_u2()]
        return cls(
            method.klass.name.bytes.decode('mutf-8'),
            method.name_and_type.name.bytes.decode('mutf-8'),
            method.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.method))

    def resolve(self, constant_pool):
        self.method.resolve(constant_pool)

    @property
    def produce_count(self):
        return 0 if self.method.name_and_type.descriptor.bytes[-1] == ord('V') else 1

    @property
    def consume_count(self):
        return 1 + len(self.method.descriptor.parameters)


class INVOKESTATIC(Opcode):
    # Invoke a static method and puts the result on the stack (might be void); the
    # method is identified by method reference index in constant pool (indexbyte1 <<
    # 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: [arg1, arg2, ...] → result
    code = 0xb8

    def __init__(self, class_name, method_name, descriptor=None, args=None, returns=None):
        descriptor = _compose_descriptor(descriptor, args, returns)
        super(INVOKESTATIC, self).__init__()
        self.method = Methodref(class_name, method_name, descriptor)

    def __arg_repr__(self):
        return ' %s.%s %s' % (
            self.method.klass.name,
            self.method.name_and_type.name,
            self.method.name_and_type.descriptor
        )

    def __len__(self):
        return 3

    @classmethod
    def read_extra(cls, reader, dump=None):
        method = reader.constant_pool[reader.read_u2()]
        return cls(
            method.klass.name.bytes.decode('mutf-8'),
            method.name_and_type.name.bytes.decode('mutf-8'),
            method.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.method))

    def resolve(self, constant_pool):
        self.method.resolve(constant_pool)

    @property
    def produce_count(self):
        return 0 if self.method.name_and_type.descriptor.bytes[-1] == ord('V') else 1

    @property
    def consume_count(self):
        return len(self.method.descriptor.parameters)


class INVOKEVIRTUAL(Opcode):
    # Invoke virtual method on object objectref and puts the result on the stack
    # (might be void); the method is identified by method reference index in
    # constant pool (indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: objectref, [arg1, arg2, ...] → result
    code = 0xb6

    def __init__(self, class_name, method_name, descriptor=None, args=None, returns=None):
        descriptor = _compose_descriptor(descriptor, args, returns)
        super(INVOKEVIRTUAL, self).__init__()
        self.method = Methodref(class_name, method_name, descriptor)

    def __arg_repr__(self):
        return ' %s.%s %s' % (
            self.method.klass.name,
            self.method.name_and_type.name,
            self.method.name_and_type.descriptor
        )

    def __len__(self):
        return 3

    @classmethod
    def read_extra(cls, reader, dump=None):
        method = reader.constant_pool[reader.read_u2()]
        return cls(
            method.klass.name.bytes.decode('mutf-8'),
            method.name_and_type.name.bytes.decode('mutf-8'),
            method.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.method))

    def resolve(self, constant_pool):
        self.method.resolve(constant_pool)

    @property
    def produce_count(self):
        return 0 if self.method.name_and_type.descriptor.bytes[-1] == ord('V') else 1

    @property
    def consume_count(self):
        return 1 + len(self.method.descriptor.parameters)


class IOR(Opcode):
    # Bitwise int or
    # Stack: value1, value2 → result
    code = 0x80

    def __init__(self):
        super(IOR, self).__init__()


class IREM(Opcode):
    # Logical int remainder
    # Stack: value1, value2 → result
    code = 0x70

    def __init__(self):
        super(IREM, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class IRETURN(Opcode):
    # Return an integer from a method
    # Stack: value → [empty]
    code = 0xac

    def __init__(self):
        super(IRETURN, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ISHL(Opcode):
    # Int shift left
    # Stack: value1, value2 → result
    code = 0x78

    def __init__(self):
        super(ISHL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class ISHR(Opcode):
    # Int arithmetic shift right
    # Stack: value1, value2 → result
    code = 0x7a

    def __init__(self):
        super(ISHR, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class ISTORE(Opcode):
    # Store a reference into a local variable #index
    # Args(1): index
    # Stack: objectref →
    code = 0x36

    def __init__(self, var):
        super(ISTORE, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ISTORE_0(Opcode):
    # Store int value into variable 0
    # Stack: value →
    code = 0x3b

    def __init__(self):
        super(ISTORE_0, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ISTORE_1(Opcode):
    # Store int value into variable 1
    # Stack: value →
    code = 0x3c

    def __init__(self):
        super(ISTORE_1, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ISTORE_2(Opcode):
    # Store int value into variable 2
    # Stack: value →
    code = 0x3d

    def __init__(self):
        super(ISTORE_2, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ISTORE_3(Opcode):
    # Store int value into variable 3
    # Stack: value →
    code = 0x3e

    def __init__(self):
        super(ISTORE_3, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class ISUB(Opcode):
    # Int subtract
    # Stack: value1, value2 → result
    code = 0x64

    def __init__(self):
        super(ISUB, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class IUSHR(Opcode):
    # Int logical shift right
    # Stack: value1, value2 → result
    code = 0x7c

    def __init__(self):
        super(IUSHR, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class IXOR(Opcode):
    # Int xor
    # Stack: value1, value2 → result
    code = 0x82

    def __init__(self):
        super(IXOR, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class JSR(Opcode):
    code = 0xa8

    def __init__(self):
        super(JSR, self).__init__()
# 2: branchbyte1, branchbyte2 → address
# Jump to subroutine at branchoffset (signed short constructed from unsigned
# bytes branchbyte1 << 8 + branchbyte2) and place the return address on the
# stack


class JSR_W(Opcode):
    code = 0xc9

    def __init__(self):
        super(JSR_W, self).__init__()
# 4: branchbyte1, branchbyte2, branchbyte3, branchbyte4   → address
# Jump to subroutine at branchoffset (signed int constructed from unsigned bytes
# branchbyte1 << 24 + branchbyte2 << 16 + branchbyte3 << 8 + branchbyte4) and
# place the return address on the stack


class L2D(Opcode):
    # Convert a long to a double
    # Stack: value → result
    code = 0x8a

    def __init__(self):
        super(L2D, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class L2F(Opcode):
    # Convert a long to a float
    # Stack: value → result
    code = 0x89

    def __init__(self):
        super(L2F, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class L2I(Opcode):
    # Convert a long to a int
    # Stack: value → result
    code = 0x88

    def __init__(self):
        super(L2I, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class LADD(Opcode):
    # add two longs
    # Stack: value1, value2 → result
    code = 0x61

    def __init__(self):
        super(LADD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LALOAD(Opcode):
    # Load a long from an array
    # Stack: arrayref, index → value
    code = 0x2f

    def __init__(self):
        super(LALOAD, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LAND(Opcode):
    # bitwise and of two longs
    # Stack: value1, value2 → result
    code = 0x7f

    def __init__(self):
        super(LAND, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LASTORE(Opcode):
    # Store a long to an array
    # Stack: arrayref, index, value →
    code = 0x50

    def __init__(self):
        super(LASTORE, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 3


class LCMP(Opcode):
    # Compare two longs values
    # Stack: value1, value2 → result
    code = 0x94

    def __init__(self):
        super(LCMP, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LCONST_0(Opcode):
    # Push the long 0 onto the stack
    # Stack: → 0L
    code = 0x09

    def __init__(self):
        super(LCONST_0, self).__init__()

    @property
    def produce_count(self):
        # Although it only produces one value, the wide value
        # takes up 2 slots on the stack.
        return 2

    @property
    def consume_count(self):
        return 0


class LCONST_1(Opcode):
    # Push the long 1 onto the stack
    # Stack: → 1L
    code = 0x0a

    def __init__(self):
        super(LCONST_1, self).__init__()

    @property
    def produce_count(self):
        # Although it only produces one value, the wide value
        # takes up 2 slots on the stack.
        return 2

    @property
    def consume_count(self):
        return 0


class LDC(Opcode):
    # Push a constant #index from a constant pool (String, int or float) onto the
    # stack
    # Args(1): index
    # Stack: → value
    code = 0x12

    def __init__(self, const):
        super(LDC, self).__init__()
        if isinstance(const, str):
            self.const = String(const)
        elif isinstance(const, int):
            self.const = Integer(const)
        # elif isinstance(const, float):
        #     self.const = Float(const)
        elif isinstance(const, Constant):
            self.const = const
        else:
            raise TypeError('Invalid type for LDC: %s' % type(const))

    def __arg_repr__(self):
        return ' %s' % self.const

    def __len__(self):
        return 2

    @classmethod
    def read_extra(cls, reader, dump=None):
        const = reader.read_u1()
        return cls(reader.constant_pool[const])

    def write_extra(self, writer):
        writer.write_u1(writer.constant_pool.index(self.const))

    def resolve(self, constant_pool):
        self.const.resolve(constant_pool)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class LDC_W(Opcode):
    # Push a constant #index from a constant pool (String, int or float) onto the
    # stack (wide index is constructed as indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: → value
    code = 0x13

    def __init__(self, const):
        super(LDC_W, self).__init__()
        if isinstance(const, str):
            self.const = String(const)
        elif isinstance(const, int):
            self.const = Integer(const)
        elif isinstance(const, float):
            self.const = Float(const)
        elif isinstance(const, Constant):
            self.const = const
        else:
            raise TypeError('Invalid type for LDC_W: %s' % type(const))

    def __arg_repr__(self):
        return ' %s' % self.const

    def __len__(self):
        return 3

    @classmethod
    def read_extra(cls, reader, dump=None):
        const = reader.read_u2()
        return cls(reader.constant_pool[const])

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.const))

    def resolve(self, constant_pool):
        self.const.resolve(constant_pool)

    @property
    def produce_count(self):
        # Although it only produces one value, the wide value
        # takes up 2 slots on the stack.
        return 2

    @property
    def consume_count(self):
        return 0


class LDC2_W(Opcode):
    # Push a constant #index from a constant pool (double or long) onto the stack
    # (wide index is constructed as indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: → value
    code = 0x14

    def __init__(self, const):
        super(LDC2_W, self).__init__()
        if isinstance(const, float):
            self.const = Double(const)
        elif isinstance(const, int):
            self.const = Long(const)
        elif isinstance(const, Constant):
            self.const = const
        else:
            raise TypeError('Invalid type for LDC_W: %s' % type(const))

    def __arg_repr__(self):
        return ' %s' % self.const

    def __len__(self):
        return 3

    @classmethod
    def read_extra(cls, reader, dump=None):
        const = reader.read_u2()
        return cls(reader.constant_pool[const])

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.const))

    def resolve(self, constant_pool):
        self.const.resolve(constant_pool)

    @property
    def produce_count(self):
        # Although it only produces one value, the wide value
        # takes up 2 slots on the stack.
        return 2

    @property
    def consume_count(self):
        return 0


class LDIV(Opcode):
    # Divide two longs
    # Stack: value1, value2 → result
    code = 0x6d

    def __init__(self):
        super(LDIV, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LLOAD(Opcode):
    # Load a long value from a local variable #index
    # Args(1): index
    # Stack: → value
    code = 0x16

    def __init__(self, var):
        super(LLOAD, self).__init__()
        self.var = var

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.var

    @classmethod
    def read_extra(cls, reader, dump=None):
        var = reader.read_u1()
        return cls(var)

    def write_extra(self, writer):
        writer.write_u1(self.var)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class LLOAD_0(Opcode):
    # Load a long value from a local variable 0
    # Stack: → value
    code = 0x1e

    def __init__(self):
        super(LLOAD_0, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class LLOAD_1(Opcode):
    # Load a long value from a local variable 1
    # Stack: → value
    code = 0x1f

    def __init__(self):
        super(LLOAD_1, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class LLOAD_2(Opcode):
    # Load a long value from a local variable 2
    # Stack: → value
    code = 0x20

    def __init__(self):
        super(LLOAD_2, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class LLOAD_3(Opcode):
    # Load a long value from a local variable 3
    # Stack: → value
    code = 0x21

    def __init__(self):
        super(LLOAD_3, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class LMUL(Opcode):
    # Multiply two longs
    # Stack: value1, value2 → result
    code = 0x69

    def __init__(self):
        super(LMUL, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LNEG(Opcode):
    # Negate a long
    # Stack: value → result
    code = 0x75

    def __init__(self):
        super(LNEG, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class LOOKUPSWITCH(Opcode):
    code = 0xab

    def __init__(self):
        super(LOOKUPSWITCH, self).__init__()
# 4+: <0-3 bytes padding>, defaultbyte1, defaultbyte2, defaultbyte3, defaultbyte4,
#   npairs1, npairs2, npairs3, npairs4, match-offset pairs...
# key →
# A target address is looked up from a table using a key and execution continues
# from the instruction at that address


class LOR(Opcode):
    # Bitwise or of two longs
    # Stack: value1, value2 → result
    code = 0x81

    def __init__(self):
        super(LOR, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LREM(Opcode):
    # Remainder of division of two longs
    # Stack: value1, value2 → result
    code = 0x71

    def __init__(self):
        super(LREM, self).__init__()

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 2


class LRETURN(Opcode):
    # Return a long value
    # Stack: value → [empty]
    code = 0xad

    def __init__(self):
        super(LRETURN, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class LSHL(Opcode):
    code = 0x79

    def __init__(self):
        super(LSHL, self).__init__()
# value1, value2 → result
# Bitwise shift left of a long value1 by int value2 positions


class LSHR(Opcode):
    code = 0x7b

    def __init__(self):

        super(LSHR, self).__init__()
# value1, value2 → result
# Bitwise shift right of a long value1 by int value2 positions


class LSTORE(Opcode):
    # Store a long value in a local variable #index
    # Args(1): index
    # Stack: value →
    code = 0x37

    def __init__(self):
        super(LSTORE, self).__init__()


class LSTORE_0(Opcode):
    # Store a long value in a local variable 0
    # Stack: value →
    code = 0x3f

    def __init__(self):
        super(LSTORE_0, self).__init__()


class LSTORE_1(Opcode):
    # Store a long value in a local variable 1
    # Stack: value →
    code = 0x40

    def __init__(self):
        super(LSTORE_1, self).__init__()


class LSTORE_2(Opcode):
    # Store a long value in a local variable 2
    # Stack: value →
    code = 0x41

    def __init__(self):
        super(LSTORE_2, self).__init__()


class LSTORE_3(Opcode):
    # Store a long value in a local variable 3
    # Stack: value →
    code = 0x42

    def __init__(self):
        super(LSTORE_3, self).__init__()


class LSUB(Opcode):
    code = 0x65

    def __init__(self):
        super(LSUB, self).__init__()
# value1, value2 → result subtract two longs


class LUSHR(Opcode):
    code = 0x7d

    def __init__(self):
        super(LUSHR, self).__init__()
# value1, value2 → result
# Bitwise shift right of a long value1 by int value2 positions, unsigned


class LXOR(Opcode):
    code = 0x83

    def __init__(self):
        super(LXOR, self).__init__()
# value1, value2 → result
# Bitwise exclusive or of two longs


class MONITORENTER(Opcode):
    code = 0xc2

    def __init__(self):
        super(MONITORENTER, self).__init__()
# objectref →
# Enter monitor for object ("grab the lock" - start of synchronized() section)


class MONITOREXIT(Opcode):
    code = 0xc3

    def __init__(self):
        super(MONITOREXIT, self).__init__()
# objectref →
# Exit monitor for object ("release the lock" - end of synchronized() section)


class MULTIANEWARRAY(Opcode):
    code = 0xc5

    def __init__(self):
        super(MULTIANEWARRAY, self).__init__()
# 3: indexbyte1, indexbyte2, dimensions
# count1, [count2,...] → arrayref
# Create a new array of dimensions dimensions with elements of type identified
# by class reference in constant pool index (indexbyte1 << 8 + indexbyte2); the
# sizes of each dimension is identified by count1, [count2, etc.]


class NEW(Opcode):
    # Create new object of type identified by class reference in constant pool index
    # (indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: → objectref
    code = 0xbb

    def __init__(self, class_name):
        super(NEW, self).__init__()
        self.classref = Classref(class_name)

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.classref.name

    @classmethod
    def read_extra(cls, reader, dump=None):
        classref = reader.constant_pool[reader.read_u2()]
        return cls(
            classref.name.bytes.decode('mutf-8'),
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.classref))

    def resolve(self, constant_pool):
        self.classref.resolve(constant_pool)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class NEWARRAY(Opcode):
    # Create new array with count elements of primitive type identified by atype
    # 1: atype
    # count → arrayref
    code = 0xbc

    # Valid primitive types that NEWARRAY can be created with.
    # For non-primitive types, see ANEWARRAY
    T_BOOLEAN = 4
    T_CHAR = 5
    T_FLOAT = 6
    T_DOUBLE = 7
    T_BYTE = 8
    T_SHORT = 9
    T_INT = 10
    T_LONG = 11

    def __init__(self, atype):
        super(NEWARRAY, self).__init__()
        self.atype = atype

    def __len__(self):
        return 2

    def __arg_repr__(self):
        return ' %s' % self.atype

    @classmethod
    def read_extra(cls, reader, dump=None):
        atype = reader.read_u1()
        return cls(atype)

    def write_extra(self, writer):
        writer.write_u1(self.atype)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 1


class NOP(Opcode):
    # Perform no operation
    # Stack: [No change]
    code = 0x00

    def __init__(self):
        super(NOP, self).__init__()


class POP(Opcode):
    # Discard the top value on the stack
    # Stack: value →
    code = 0x57

    def __init__(self):
        super(POP, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class POP2(Opcode):
    # Discard the top two values on the stack (or one value, if it is a double or long)
    # {value2, value1} →
    code = 0x58

    def __init__(self):
        super(POP2, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class PUTFIELD(Opcode):
    # Set field to value in an object objectref, where the field is identified by a
    # field reference index in constant pool (indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: objectref, value →
    code = 0xb5

    def __init__(self, class_name, field_name, descriptor):
        super(PUTFIELD, self).__init__()
        self.field = Fieldref(class_name, field_name, descriptor)

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s.%s (%s)' % (self.field.klass.name, self.field.name, self.field.name_and_type.descriptor)

    @classmethod
    def read_extra(cls, reader, dump=None):
        field = reader.constant_pool[reader.read_u2()]
        return cls(
            field.class_name,
            field.name,
            field.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.field))

    def resolve(self, constant_pool):
        self.field.resolve(constant_pool)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 2


class PUTSTATIC(Opcode):
    # Set static field to value in a class, where the field is identified by a field
    # reference index in constant pool (indexbyte1 << 8 + indexbyte2)
    # Args(2): indexbyte1, indexbyte2
    # Stack: value →
    code = 0xb3

    def __init__(self, class_name, field_name, descriptor):
        super(PUTSTATIC, self).__init__()
        self.field = Fieldref(class_name, field_name, descriptor)

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s.%s (%s)' % (self.field.klass.name, self.field.name, self.field.name_and_type.descriptor)

    @classmethod
    def read_extra(cls, reader, dump=None):
        field = reader.constant_pool[reader.read_u2()]
        return cls(
            field.class_name,
            field.name,
            field.name_and_type.descriptor.bytes.decode('mutf-8')
        )

    def write_extra(self, writer):
        writer.write_u2(writer.constant_pool.index(self.field))

    def resolve(self, constant_pool):
        self.field.resolve(constant_pool)

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 1


class RET(Opcode):
    code = 0xa9

    def __init__(self):
        super(RET, self).__init__()
# 1: index
# [No change]
# Continue execution from address taken from a local variable #index (the
# asymmetry with jsr is intentional)


class RETURN(Opcode):
    # Return void from method
    # Stack:→ [empty]
    code = 0xb1

    def __init__(self):
        super(RETURN, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 0


class SALOAD(Opcode):
    code = 0x35

    def __init__(self):
        super(SALOAD, self).__init__()
# arrayref, index → value
# Load short from array


class SASTORE(Opcode):
    code = 0x56

    def __init__(self):
        super(SASTORE, self).__init__()
# arrayref, index, value →
# Store short to array


class SIPUSH(Opcode):
    # push a short onto the stack
    # Args(2): byte1, byte2
    # Stack: → value
    code = 0x11

    def __init__(self, const):
        super(SIPUSH, self).__init__()
        self.const = const

    def __len__(self):
        return 3

    def __arg_repr__(self):
        return ' %s' % self.const

    @classmethod
    def read_extra(cls, reader, dump=None):
        const = reader.read_s2()
        return cls(const)

    def write_extra(self, writer):
        writer.write_s2(self.const)

    @property
    def produce_count(self):
        return 1

    @property
    def consume_count(self):
        return 0


class SWAP(Opcode):
    # Swaps two top words on the stack (note that value1 and value2 must not be
    # double or long)
    # Stack: value2, value1 → value1, value2
    code = 0x5f

    def __init__(self):
        super(SWAP, self).__init__()

    @property
    def produce_count(self):
        return 0

    @property
    def consume_count(self):
        return 0


class TABLESWITCH(Opcode):
    code = 0xaa

    def __init__(self):
        super(TABLESWITCH, self).__init__()
# 4+: [0-3 bytes padding], defaultbyte1, defaultbyte2, defaultbyte3, defaultbyte4,
#   lowbyte1, lowbyte2, lowbyte3, lowbyte4,
#   highbyte1, highbyte2, highbyte3, highbyte4, jump offsets...
# index →
# continue execution from an address in the table at offset index


class WIDE(Opcode):
    code = 0xc4

    def __init__(self):
        super(WIDE, self).__init__()
# 3/5: Opcode, indexbyte1, indexbyte2
# or
# iinc, indexbyte1, indexbyte2, countbyte1, countbyte2
# Execute Opcode, where Opcode is either iload, fload, aload, lload, dload,
# istore, fstore, astore, lstore, dstore, or ret, but assume the index is 16
# bit; or execute iinc, where the index is 16 bits and the constant to
# increment by is a signed 16 bit short
