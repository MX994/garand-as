from PIL import Image
import argparse
from struct import pack

parser = argparse.ArgumentParser()
parser.add_argument('input', help='The input file.')
parser.add_argument('output', help='The output file.')
args = parser.parse_args()

def main():
    # Remove alpha channel and flatten to RGB byte buffer.
    with open(args.output, 'wb') as GarandFmtImg:
        Buffer = Image.open(args.input).convert('RGBA').tobytes()
        for x in range(len(Buffer)):
            if x % 4 == 0:
                GarandFmtImg.write(pack('B', Buffer[x + 2]))
            elif x % 4 == 2:
                GarandFmtImg.write(pack('B', Buffer[x - 2]))
            else:
                GarandFmtImg.write(pack('B', Buffer[x]))
        # GarandFmtImg.write(Image.open(args.input).convert('RGBA').tobytes())
main()