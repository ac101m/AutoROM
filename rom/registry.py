#!/usr/bin/env python3


# Standard
import os
import sys
import json
import importlib


# Paths to board and registry
__BOARD_DATA_DIR = os.path.dirname(__file__) + '/data'
__BOARD_REGISTRY_PATH = __BOARD_DATA_DIR + '/rom-registry.json'


# Attempt to load the board registry
__BOARD_REGISTRY = {}
try:
    __BOARD_REGISTRY = json.loads(open(__BOARD_REGISTRY_PATH, 'rb').read())
except FileNotFoundError:
    print("ERROR: Board registry not found. Nothing to be done.")
    sys.exit()


# Clean all board json files from the board directory
def clean():
    for id in get_rom_ids():
        try:
            os.remove(get_json_path(id))
            print('Cleaned ' + get_json_path(id))
        except FileNotFoundError:
            pass


# Get board path from ID
def get_board_path(boardID):
    return __BOARD_DATA_DIR + '/' + __BOARD_REGISTRY[boardID]['path']


# Get json board path from ID
def get_json_path(boardID):
    return get_board_path(boardID) + '.json'


# Get module path from ID
def get_module(boardID):
    moduleName = __BOARD_REGISTRY[boardID]['module']
    try:
        return importlib.import_module(moduleName)
    except ModuleNotFoundError as e:
        print("ERROR: Failed to load board module '" + moduleName + "'")
        print(e)
        sys.exit()


# Get list of all board IDs
def get_rom_ids():
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
        print(key + ':')
        print("\tCapacity: " + str(__BOARD_REGISTRY[key]['capacity']))
        print("\tPath: " + __BOARD_REGISTRY[key]['path'])


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
