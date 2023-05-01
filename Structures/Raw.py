from Structures.IStructure import *
from Enums.Types import *

class Raw(IStructure):
    def __init__(self, Bytes):
        super().__init__()
        self.Bytes = Bytes
        return
    
    def GetBytes(self):
        return self.Bytes
    
    