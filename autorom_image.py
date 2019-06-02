#!/usr/bin/env python3


# Standard
import os
import sys


# Class stores a ROM image as a sequence of bytes
# Also handles input file parsing
class rom_image:
    data = bytearray()


    # Fill with data from arbitrary file
    def __init__(self, path, romSize):
        name, ext = os.path.splitext(path)
        if ext.lower() == '':       self.init_raw(path, romSize)
        elif ext.lower() == '.txt': self.init_raw(path, romSize)
        elif ext.lower() == '.hex': self.init_hex(path, romSize)
        elif ext.lower() == '.b64': self.init_b64(path, romSize)

        # By default, treat the file as raw
        else:
            print("WARNING: '" + ext + "' is not a recognised extension, ", end = '')
            print('file will be treated as raw bytes')
            self.init_raw(path, romSize)

        # Pad to rom size
        self.__pad(romSize)


    # Print the contents of the image
    def print_all(self):
        print('Image size: ' + str(len(self.data)) + ' Bytes')
        print(self.data)


    # Add padding bytes
    def __pad(self, romSize):
        while len(self.data) < romSize:
            self.data.append(0x00)


    # Initialise image directly from file contents
    def init_raw(self, path, romSize):
        with open(path, 'rb') as file:
            while True:
                byte = file.read(1)
                if byte != b'':
                    if len(self.data) < romSize:
                        self.data.append(ord(byte))
                    else:
                        print("WARNING: file '" + path + "' ", end = '')
                        print('exceeds rom capacity, file truncated')
                        break
                else:
                    break


    # Initialise from hex file [TODO]
    def init_hex(self, path, romSize):
        print('ERROR, hex file parser not yet implemented :(')
        sys.exit()


    # Initialise from base64 encoded file [TODO]
    def init_b64(self, path, romSize):
        print('ERROR, b64 file parser not yet implemented :(')
        sys.exit()
