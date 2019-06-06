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
__BOARD_REGISTRY = {}


# Exception classes
class MaxSizeException(Exception): pass


# Clean all board json files from the board directory
def clean():
    for id in get_board_ids():
        try:
            os.remove(get_json_path(id))
            print('Cleaned ' + get_json_path(id))
        except FileNotFoundError:
            pass


# Get board path from ID
def get_board_path(boardID):
    return __BOARD_DIR + '/' + __BOARD_REGISTRY[boardID]['path']


# Get json board path from ID
def get_json_path(boardID):
    return get_board_path(boardID) + '.json'


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


# Get the md5 hash from the board registry, returns None if not found
def get_registry_md5(boardID):
    try:
        return __BOARD_REGISTRY[boardID].get('md5', None)
    except KeyError:
        print("ERROR: Board registry error, No such board: '" + boardID + "'.")
        sys.exit()


# Update board md5 hash in the board registry
def update_registry_md5(boardID, md5Sum):
    try:
        __BOARD_REGISTRY[boardID]['md5'] = md5Sum
    except KeyError:
        print("ERROR: Board registry error, No such board: '" + boardID + "'.")
        sys.exit()
    with open(__BOARD_REGISTRY_PATH, 'w') as file:
        file.write(json.dumps(__BOARD_REGISTRY, indent = 2))


# Attempt to load the board registry
try:
    __BOARD_REGISTRY = json.loads(open(__BOARD_REGISTRY_PATH, 'rb').read())
except FileNotFoundError:
    print("ERROR: Board registry not found. Nothing to be done.")
    sys.exit()


# Class serves as interface for modifying board contents
class TungRomEncoder:
    jsonPath = None
    boardPath = None
    baseJsonData = None
    capacity = None
    boardID = None


    # Initialise
    def __init__(self, boardID):
        self.boardID = boardID
        self.capacity = get_capacity(boardID)
        self.boardPath = get_board_path(boardID)
        self.jsonPath = get_json_path(boardID)

        # Convert to json (lazily, check md5 sum first)
        md5Sum = util.md5_hex_digest(self.boardPath)
        if os.path.isfile(self.jsonPath):
            if get_registry_md5(boardID) != md5Sum:
                b2j.board_to_json(self.boardPath, self.jsonPath)
                update_registry_md5(boardID, md5Sum)
        else:
            b2j.board_to_json(self.boardPath, self.jsonPath)
            update_registry_md5(boardID, md5Sum)

        # Load data from the
        self.baseJsonData = json.loads(open(self.jsonPath, 'r').read())

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
                    self._set_bit(i, jsonData)
        except MaxSizeException:
            print('WARNING: Image exceeds ROM size, image data truncated.')
        return jsonData


    # Set single bit
    def _set_bit(self, i, jsonData):
        if i < self.capacity:
            self.set_bit_boardID(i, jsonData)
        else:
            raise MaxSizeException(
                'Failed to set bit, bit index out of range.')


    # Encode board and dump to file
    def encode(self, outputPath, image):

        # Encode json data with image
        jsonData = self._encode_json_data(image)

        # Write new json data to temporary
        tmpJsonPath = outputPath + '.json'
        with open(tmpJsonPath, 'w') as file:
            file.write(json.dumps(jsonData))

        # Convert back to tungboard
        b2j.json_to_board(tmpJsonPath, outputPath)
        os.remove(tmpJsonPath)


#====[BOARD SPECIFIC SET_BIT IMPLEMENTATIONS HERE]============================//

    # Set bit for 16 by 16 matrix ROM
    def set_bit_matrix_rom_16x16(self, i, jsonData):
        print('WARNING: set_bit_matrix_rom_16x16 not yet implemented!')
