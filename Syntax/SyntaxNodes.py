from Syntax.INode import *
from Enums.Types import Node
from Structures.Command import *
from Structures.Label import *
from Structures.Comment import *

class SyntaxCommand(INode):
    def __init__(self, Operation, Condition, Args, Parameters):
        super().__init__(Node.Command, Command(Operation, Condition, Args, Parameters))

class SyntaxComment(INode):
    def __init__(self):
        super().__init__(Node.Comment, Comment())

class SyntaxLabel(INode):
    def __init__(self, Name):
        super().__init__(Node.Label, Label(Name))