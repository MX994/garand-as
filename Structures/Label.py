from Structures.IStructure import *
from Enums.Types import *

class Label(IStructure):
    def __init__(self, Name):
        super().__init__()
        self.Name = Name
        return
    
    def GetName(self):
        return self.Name
