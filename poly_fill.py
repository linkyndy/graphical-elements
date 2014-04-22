from xpm import XPM, Color


image = XPM(50, 50)
image.poly(
    vertices=[[5, 8], [10, 25], [40, 26], [32, 10]],
    color=Color('#FF0000', 'R'),
    fill=Color('#FF0000', 'R'))
image.export('poly_fill.xpm', autofill=True)
