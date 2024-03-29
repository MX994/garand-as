import yaml
import argparse
from Syntax.Tokenizer import Tokenizer
from Lowering.Garand import Garand

parser = argparse.ArgumentParser()
parser.add_argument('input', help='The input file.')
parser.add_argument('output', help='The output file.')
args = parser.parse_args()

def main():
    ISADefs = None
    CondCodes = None
    # Load ISA operations.
    with open('garand.yml', 'r') as ISADefs_R:
        ISADefs = yaml.safe_load(ISADefs_R)
        ISADefs_R.close()

    # Load Conditional operations.
    with open('garand_cond.yml') as CondCodes_R:
        CondCodes = list(map(lambda x: x.strip(), CondCodes_R.readlines()))
        CondCodes_R.close()
    
    # Load program.
    ProgLines = None
    with open(args.input, 'r') as Prog_R:
        ProgLines = Prog_R.readlines()
        Prog_R.close()

    # Tokenize and lower.
    LoweringHandler = Garand(ISADefs)
    LoweringHandler.LowerNodeList(Tokenizer.Tokenize(ProgLines, ISADefs, CondCodes))
    LoweringHandler.Serialize(args.output)

main()