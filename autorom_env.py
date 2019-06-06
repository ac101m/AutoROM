#!/usr/bin/env python3


# standard
import os
import json


# Path to environment variable file
__ENV_PATH = os.path.dirname(__file__) + '/env.json'
__ENV_DICT = {}


# Save the dictionary containing evironment variables
def __save():
    with open(__ENV_PATH, "w") as file:
        json.dump(__ENV_DICT, file)


# Load the environment variable dictionary
def __load():
    global __ENV_DICT
    if os.path.isfile(__ENV_PATH):
        with open(__ENV_PATH, 'r') as file:
            __ENV_DICT = json.load(file)


# Check if variable exists
def __var_exists(name):
    if name in __ENV_DICT:
        return True
    return False


# Set an environment variable
def set_var(name, value):
    __ENV_DICT[name] = value
    __save()


# Get an environment variable
def get_var(name):
    if __var_exists(name):
        return __ENV_DICT[name]
    else:
        return None

# Delete all board variables
def clean():
    try:
        os.remove(__ENV_PATH)
        print('Cleaned ' + __ENV_PATH)
    except FileNotFoundError:
        pass


# Print the entire environment variable dictionary
def print_all():
    print(__ENV_DICT)


# Load dictionary from file on import
__load()
