from xpm import XPM, Color


image = XPM(50, 50)
image.line(3, 5, 45, 49, Color('#FF0000', 'R'))
image.export('line.xpm', autofill=True)
