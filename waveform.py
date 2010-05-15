import cwaveform

def draw(inAudioFile, outImageFile, (imageWidth, imageHeight), bgColor=(0, 0, 0, 0), fgColor=(0, 0, 0, 255), cheat=False):
    return cwaveform.draw(inAudioFile, outImageFile, imageWidth, imageHeight,
        bgColor[0], bgColor[1], bgColor[2], bgColor[3],
        fgColor[0], fgColor[1], fgColor[2], fgColor[3],
        cheat)
