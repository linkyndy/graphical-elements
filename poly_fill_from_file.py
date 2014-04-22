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
args = parser.parse_args()

# Vertices are stored one per line in a .pol file, with x and y coords
# separated by a space
vertices = [map(int, line.replace('\n', '').split())
            for line in list(args.file)]

# Compute HEX value for given RGB color
color = Color('#%02x%02x%02x' % (args.red, args.green, args.blue), 'C')

image = XPM(args.width, args.height)
image.poly(
    vertices=vertices,
    color=color,
    fill=color)
image.export(args.output, autofill=True)
