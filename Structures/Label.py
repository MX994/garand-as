from Structures.IStructure import *
from Enums.Types import *

class Label(IStructure):
    def __init__(self, Name, relative=0):
        super().__init__()
        self.Name = Name
        self.relative = relative
        return
    
    def GetName(self):
        return self.Name

    def GetRelative(self):
        return self.relative