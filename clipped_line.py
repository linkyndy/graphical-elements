from xpm import XPM, Color


image = XPM(10, 10)
image.clipped_line(0, 0, 9, 9, 4, 4, 6, 6, Color('#FF0000', 'R'))
image.export('clipped_line.xpm', autofill=True)
