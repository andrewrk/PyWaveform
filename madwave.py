import mad
import struct
from PIL import Image, ImageDraw
import mp3decoder

import sys

image_width = 800
image_height = 100

madfile = mad.MadFile(sys.argv[1])
# calculations
channel_count = madfile.mode()
sample_size = 2
pack_char = "h" # depends on sample_size
frame_size = sample_size * channel_count
byte_count = int(madfile.total_time() / 1000.0 * madfile.samplerate() * frame_size)
frame_count = byte_count / frame_size

sample_min = -pow(2, 8*sample_size-1)+1
sample_max = pow(2, 8*sample_size-1)

mfoffset = 0
buf = madfile.read()
sample_range = float(sample_max - sample_min)
frames_per_pixel = frame_count / float(image_width)
frames_per_pixel_int = int(frames_per_pixel)

image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

image_height_m1 = image_height - 1

cheat = 500

# for each pixel
x = 0
while x < image_width:
    # range of frames that fit in this pixel
    start = int(x * frames_per_pixel)
    #end = start+frames_per_pixel_int
    end = start+cheat
    
    # get the min and max of this range
    min = sample_max
    max = sample_min
    # for each frame from start to end
    i = start
    while i < end:
        tmp_offset = i * frame_size
        while tmp_offset >= mfoffset + len(buf):
            buf = madfile.read()
            if buf is None:
                break
            mfoffset += len(buf)
        if buf is None:
            break

        offset = tmp_offset - mfoffset
        vals = struct.unpack("hh", buf[offset:offset+frame_size])
        # average the channels
        value = (vals[0] + vals[1]) / 2

        if value < min:
            min = value
        if value > max:
            max = value

        i += 1

    if buf is None:
        break

    # translate into y pixel coord
    y_min = int((min - sample_min) / sample_range * image_height_m1)
    y_max = int((max - sample_min) / sample_range * image_height_m1)

    # draw
    draw.line(((x, y_min), (x, y_max)), (0,0,0,255))

    # iterate
    x += 1

image.save("out.png")


