#!/usr/bin/env python3


# Standard
import os
import json


# This project
import autorom_image as image
import autorom_util as util


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
    return __BOARD_REGISTRY[id]['path']


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


# Class describes a board
class board:
     def __init__(self, type, image):
         pass
