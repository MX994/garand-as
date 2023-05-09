from Syntax import INode
from pathlib import Path
from Enums.Types import Node

class Garand:
    def __init__(self, Defs):
        self.Buffer = b''
        self.Defs = Defs
        return
    
    def LowerNode(self, Curr : INode):
        match Curr.GetKind():
            case Node.Comment:
                # This is ignored, and doesn't have a lowering representation.
                ...
            case Node.Label:
                # Handled in a higher level.
                ...
            case Node.Command:
                # Serialize command.
                self.Buffer += Curr.GetData().Serialize()
            case Node.Raw:
                Offs = Curr.GetOffset()
                if Offs != -1:
                    PreBuff = self.Buffer[0:Offs]
                    if len(PreBuff) < Offs:
                        # Pad to size
                        PreBuff += b'\x00' * (Offs - len(PreBuff)) 
                    NewBuf = Curr.GetData().GetBytes()
                    PostBuff = self.Buffer[Offs + len(NewBuf):]
                    self.Buffer = PreBuff + NewBuf + PostBuff
        return
    
    def LowerNodeList(self, Head : INode):
        Curr = Head
        while Curr != None:
            # Lower current node.
            self.LowerNode(Curr)
            # Prepare for next iteration.
            # match Curr.GetKind():
            #     case Node.Raw:
            #         self.Offset += len(Curr.GetData().GetBytes())
            #     case Node.Command:
            #         self.Offset += 4
            Curr = Curr.GetNext()
        return
    
    def Serialize(self, BinaryPath):
        with Path(BinaryPath).open('wb') as PROG:
            PROG.write(self.Buffer)
            PROG.close()
        return
