#!/usr/bin/env python3


# Standard
import os
import sys


# Exception classes
class MaxSizeException(Exception): pass


# Class stores a memory image as a list of bits and handles file parsing
class RomImage:
    data = []
    maxSize = None


    def __init__(self, maxSize = None, path = None):

        # If size was specified
        if maxSize != None:
            self.set_max_size(maxSize)

        # Load from file if apropriate
        if path != None:
            self.load_from_file(path)


    # Set the maximum size for this image
    def set_max_size(self, maxSize):
        self.maxSize = maxSize

        # No need to do anything
        if maxSize == None:
            return

        # If the new max size is smaller than present data
        if maxSize >= 0:
            if maxSize < len(self.data):
                print('WARNING: Image resized from ' + str(len(self.data)) +
                      ' to ' + str(size) + ' bits. Data may be truncated.')
                self.data = self.data[:size]
        else:
            print('ERROR: Invalid image size: ' + str(size))
            sys.exit()


    # Returns true if the given size is valid
    def _fits(self, testSize):
        if self.maxSize is not None:
            if testSize > self.maxSize:
                return False
        return True


    # Expand the data array to a given size
    def _expand_data_array(self, newSize):
        if newSize <= len(self.data):
            return
        if not self._fits(newSize):
            raise MaxSizeException(
                'Failed to expand data array, maximum size reached.')
        self.data += [False] * (i - len(self.data))


    # Append bit to current data
    def append_bit(self, bit):
        if not self._fits(len(self.data) + 1):
            raise MaxSizeException(
                'Failed to append bit to image, maximum size reached.')
        self.data.append(bit)


    # Append byte to current data
    def append_byte(self, byte):
        if not self._fits(len(self.data) + 8):
            raise MaxSizeException(
                'Failed to append byte to image, maximum size reached.')
        for i in range(0, 8):
            bitMask = 0x80 >> i
            if byte & bitMask:
                self.append_bit(True)
            else:
                self.append_bit(False)


    # Set bit at specific position within image
    def set_bit(self, i, bit):
        if not self._fits(i + 1):
            raise MaxSizeException(
                'Failed to set bit in image, maximum size reached.')
        self._expand_data_array(i + 1)
        self.data[i] = bit


    # Set byte at specific position within image
    def set_byte(self, i, byte):
        if not self._fits(i + 8):
            raise MaxSizeException(
                'Failed to set byte in image, maximum size reached.')
        self._expand_data_array(i + 8)
        for j in range(0, 8):
            bitMask = 0x80 >> j
            if byte & bitMask:
                self.set_bit(i + j, True)
            else:
                self.set_bit(i + j, False)


    # Print image contents
    # [TODO] Better implementation with selectable formats might be nice
    def print_all(self):
        print('Image size: ' + str(len(self.data)) + ' Bytes')
        print(self.data)


#====[FILE LOADING]===========================================================//

    # Master load from file
    def load_from_file(self, path):
        try:
            name, ext = os.path.splitext(path)
            if ext.lower() in ['.txt', '']:
                self.init_raw(path)
            elif ext.lower() in ['.hex']:
                self.init_hex(path)
            elif ext.lower() in ['.b64']:
                self.init_b64(path)

            # By default, treat the file as raw, but print out a message
            # to let the user know things may be screwy
            else:
                print("WARNING: '" + ext + "' is not a recognised extension, " +
                      'file will be treated as raw bytes')
                self.init_raw(path, maxBits)

        except MaxSizeException:
            print('WARNING: File exceeds image size, data truncated.')
            return


    # Initialise image directly from file contents
    def init_raw(self, path):
        with open(path, 'rb') as file:
            while True:
                byte = file.read(1)
                if byte == b'':
                    break
                self.append_byte(ord(byte))


    # Initialise from hex file [TODO]
    def init_hex(self, path):
        print('ERROR, hex file parser not yet implemented :(')
        sys.exit()


    # Initialise from base64 encoded file [TODO]
    def init_b64(self, path):
        print('ERROR, b64 file parser not yet implemented :(')
        sys.exit()
