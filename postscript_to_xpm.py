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
parser.add_argument(
    '-wl', '--window-left', type=int,
                            help='Left limit of clipping rectangle')
parser.add_argument(
    '-wt', '--window-top', type=int,
                           help='Top limit of clipping rectangle')
parser.add_argument(
    '-wr', '--window-right', type=int,
                             help='Right limit of clipping rectangle')
parser.add_argument(
    '-wb', '--window-bottom', type=int,
                              help='Bottom limit of clipping rectangle')
parser.add_argument(
    '-t', '--transforms', type=argparse.FileType('r'),
    help='File containing transforms to be applied on input file')
args = parser.parse_args()

# Keep only valid lines from postscript file (the ones ending with LINE),
# remove newline characters, split the valid lines to the 4 coordinates they
# contain, and cast them to integers
lines = [map(int, line.replace('Line\n', '').split())
         for line in list(args.file)
         if line.endswith(' Line\n')]

# Translate line points to the coordinate system used in xpm.py; postscript
# files have the origin in the lower-left corner
for line in lines:
    line[0], line[1] = args.height - line[1], line[0]
    line[2], line[3] = args.height - line[3], line[2]

# Check whether lines need clipping
clipping = (args.window_left and args.window_top and
            args.window_right and args.window_bottom)

image = XPM(args.width, args.height)

# Only perform transforms if transform file is given as input
if args.transforms:
    transforms = [line.split() for line in list(args.transforms)
                  if line.startswith(('t', 'r', 's'))]
    for t in transforms:
        if t[0] == 't':
            image.translate(*map(int, t[1:]))
        elif t[0] == 'r':
            image.rotate(*map(int, t[1:]))
        elif t[0] == 's':
            image.scale(*map(int, t[1:3])+map(float, t[3:5]))

if clipping:
    for line in lines:
        image.clipped_line(*line, xmin=args.window_left,
                                  ymin=args.window_bottom,
                                  xmax=args.window_right,
                                  ymax=args.window_top,
                                  color=Color('#FF0000', 'R'))
else:
    for line in lines:
        image.line(*line, color=Color('#FF0000', 'R'))
image.export(args.output, autofill=True)
