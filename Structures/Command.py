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
        LastBitStart = 22
        for Index in range(len(self.Types)):
            Typing = self.Types[list(self.Types.keys())[Index]]
            if not str(Typing).isnumeric():
                MaskedVal = self.Parameters[Index] & 2**Typing['BitSize'] - 1
                CommandBase |= MaskedVal << Typing['BitStart']
                LastBitStart = Typing['BitStart']
            else:
                LastBitStart -= Typing
                MaskedVal = self.Parameters[Index] & (2**Typing - 1)
                CommandBase |= MaskedVal << LastBitStart
        print(pack('L', CommandBase))
        return pack('L', CommandBase)
