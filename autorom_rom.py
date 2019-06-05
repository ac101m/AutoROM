#!/usr/bin/env python3


# Standard
import os
import sys
import json
import copy


# This project
import autorom_image as rom_image
import autorom_util as util
import autorom_b2j as b2j


# Board registry info
__BOARD_DIR = os.path.dirname(__file__) + '/boards'
__BOARD_REGISTRY_PATH = __BOARD_DIR + '/board-registry.json'
__BOARD_REGISTRY = json.loads(open(__BOARD_REGISTRY_PATH, 'r').read())


# Exception classes
class MaxSizeException(Exception): pass


# Get board path from ID
def get_board_path(boardID):
    return __BOARD_DIR + '/' + __BOARD_REGISTRY[boardID]['path']


# Get json board path from ID
def get_json_path(boardID):
    return __BOARD_DIR + '/' + __BOARD_REGISTRY[boardID]['path'] + '.json'


# Get list of all board IDs
def get_board_ids():
    idList = []
    for key in __BOARD_REGISTRY:
        idList.append(key)
    return idList


# Get ROM capacity from ID
def get_capacity(boardID):
    return __BOARD_REGISTRY[boardID]['capacity']


# Print contents of board registry
# Could use a more friendly output [TODO]
def print_all():
    print('List of available ROM boards:')
    for key in __BOARD_REGISTRY:
        print(key, end = ': ')
        print(__BOARD_REGISTRY[key])


# Class serves as interface for modifying board contents
class tung_rom_board:
    jsonPath = None
    boardPath = None
    baseJsonData = None
    capacity = None
    boardID = None


    # Initialise
    def __init__(self, boardID):
        self.boardID = boardID
        self.capacity = get_capacity(boardID)

        # Convert board to JSON and load
        self.boardPath = get_board_path(boardID)
        self.jsonPath = get_json_path(boardID)
        b2j.board_to_json(self.boardPath, self.jsonPath)
        self.baseJsonData = json.loads(open(self.jsonPath, 'rb').read())

        # Select set_bit method for given ROM
        setBitMethodName = 'set_bit_' + boardID
        try:
            setattr(self, 'set_bit_boardID', getattr(self, setBitMethodName))
        except:
            print("ERROR: Couldn't find set_bit implementation for " + boardID)
            sys.exit()


    # Load bits from image
    def _encode_json_data(self, image):
        jsonData = copy.deepcopy(self.baseJsonData)
        try:
            for i, bit in enumerate(image.data):
                if bit:
                    self._set_bit(jsonData, i)
        except Exception as e:
            print('WARNING: Image exceeds ROM size, image data truncated.')
        return jsonData


    # Set single bit
    def _set_bit(self, index, jsonData):
        if index < self.capacity:
            self.set_bit_boardID(index)
        else:
            raise MaxSizeException(
                'Failed to set bit, bit index out of range.')


    # Encode board and dump to file
    def encode(self, outputPath, image):

        # Encode json data with image
        jsonData = self._encode_json_data(image)

        # Write new json data to temporary
        tmpJsonPath = get_board_path(self.boardID) + '.tmp.json'
        with open(tmpJsonPath, 'w') as file:
            file.write(json.dumps(jsonData))

        # Convert back to tungboard
        b2j.json_to_board(tmpJsonPath, outputPath)
        os.remove(tmpJsonPath)


#====[BOARD SPECIFIC SET_BIT IMPLEMENTATIONS HERE]============================//

    # Set bit for 16 by 16 matrix ROM
    def set_bit_matrix_rom_16x16(self, index, jsonData):
        print('WARNING: set_bit_matrix_rom_16x16 not yet implemented!')
