import mad
from PIL import Image, ImageDraw
import struct

import sys

image_width = 800
image_height = 100

madfile = mad.MadFile(sys.argv[1])

# load the entire thing into memory
bytes = ""
while True:
    buf = madfile.read()
    if buf is None:
        break
    for i in range(len(buf)):
        bytes += buf[i]

print "done loading"

channel_count = madfile.mode()
sample_size = 2
frame_size = sample_size * channel_count
byte_count = len(bytes)
frame_count = byte_count / frame_size
#byte_count = frame_count * frame_size

sample_min = -pow(2, 8*sample_size-1)+1
sample_max = pow(2, 8*sample_size-1)
sample_range = float(sample_max - sample_min)

frames_per_pixel = frame_count / float(image_width)

image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

# for each pixel
x = 0
while x < image_width:
    # range of frames that fit in this pixel
    start = int(x * frames_per_pixel)
    end = int((x+1) * frames_per_pixel)
    
    # get the min and max of this range
    min = sample_max
    max = sample_min
    # for each frame from start to end
    i = start
    while i < end:
        offset = i * frame_size
        lvalue = struct.unpack("h", bytes[offset:offset+sample_size])[0]
        offset += sample_size
        rvalue = struct.unpack("h", bytes[offset:offset+sample_size])[0]
        value = (lvalue + rvalue) / 2.0

        if value < min:
            min = value
        if value > max:
            max = value

        i += 1

    # translate into y pixel coord
    y_min = int(round((min - sample_min) / sample_range * (image_height-1)))
    y_max = int(round((max - sample_min) / sample_range * (image_height-1)))

    # draw
    draw.line(((x, y_min), (x, y_max)), (0,0,0,255))

    # iterate
    x += 1

image.save("out.png")


