from xpm import XPM, Color


image = XPM(50, 50)
image.bezier(
    points=[[2, 2], [10, 30], [30, 20], [45, 45]],
    step=0.02,
    color=Color('#FF0000', 'R'))
image.export('bezier.xpm', autofill=True)
