import mad
import struct

class Mp3Decoder:
    """
    This class depends on an mp3 library and provides methods for accessing
    metadata and samples.

    Can only read forwards. You may never access a frame before a frame
    you've already accessed.
    """
    def __init__(self, file):
        self.madfile = mad.MadFile(file)
        # calculations
        self.channel_count = self.madfile.mode()
        self.sample_size = 2
        self.pack_char = "h" # depends on self.sample_size
        self.frame_size = self.sample_size * self.channel_count
        self.byte_count = int(self.madfile.total_time() / 1000.0 * self.madfile.samplerate() * self.frame_size)
        self.frame_count = self.byte_count / self.frame_size

        self.sample_min = -pow(2, 8*self.sample_size-1)+1
        self.sample_max = pow(2, 8*self.sample_size-1)

        self.offset = 0
        self.buf = self.madfile.read()

    def frame(self, index):
        """
        returns a tuple with a value for each channel
        """
        while index * self.frame_size >= self.offset+len(self.buf):
            self.buf = self.madfile.read()
            if self.buf is None:
                return None
            self.offset += len(self.buf)
        frame_offset = index * self.frame_size - self.offset
        return struct.unpack(self.pack_char*self.channel_count, self.buf[frame_offset:frame_offset+self.frame_size])
