from xpm import XPM, Color

image = XPM(50, 50)
image.poly(Color('#FF0000', 'R'), 5, 8, 10, 25, 40, 26, 32, 10)
image.export('poly.xpm', autofill=True)
