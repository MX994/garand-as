from Syntax import INode
from pathlib import Path
from Enums.Types import Node

class Garand:
    def __init__(self, Defs):
        self.Offset = 0
        self.Buffer = b''
        self.LabelMap = {}
        self.Defs = Defs
        return
    
    def LowerNode(self, Curr : INode):
        match Curr.GetKind():
            case Node.Comment:
                # This is ignored, and doesn't have a lowering representation.
                ...
            case Node.Label:
                self.LabelMap[Curr.GetData().GetName()] = self.Offset
            case Node.Command:
                # Serialize command.
                self.Buffer += Curr.GetData().Serialize()
        return
    
    def LowerNodeList(self, Head : INode):
        self.Offset = 0
        Curr = Head
        while Curr != None:
            # Lower current node.
            self.LowerNode(Curr)
            # Prepare for next iteration.
            Curr = Curr.GetNext()
            self.Offset += 4
        return
    
    def Serialize(self, BinaryPath):
        with Path(BinaryPath).open('wb') as PROG:
            PROG.write(self.Buffer)
            PROG.close()
        return
