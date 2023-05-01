from Syntax.SyntaxNodes import *
import sys

class Tokenizer:
    @staticmethod
    def Tokenize(Data, Opcodes : dict, Conditions):
        Head = None
        Curr = None
        Labels = []
        LabelOffsetMap = {}
        LineNo = 1
        Offset = [0]
        for Line in Data:
            try:
                NewNode = Tokenizer.TokenizeLine(Line, Opcodes, Conditions, Labels, Offset, LabelOffsetMap)
                if Head == None:
                    Head = NewNode
                else:
                    Curr.SetNext(NewNode)
                Curr = NewNode
                LineNo += 1
            except Exception as e:
                print(f'Error (Line {LineNo}): {e}')
                sys.exit(1)
        return Head
    
    @staticmethod
    # Naively tokenize string.
    def TokenizeLine(String, Opcodes : dict, Conditions, Labels, Offset, Map):
        if len(String) == 0 or String == '\n':
            # Empty string; no tokens.
            return SyntaxComment()
        
        PossibleTokens = String.split()
        if len(PossibleTokens) < 2:
            raise Exception('Missing arguments.')
        if PossibleTokens[0].startswith('#'):
            # Comment; doesn't matter.
            return SyntaxComment()
        if PossibleTokens[0] == 'def':
            # Label.
            Node = SyntaxLabel(PossibleTokens[1])
            Labels.append(Node.GetData())
            Map[Node.GetData().GetName()] = Offset[0]
            return SyntaxLabel(PossibleTokens[1])
        
        # Likely a command. Try to parse it.     
        CommandNames = list(Opcodes.keys())

        Op = None
        CondCode = None
        
        # Check if there is a condition code attached to it.
        if '.' in PossibleTokens[0]:
            NameSpl = PossibleTokens[0].split('.')
            if len(NameSpl) != 2:
                raise Exception(f'Condition code not specified.')
            if NameSpl[0] not in CommandNames:
                raise Exception(f'Command name "{NameSpl[0]}" is nonsense!')
            if NameSpl[1] not in Conditions:
                raise Exception(f'Condition code "{NameSpl[1]}" invalid.')
            Op = NameSpl[0]
            CondCode = Conditions.index(NameSpl[1])
        elif PossibleTokens[0] not in CommandNames:
            raise Exception(f'Command name "{PossibleTokens[0]}" is nonsense!')
        else:
            Op = PossibleTokens[0]
        print(Op, CondCode)
        Parameters = []
        for Parameter in PossibleTokens[1:]:
            # Just for sanity.
            ParameterNoComma = Parameter.strip(',')
            # Check in the following order:
            # - Registers (GP -> IO)
            # - Immediate
            # - Label
            if ParameterNoComma.startswith('R'):
                RegIndex = ParameterNoComma[1:]
                if not RegIndex.isnumeric():
                    raise Exception(f'No idea what register "{ParameterNoComma}" is.')
                Parameters.append(int(RegIndex))
                continue
            elif ParameterNoComma.startswith('I'):
                RegIndex = ParameterNoComma[1:]
                if not RegIndex.isnumeric():
                    raise Exception(f'No idea what register "{ParameterNoComma}" is.')
                Parameters.append(int(RegIndex))
                continue
            # Probably an immediate, or label.
            # Try immediate first.
            elif ParameterNoComma.startswith('#'):
                # Immediate.
                if not ParameterNoComma[1:].isnumeric():
                    raise Exception(f'No idea what immediate "{ParameterNoComma}" is.')
                Parameters.append(int(ParameterNoComma[1:]))
                continue
            elif any(map(lambda x: x.GetName() == ParameterNoComma, Labels)):
                Parameters.append(Map[ParameterNoComma])
                print(Map[ParameterNoComma])
                continue
            # Erroneous parameter; raise exception.
            raise Exception(f'Parameter "{Parameter}" is nonsense!')

        CommandData = Opcodes[Op]
        ExpectedParameterCnt = len(CommandData['Args'])
        ActualParameterCnt = len(Parameters)

        if ActualParameterCnt != ExpectedParameterCnt:
            raise Exception(f'Expected {ExpectedParameterCnt} parameters, got {ActualParameterCnt}')
        Offset[0] += 4
        return SyntaxCommand(CommandData['Operation'], CommandData['Condition'] if CondCode == None else CondCode, CommandData['Args'], Parameters)