
# Standard
import os
import json
import copy


# This project
import rom.registry as RomRegistry
import util.b2j as b2j
import util.misc as util


# Exception classes
class MaxSizeException(Exception): pass


# Class serves as interface for modifying board contents
class TungRomEncoder:
    jsonPath = None
    boardPath = None
    baseJsonData = None
    capacity = None
    boardID = None
    boardModule = None


    # Initialise
    def __init__(self, boardID):
        self.boardID = boardID
        self.capacity = RomRegistry.get_capacity(boardID)
        self.boardPath = RomRegistry.get_board_path(boardID)
        self.jsonPath = RomRegistry.get_json_path(boardID)

        # Convert to json (lazily, check md5 sum first)
        md5Sum = util.md5_hex_digest(self.boardPath)
        if os.path.isfile(self.jsonPath):
            if RomRegistry.get_registry_md5(boardID) != md5Sum:
                b2j.board_to_json(self.boardPath, self.jsonPath)
                RomRegistry.update_registry_md5(boardID, md5Sum)
        else:
            b2j.board_to_json(self.boardPath, self.jsonPath)
            RomRegistry.update_registry_md5(boardID, md5Sum)

        # Load json data
        self.baseJsonData = json.loads(open(self.jsonPath, 'r').read())

        # Load the module responsible for this board type
        self.boardModule = RomRegistry.get_module(boardID)


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
            self.boardModule.set_bit(i, jsonData)
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
            file.write(json.dumps(jsonData, indent = 2))

        # Convert back to tungboard
        b2j.json_to_board(tmpJsonPath, outputPath)
        os.remove(tmpJsonPath)
