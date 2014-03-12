IMAGE = '/* XPM */\n' \
        'static char *egc[] = {{\n\n' \
        '/* width,height,nrcolors,charsperpixel */\n' \
        '" {width} {height} {nof_colors} {cpp} ",\n\n' \
        '/* colors #RRGGBB */\n' \
        '{colors},\n\n' \
        '/* pixels */\n' \
        '{pixels}\n' \
        '}};'

COLORS = '"{chars} c {code}"'

PIXELS = '"{pixels}"'


class Color(object):
    def __init__(self, code, chars):
        """
        Initializes a color object by setting the color code (in the format
        '#RRGGBB') and the character representation of the color
        """

        self.code = code
        self.chars = chars


class XPM(object):
    def __init__(self, width, height):
        """
        Initializes an XPM image with given width and height
        """

        self.width = width
        self.height = height
        self.cpp = None
        self.colors = set()
        self.pixels = [[None for _ in range(width)] for _ in range(height)]

    def set(self, x, y, color):
        """
        Assign pixel (x,y) a color;
        """

        if not isinstance(color, Color):
            raise TypeError('Supplied color must be a Color object')

        if not self.cpp:
            self.cpp = len(color.chars)
        elif len(color.chars) != self.cpp:
            raise ValueError('Length of character representation of the '
                             'supplied color must match the one of colors '
                             'added to the image, which is %s' % self.cpp)

        self.colors.add(color)
        self.pixels[x][y] = color

    def export(self, path):
        """
        Export image to path.xpm file
        """

        for x in self.pixels:
            if None in x:
                raise Exception('Cannot export image with undefined pixels')

        colors = ",\n".join(
            [COLORS.format(chars=color.chars,
                           code=color.code) for color in self.colors])
        pixels = ",\n".join(
            [PIXELS.format(pixels="".join(
                [c.chars for c in pixel_line])) for pixel_line in self.pixels])
        image = IMAGE.format(width=self.width,
                             height=self.height,
                             nof_colors=len(self.colors),
                             cpp=self.cpp,
                             colors=colors,
                             pixels=pixels)

        with open(path, 'w') as f:
            f.write(image)
