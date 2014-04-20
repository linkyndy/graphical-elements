import argparse
from xpm import XPM, Color


# Define command line arguments and parse them
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-f', '--file',
    type=argparse.FileType('r'), help='Input file (with .pol extension)')
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
    '-wl', '--window-left',
    type=int, help='Left limit of clipping rectangle')
parser.add_argument(
    '-wt', '--window-top',
    type=int, help='Top limit of clipping rectangle')
parser.add_argument(
    '-wr', '--window-right',
    type=int, help='Right limit of clipping rectangle')
parser.add_argument(
    '-wb', '--window-bottom',
    type=int, help='Bottom limit of clipping rectangle')
args = parser.parse_args()

# Vertices are stored one per line in a .pol file, with x and y coords
# separated by a space
vertices = [map(int, line.replace('\n', '').split())
            for line in list(args.file)]

# Check whether lines need clipping
clipping = (args.window_left and args.window_top and
            args.window_right and args.window_bottom)

image = XPM(args.width, args.height)
image.complex_poly(
    vertices=vertices,
    color=Color('#FF0000', 'R'),
    clip=(args.window_left, args.window_bottom,
          args.window_right, args.window_top) if clipping else None)
image.export(args.output, autofill=True)
