#!/usr/bin/env python3


# Standard
import os
import sys
import json


# This project
import autorom_image as rom_image
import autorom_util as util
import autorom_b2j as b2j


# Board registry info
__BOARD_DIR = os.path.dirname(__file__) + '/boards'
__BOARD_REGISTRY_PATH = __BOARD_DIR + '/board-registry.json'
__BOARD_REGISTRY = json.loads(open(__BOARD_REGISTRY_PATH, 'r').read())


# Get list of all board IDs
def get_board_ids():
    idList = []
    for key in __BOARD_REGISTRY:
        idList.append(key)
    return idList


# Get ROM path from ID
def get_path(id):
    return __BOARD_DIR + '/' + __BOARD_REGISTRY[id]['path']


# Get ROM capacity from ID
def get_capacity(id):
    return __BOARD_REGISTRY[id]['capacity']


# Print contents of board registry
# Could use a more friendly output [TODO]
def print_all():
    print('List of available ROM boards:')
    for key in __BOARD_REGISTRY:
        print(key, end = ': ')
        print(__BOARD_REGISTRY[key])


# Class serves as interface for modifying board contents
class tung_rom_board:
    data = None
    capacity = None
    romID = None


    # Initialise
    def __init__(self, romID):
        self.romID = romID
        self.capacity = get_capacity(romID)

        # Convert board to JSON and load
        boardPath = get_path(romID)
        jsonPath, junk = os.path.splitext(boardPath)
        jsonPath += '.json'
        b2j.board_to_json(boardPath, jsonPath)
        self.data = json.loads(open(jsonPath, 'r').read())

        # Select set_bit method for given ROM
        setBitMethodName = 'set_bit_json_' + romID
        try:
            setattr(self, 'set_bit_json', getattr(self, setBitMethodName))
        except:
            print("ERROR: Failed to find set_bit implementation for " + romID)
            sys.exit(1)


    # Load image
    def load_image(self, image):
        self.set_byte(0, 0x81)


    # Set byte
    def set_byte(self, index, value):
        bitMask = 0x80
        for i in range(0, 8):
            bitMask = 0x80 >> i
            if value & bitMask != 0:
                self.set_bit((index * 8) + i)


    # Set bit
    def set_bit(self, index):
        if index < self.capacity * 8:
            self.set_bit_json(index)
        else:
            print('WARNING: Bit ' + str(index) + ' out of range')


    # Save ROM to output file
    def save_tungboard(self, path):
        with open(path, 'w') as file:
            file.write("I'm not a tung board!")



#====[SET BIT IMPLEMENTATIONS HERE]===========================================//

    # Set bit
    def set_bit_json_matrix_rom_16x16(self, index):
        print('WARNING: set_bit_json_matrix_rom_16x16 not yet implemented!')
