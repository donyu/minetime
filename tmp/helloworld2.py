"""
Basic hello world. Adds one diamond block at (5,5,5)
"""

import logging
import os
import sys
from pymclevel import mclevel
from pymclevel.box import BoundingBox

if __name__ == "__main__":
    level = mclevel.MCInfdevOldLevel("testmap", create=True)

    # chunk_box = box.BoundingBox((-32, 0, -32), (64, 64, 64))
    level.createChunksInBox(BoundingBox((-32, 0, -32), (64, 64, 64)))

    # Diamond ore
    # dblock =  level.materials.blockWithID(57)
    # dblock_box = BoundingBox(origin=(5,5,5), size=(1,1,1)) 
    level.fillBlocks(BoundingBox(origin=(5,5,5), size=(1,1,1)),
                     level.materials.blockWithID(57))
    
    level.saveInPlace()

