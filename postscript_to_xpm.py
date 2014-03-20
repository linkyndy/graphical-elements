import argparse
from xpm import XPM, Color

# Define command line arguments and parse them
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-f', '--file', type=argparse.FileType('r'),
                    help='Input file (of simplified Postscript type)')
parser.add_argument('-w', '--width', type=int, help='Width of XPM image')
parser.add_argument('-h', '--height', type=int, help='Height of XPM image')
parser.add_argument('-o', '--output', help='Output file (of XPM type)')
args = parser.parse_args()

# Keep only valid lines from postscript file (the ones ending with LINE),
# remove newline characters, split the valid lines to the 4 coordinates they
# contain, and cast them to integers
lines = [map(int, line.replace('Line\n', '').split())
         for line in list(args.file)
         if line.endswith(' Line\n')]

image = XPM(args.width, args.height)
for line in lines:
    image.line(*line, color=Color('#FF0000', 'R'))
image.export(args.output, autofill=True)
