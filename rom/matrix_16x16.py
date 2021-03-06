
# Standard
import numpy as np


# This project
import tung.wire as TungWire


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
    wireStartPos = np.array([6.42100068, -4.72500229, 4.95])
    wireEndPos = np.array([7.20500068, -4.72500229, 4.95])

    # Compute wire start and end positions from indices
    wireStartPos += posDelta * majorIndexVec
    wireEndPos += posDelta * minorIndexVec

    # Add wire to json data
    wire = TungWire.from_position(wireStartPos, wireEndPos)
    jsonData['Children'].append(wire.as_json_object())
