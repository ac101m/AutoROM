#!/usr/bin/env python3


# Standard
import sys
import numpy as np


# Exception object for improperly formatted json object
class JsonObjectError(Exception): pass


# Return a wire object initialised from json object
def from_json_object(jsonData):
    w = wire()
    w.from_json_object(jsonData)
    return w


# Return a wire object initialised from start and end vectors
def from_position(start, end):
    w = wire()
    w.from_position(start, end)
    return w


# Describes a wire in a tung board
class wire:

    # Set some sensible defaults
    def __init__(self):
        self.iInput = False
        self.length = 1.0
        self.position = np.array([0.0, 0.0, 0.0])
        self.euler = np.array([0.0, 0.0, 0.0])


    # Set wire data from start and end positions
    def from_position(self, start, end, inputInput = False):
        self.iInput = inputInput

        # Compute length of vector
        wireVec = end - start
        self.length = np.linalg.norm(wireVec)

        # Compute position
        self.position = (start + end) / 2.0

        # v1: Use basic trig to compute angles
        dx = wireVec[0]
        dy = wireVec[1]
        dz = wireVec[2]
        self.euler[0] = -np.arctan2(dy, np.sqrt(dx**2 + dz**2))
        self.euler[1] = np.arctan2(dx, dz)
        self.euler[2] = 0.0
        self.euler *= (180 / np.pi)


    # Set wire data from json object
    def from_json_object(self, jsonData):
        try:

            # Check to ensure that the $type field matches
            if jsonData['$type'] != 'SavedObjects.SavedWire, Assembly-CSharp':
                raise JsonError(
                    "Cannot generate wire from json object with $type: '" +
                    jsonData['$type'] + "'.")

            # Extract data from json object
            self.iInput = jsonData['InputInput']
            self.length = jsonData['length']
            self.position[0] = jsonData['LocalPosition']['x']
            self.position[1] = jsonData['LocalPosition']['y']
            self.position[2] = jsonData['LocalPosition']['z']
            self.euler[0] = jsonData['LocalEulerAngles']['x']
            self.euler[1] = jsonData['LocalEulerAngles']['y']
            self.euler[2] = jsonData['LocalEulerAngles']['z']

        # If any of the keys are missing, we got a problem
        except KeyError as e:
            raise JsonObjectError(
                "Cannot generate wire from json object. json object " +
                "malformed, key: '" + e.args[0] + "' not present.")


    # [TODO]
    def as_position(self):
        print('ERROR: wire.as_position not implemented yet')
        sys.exit()
        pass


    # Gets the wire data as a json encodable object
    def as_json_object(self):
        jsonData = {
          "$type": "SavedObjects.SavedWire, Assembly-CSharp",
          "InputInput": self.iInput,
          "length": self.length,
          "LocalPosition": {
            "x": self.position[0],
            "y": self.position[1],
            "z": self.position[2]
          },
          "LocalEulerAngles": {
            "x": self.euler[0],
            "y": self.euler[1],
            "z": self.euler[2]
          },
          "Children": None,
          "CanHaveChildren": False
        }

        return jsonData
