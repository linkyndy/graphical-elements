import string
from xpm import XPM, Color


NOF_COLORS = 50
STEP = 255 / NOF_COLORS

image = XPM(50, 50)

for i in range(50):
    for j in range(50):
        image.set(i, j, Color('#%02x0000' % (j * STEP,), string.letters[j]))

image.export('gradient.xpm')
