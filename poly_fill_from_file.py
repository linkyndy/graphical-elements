import argparse
from xpm import XPM, Color


# Define command line arguments and parse them
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-f', '--file',
    type=argparse.FileType('r'), help='Input file (of .pol extension)')
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
    '-r', '--red',
    type=int, help='Red component of fill color')
parser.add_argument(
    '-g', '--green',
    type=int, help='Green component of fill color')
parser.add_argument(
    '-b', '--blue',
    type=int, help='Blue component of fill color')
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
parser.add_argument(
    '-vl', '--viewport-left',
    type=int, default=0, help='Left limit of viewport rectangle')
parser.add_argument(
    '-vt', '--viewport-top',
    type=int, default=0, help='Top limit of viewport rectangle')
parser.add_argument(
    '-vr', '--viewport-right',
    type=int, help='Right limit of viewport rectangle')
parser.add_argument(
    '-vb', '--viewport-bottom',
    type=int, help='Bottom limit of viewport rectangle')
args = parser.parse_args()

# Vertices are stored one per line in a .pol file, with x and y coords
# separated by a space
vertices = [map(int, line.replace('\n', '').split())
            for line in list(args.file)]

# Compute HEX value for given RGB color
color = Color('#%02x%02x%02x' % (args.red, args.green, args.blue), 'C')

# Check whether poly needs clipping
clipping = (args.window_left and args.window_top and
            args.window_right and args.window_bottom)

# Set defaults for remaining viewport args
args.viewport_right = args.viewport_right or args.width-1
args.viewport_bottom = args.viewport_bottom or args.height-1

# Compute viewport scale factors
x_factor = 1.*(args.viewport_bottom-args.viewport_top)/(args.window_bottom-args.window_top)
y_factor = 1.*(args.viewport_right-args.viewport_left)/(args.window_right-args.window_left)

image = XPM(args.width, args.height)
image.scale(args.viewport_top, args.viewport_left, x_factor, y_factor)
image.complex_poly(
    vertices=vertices,
    color=color,
    fill=color,
    clip=(args.window_left, args.window_bottom,
          args.window_right, args.window_top) if clipping else None)
image.export(args.output, autofill=True)
