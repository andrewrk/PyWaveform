from PIL import Image, ImageDraw
import mp3decoder

import sys

image_width = 800
image_height = 100

mp3 = mp3decoder.Mp3Decoder(sys.argv[1])
sample_range = float(mp3.sample_max - mp3.sample_min)
frames_per_pixel = mp3.frame_count / float(image_width)

image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

# for each pixel
x = 0
while x < image_width:
    # range of frames that fit in this pixel
    start = int(x * frames_per_pixel)
    end = int((x+1) * frames_per_pixel)
    
    # get the min and max of this range
    min = mp3.sample_max
    max = mp3.sample_min
    # for each frame from start to end
    i = start
    while i < end:
        frame = mp3.frame(i)
        # average the channels
        value = float(sum(frame)) / len(frame)

        if value < min:
            min = value
        if value > max:
            max = value

        i += 1

    # translate into y pixel coord
    y_min = int(round((min - mp3.sample_min) / sample_range * (image_height-1)))
    y_max = int(round((max - mp3.sample_min) / sample_range * (image_height-1)))

    # draw
    draw.line(((x, y_min), (x, y_max)), (0,0,0,255))

    # iterate
    x += 1

image.save("out.png")


