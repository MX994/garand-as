from Structures.IStructure import *
from Enums.Types import *
from struct import pack

class Command(IStructure):
    def __init__(self, Operation, Condition, Types, Parameters):
        super().__init__()
        self.Operation = Operation
        self.Condition = Condition
        self.Parameters = Parameters
        self.Types = Types

    def GetOperation(self):
        return self.Operation
    
    def GetCondition(self):
        return self.Condition
    
    def GetParameters(self):
        return self.Parameters
    
    def GetTypes(self):
        return self.Types
    
    def Serialize(self):
        CommandBase = ((self.Condition & 0b1111) << 28) | ((self.Operation & 0b111111) << 22)
        ArgIdx = 22
        for Name in self.Types:
            Idx = list(self.Types.keys()).index(Name)
            Typing = self.Types[Name]
            if Typing == 'Reg':
                ArgIdx -= System.RegisterBits.value
                CommandBase |= (self.Parameters[Idx] & (2**System.RegisterBits.value - 1)) << ArgIdx
            elif Typing == 'Imm':
                ArgIdx -= System.ImmediateBits.value
                CommandBase |= (self.Parameters[Idx] & (2**System.ImmediateBits.value - 1)) << ArgIdx
        return pack('L', CommandBase)
