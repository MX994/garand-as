from Structures.IStructure import *

class INode:
    def __init__(self, Kind, Data):
        self.Kind = Kind
        self.Data = Data
        self.Next = None
        return

    def GetKind(self):
        return self.Kind

    def GetData(self):
        return self.Data
    
    def GetNext(self):
        return self.Next
    
    def SetNext(self, newNext):
        self.Next = newNext
        return