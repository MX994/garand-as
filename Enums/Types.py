from enum import Enum

class System(Enum):
    IORegFlag = 0b10000
    WORD_SIZE = 4

class Node(Enum):
    Label = 0
    Comment = 1
    Command = 2
    Empty = 3

class GPRegisters(Enum):
    R0 = 0

class IORegisters(Enum):
    I0 = GPRegisters.R0.value | System.IORegFlag.value 