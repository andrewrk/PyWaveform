import cwaveform

__version__ = '0.3'

def draw(inAudioFile, outImageFile, (imageWidth, imageHeight), bgColor=(0, 0, 0, 0), fgColor=None, fgGradientCenter=None, fgGradientOuter=None, cheat=False):
    """
    Draws the waveform of inAudioFile to picture file outImageFile.
    If a fgColor is specified, the image will be drawn with only that color.
    If fgGradientCenter and fgGradientOuter are specified, a gradient will
        be constructed.
    """
    if fgColor == None:
        fgColor=(0, 0, 0, 255)

    if fgGradientCenter == None or fgGradientOuter == None:
        fgGradientCenter = fgColor
        fgGradientOuter = fgColor

    return cwaveform.draw(inAudioFile, outImageFile, imageWidth, imageHeight,
        bgColor[0], bgColor[1], bgColor[2], bgColor[3],
        fgGradientCenter[0], fgGradientCenter[1], fgGradientCenter[2], fgGradientCenter[3],
        fgGradientOuter[0], fgGradientOuter[1], fgGradientOuter[2], fgGradientOuter[3],
        cheat)
