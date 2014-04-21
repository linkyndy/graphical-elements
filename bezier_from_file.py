import argparse
from xpm import XPM, Color


# Define command line arguments and parse them
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-i', '--file',
    type=argparse.FileType('r'), help='Input file (of .bze extension)')
parser.add_argument(
    '-w', '--width',
    type=int, help='Width of XPM image')
parser.add_argument(
    '-h', '--height',
    type=int, help='Height of XPM image')
parser.add_argument(
    '-o', '--output',
    help='Output file (of XPM type)')
parser.add_argument(
    '-p', '--step',
    type=float, help='Step for drawing Bezier curves')
args = parser.parse_args()

# Keep only valid lines from input file (the ones ending with Point),
# remove newline characters, split the valid lines to the 2 coordinates they
# contain, and cast them to integers
points = [map(int, line.replace('Point\n', '').replace(' Point \n', '').split())
         for line in list(args.file)
         if line.endswith((' Point\n', ' Point \n'))]

image = XPM(args.width, args.height)
image.bezier(
    points=points,
    step=args.step,
    color=Color('#FF0000', 'R'))
image.export(args.output, autofill=True)
