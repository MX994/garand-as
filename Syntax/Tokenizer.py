from Syntax.SyntaxNodes import *
from struct import pack
import sys

class Tokenizer:
    @staticmethod
    def Tokenize(Data: list[str], Opcodes : dict, Conditions):
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
        # Post processing: Compute the label address
        ScanNode = Head
        while ScanNode != None:
            if isinstance(ScanNode, SyntaxCommand):
                data: Command = ScanNode.GetData()
                NewParam = []
                for p in data.GetParameters():
                    if isinstance(p, Label):
                        p: Label
                        print("Updating label", p.GetName())
                        NewParam.append(LabelOffsetMap[p.GetName()] - p.GetRelative())
                    else:
                        NewParam.append(p)
                ScanNode.GetData().Parameters = NewParam
            ScanNode = ScanNode.GetNext()
        return Head
    
    @staticmethod
    # Naively tokenize string.
    def TokenizeLine(String: str, Opcodes : dict, Conditions, Labels, Offset, Map):
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
            if PossibleTokens[1] in Map.keys():
                raise Exception(f'Label "{PossibleTokens[1]}" already defined!')
            Node = SyntaxLabel(PossibleTokens[1])
            Labels.append(Node.GetData())
            Map[Node.GetData().GetName()] = Offset[0]
            return SyntaxLabel(PossibleTokens[1])
        if PossibleTokens[0] == '.byte':
            # Raw byte
            if PossibleTokens[1][1:].isnumeric():
                # Immediate syntax
                return SyntaxRaw(pack('B', int(PossibleTokens[1][1:])))
            elif PossibleTokens[1][0:2] == '0x':
                # hex
                return SyntaxRaw(pack('B', int(PossibleTokens[1], 16)))
            raise Exception('Invalid literal for raw directive.')
        if PossibleTokens[0] == '.hword':
            # Raw byte
            if PossibleTokens[1][1:].isnumeric():
                # Immediate syntax
                return SyntaxRaw(pack('H', int(PossibleTokens[1][1:])))
            elif PossibleTokens[1][0:2] == '0x':
                # hex
                return SyntaxRaw(pack('H', int(PossibleTokens[1], 16)))
            raise Exception('Invalid literal for raw directive.')
        if PossibleTokens[0] == '.word':
            # Raw byte
            if PossibleTokens[1][1:].isnumeric():
                # Immediate syntax
                return SyntaxRaw(pack('I', int(PossibleTokens[1][1:])))
            elif PossibleTokens[1][0:2] == '0x':
                # hex
                return SyntaxRaw(pack('I', int(PossibleTokens[1], 16)))
            raise Exception('Invalid literal for raw directive.')
        if PossibleTokens[0] == '.incbin':
            if len(PossibleTokens) != 3:
                raise Exception('Need to specify all three parameters for incbin!')
            with open(PossibleTokens[1].strip("'"), 'rb') as RAWBuf:
                if PossibleTokens[2][1:].isnumeric():
                    return SyntaxRaw(RAWBuf.read(), int(PossibleTokens[2], 10))
                elif PossibleTokens[2][0:2] == '0x':
                    return SyntaxRaw(RAWBuf.read(), int(PossibleTokens[2], 16))
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
            else:
                if Op == 'B':
                    Parameters.append(Label(ParameterNoComma, Offset[0]))
                else:
                    Parameters.append(Label(ParameterNoComma))
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
