import mad
from PIL import Image

import sys

image_width = 800
image_height = 100


madfile = mad.MadFile(sys.argv[1])
total_samples = madfile.total_time() / 1000.0 * madfile.samplerate()
buf = madfile.read()
mfoffset = 0

mp3min = 0.0
mp3max = 255.0
mp3range = float(mp3max - mp3min)

image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
x = 0
while x < image_width:
    # what index in the mp3 buffer would this translate to?
    sample_index = int((x / float(image_width)) * total_samples)
    
    # what's the sample value?
    while sample_index - mfoffset >= len(buf):
        buf = madfile.read()
        if buf is None:
            break
        mfoffset += len(buf)

    if buf is None:
        break

    value = ord(buf[sample_index - mfoffset])

    # translate into y pixel coord
    y = int(round((value - mp3min) / mp3range * (image_height-1)))

    # draw
    print "x=%s, y=%s" % (x,y)
    image.putpixel((x, y), (0, 0, 0, 255))

    # iterate
    x += 1

image.save("out.png")
