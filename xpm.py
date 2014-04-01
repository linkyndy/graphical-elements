from math import pi, sin, cos


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

    def __eq__(self, other):
        if isinstance(other, Color):
            return (self.code == other.code) and (self.chars == other.chars)
        return False

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return '<%s for %s>' % (self.chars, self.code)


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
        self.transforms = Matrix.identity(3)

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

    def autofill(self, color=Color('#FFFFFF', '_')):
        """
        Fill unset pixels so that image can be exported
        """

        for x in range(self.height):
            for y in range(self.width):
                if not self.pixels[x][y]:
                    self.set(x, y, color)

    def export(self, path, autofill=False):
        """
        Export image to path.xpm file
        """

        if autofill:
            self.autofill()

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

    def line(self, x1, y1, x2, y2, color):
        """
        Draws a colored line from (x1, y1) to (x2, y2) after applying
        transforms, if any are defined for the image
        """

        if self.transforms:
            x1, y1 = self._apply_transforms(x1, y1)
            x2, y2 = self._apply_transforms(x2, y2)

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        error = dx - dy

        x = x1
        y = y1

        while(True):
            self.set(x, y, color)

            if x == x2 and y == y2:
                break

            error_double = 2 * error
            if error_double > -dy:
                error -= dy
                x += sx
            if error_double < dx:
                error += dx
                y += sy

    def clipped_line(self, x1, y1, x2, y2, xmin, ymin, xmax, ymax, color):
        """
        Draws a colored line from (x1, y1) to (x2, y2), clipping it to a
        rectangle having its diagonal from (xmin, ymin) to (xmax, ymax). If
        clipping can not occur, None is returned
        """

        def compute_outcode(x, y):
            outcode = 0
            if x < xmin:
                # To the left of clip window (bin(1) == 0001)
                outcode |= 1
            elif x > xmax:
                # To the right of clip window (bin(2) == 0010)
                outcode |= 2
            if y < ymin:
                # Below the clip window (bin(4) == 0100)
                outcode |= 4
            elif y > ymax:
                # Above the clip window (bin(8) == 1000)
                outcode |= 8
            return outcode

        outcode1 = compute_outcode(x1, y1)
        outcode2 = compute_outcode(x2, y2)
        while(True):
            if outcode1 | outcode2 == 0:
                return self.line(x1, y1, x2, y2, color)
            elif outcode1 & outcode2 != 0:
                return None

            outcodeout = outcode1 or outcode2
            if outcodeout & 8:
                x, y = x1 + (x2-x1) * (ymax-y1) / (y2-y1), ymax
            elif outcodeout & 4:
                x, y = x1 + (x2-x1) * (ymin-y1) / (y2-y1), ymin
            elif outcodeout & 2:
                x, y = xmax, y1 + (y2-y1) * (xmax-x1) / (x2-x1)
            elif outcodeout & 1:
                x, y = xmin, y1 + (y2-y1) * (xmin-x1) / (x2-x1)

            if outcodeout == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2)
        return self.line(x1, y1, x2, y2, color)

    def translate(self, x, y):
        """
        Creates a transform matrix for translating a point to (x, y)
        """

        self.transforms *= Matrix([[1, 0, x],
                                   [0, 1, y],
                                   [0, 0, 1]])

    def rotate(self, x, y, angle):
        """
        Creates a transform matrix for rotating a point by given angle (in
        degrees) around point (x, y)
        It translates to/from the given point before/after rotation
        """

        radians = angle*pi/100

        self.translate(x, y)
        self.transforms *= Matrix([[cos(radians), -sin(radians), 0],
                                   [sin(radians), cos(radians), 0],
                                   [0, 0, 1]])
        self.translate(-x, -y)

    def scale(self, x, y, xfactor, yfactor):
        """
        Creates a transform matrix for scaling a point by given factors
        around point (x, y)
        It translates to/from the given point before/after scaling
        """

        self.translate(x, y)
        self.transforms *= Matrix([[xfactor, 0, 0],
                                   [0, yfactor, 0],
                                   [0, 0, 1]])
        self.translate(-x, -y)

    def _apply_transforms(self, x, y):
        """
        Applies transforms defined for image on point (x, y), returning the
        new transformed point's coordinates, converted to integers
        """

        point = Matrix([[x,], [y,], [1,]])
        transformed_point = self.transforms * point
        return int(transformed_point[0][0]), int(transformed_point[1][0])

    def reset_transforms(self):
        self.transforms = Matrix.identity(3)


class Matrix(object):
    def __init__(self, elements):
        # try:
        #     print elements
        #     print set(elements)
        #     if len(set(elements)) != 1:
        #         raise ValueError('Matrix is invalid')
        # except TypeError:
        #     raise TypeError('Matrix must be provided as a tuple')
        self.elements = elements
        self.height = len(elements)
        self.width = len(elements[0])

    def __getitem__(self, key):
        return self.elements[key]

    def __eq__(self, other):
        return self.elements == other.elements

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        """
        Identity matrices are evaluated as False
        """

        return self.width != self.height or self != self.identity(self.width)

    def __mul__(self, other):
        if self.width != other.height:
            raise ValueError('Matrices\'s size is invalid for multiplication')

        result = Matrix.null(self.height, other.width)
        for i in range(self.height):
            for j in range(other.width):
                for k in range(self.width):
                    result[i][j] += self[i][k] * other[k][j]
        return result

    def __imul__(self, other):
        if self.width != other.height:
            raise ValueError('Matrices\'s size is invalid for multiplication')

        result = Matrix.null(self.height, other.width)
        for i in range(self.height):
            for j in range(other.width):
                for k in range(self.width):
                    result[i][j] += self[i][k] * other[k][j]
        self.elements = result.elements
        return self

    @classmethod
    def null(cls, height, width):
        """
        Returns a null matrix, of given size
        """

        return cls([[0 for _ in range(width)] for _ in range(height)])

    @classmethod
    def identity(cls, size):
        """
        Returns an identity matrix, of given size
        """

        return cls(
            [[1 if i==j else 0 for j in range(size)] for i in range(size)])

