#!/usr/bin/env python3


# Standard
import sys
import numpy as np


# Generate wire json data from start
def gen_wire(start, end):

    # Compute length of vector
    wireVec = end - start
    length = np.linalg.norm(wireVec)

    # Compute position
    position = (start + end) / 2.0

    # v1: Use basic trig to compute angles, janky
    dx = wireVec[0]
    dy = wireVec[1]
    dz = wireVec[2]
    euler_x = - np.arctan2(dy, np.sqrt(dx**2 + dz**2))
    euler_y = np.arctan2(dx, dz)
    euler = np.array([euler_x, euler_y, 0.0]) * (180 / np.pi)

    # Pack up the angles and return
    return length, position, euler


# Generate JSON data from wire
def gen_wire_json(start, end, inputinput = False):
    length, position, euler = gen_wire(start, end)

    wire_json = {
      "$type": "SavedObjects.SavedWire, Assembly-CSharp",
      "InputInput": inputinput,
      "length": length,
      "LocalPosition": {
        "x": position[0],
        "y": position[1],
        "z": position[2]
      },
      "LocalEulerAngles": {
        "x": euler[0],
        "y": euler[1],
        "z": euler[2]
      },
      "Children": None,
      "CanHaveChildren": False
    }

    return wire_json


# Set bit for 16 by 16 matrix ROM
def set_bit(i, jsonData):

    # Compute major and minor indices
    minorIndex = i & 0xff
    majorIndex = (i >> 8) & 0xff
    minorIndexVec = np.array([0.0, (minorIndex >> 4) & 0xf, minorIndex & 0xf])
    majorIndexVec = np.array([0.0, (majorIndex >> 4) & 0xf, majorIndex & 0xf])

    # Amount to advance in each axis for each incremenet of index
    posDelta = np.array([0.0, 0.3, -0.3])

    # Position of wires @ index 0
    wireStartPos = np.array([6.42100264, -4.7250185, 7.0499835])
    wireEndPos = np.array([7.20500444, -4.7250185, 7.0499835])

    # Compute wire start and end positions from indices
    wireStartPos += posDelta * majorIndexVec
    wireEndPos += posDelta * minorIndexVec

    # Add wire to json data
    jsonData['Children'].append(gen_wire_json(wireStartPos, wireEndPos))
