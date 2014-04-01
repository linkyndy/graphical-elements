from xpm import XPM, Color


image = XPM(10, 10)
image.complex_line(0, 0, 9, 9, clip=(4, 4, 6, 6), color=Color('#FF0000', 'R'))
image.export('clipped_line.xpm', autofill=True)
