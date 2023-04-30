from Syntax.SyntaxNodes import *
import sys

class Tokenizer:
    @staticmethod
    def Tokenize(Data, Opcodes : dict):
        Head = None
        Curr = None
        LineNo = 1
        for Line in Data:
            try:
                NewNode = Tokenizer.TokenizeLine(Line, Opcodes)
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
    def TokenizeLine(String, Opcodes : dict):
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
            return SyntaxLabel(PossibleTokens[1])
        
        # Likely a command. Try to parse it.     
        CommandNames = list(Opcodes.keys())
        
        if PossibleTokens[0] not in CommandNames:
            raise Exception(f'Command name "{PossibleTokens[0]}" is nonsense!')
        
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
            # Erroneous parameter; raise exception.
            raise Exception(f'Parameter "{Parameter}" is nonsense!')

        CommandData = Opcodes[PossibleTokens[0]]

        ExpectedParameterCnt = len(CommandData['Args'])
        ActualParameterCnt = len(Parameters)

        if ActualParameterCnt != ExpectedParameterCnt:
            raise Exception(f'Expected {ExpectedParameterCnt} parameters, got {ActualParameterCnt}')

        return SyntaxCommand(CommandData['Operation'], CommandData['Condition'], CommandData['Args'], Parameters)