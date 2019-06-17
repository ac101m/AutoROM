
# Standard
import numpy as np


# This project
import tung.wire as TungWire


# Set bit for 16 by 16 matrix ROM
def set_bit(i, jsonData):

    # Compute major and minor indices
    minorIndex = i & 0x3f
    majorIndex = (i >> 6) & 0x3f
    minorIndexVec = np.array([0.0, (minorIndex >> 3) & 0x7, minorIndex & 0x7])
    majorIndexVec = np.array([0.0, (majorIndex >> 3) & 0x7, majorIndex & 0x7])

    # Amount to advance in each axis for each incremenet of index
    posDelta = np.array([0.0, 0.3, -0.3])

    # Position of wires @ index 0
    wireStartPos = np.array([4.9210049, -2.32500243, 2.55000448])
    wireEndPos = np.array([5.4050051, -2.32500243, 2.55000448])

    # Compute wire start and end positions from indices
    wireStartPos += posDelta * majorIndexVec
    wireEndPos += posDelta * minorIndexVec

    # Add wire to json data
    wire = TungWire.from_position(wireStartPos, wireEndPos)
    jsonData['Children'].append(wire.as_json_object())
