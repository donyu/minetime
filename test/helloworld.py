"""
Basic hello world. Adds one diamond block at (5,5,5)
"""

import logging
import os
import sys
from pymclevel import mclevel, box

MC_DIR = "~/.minecraft/saves"

if __name__ == "__main__":
    world = sys.argv[1]
    saves = os.path.expanduser(MC_DIR)
    worldpath = os.path.join(saves, world)

    # Creates a map if doesn't exist, else loads pre-existing map
    if not os.path.exists(worldpath):
        level = mclevel.MCInfdevOldLevel(worldpath, create=True)
    else:
        level = mclevel.loadWorld(worldpath)
    
    # Empty chunk dimensions
    chunk_box = box.BoundingBox((-32, 0, -32), (64, 64, 64))
    level.createChunksInBox(chunk_box)

    # Diamond ore
    dblock =  level.materials.blockWithID(57)
    dblock_box = box.BoundingBox(origin=(5,5,5), size=(1,1,1)) 
    level.fillBlocks(dblock_box, dblock)
    
    level.saveInPlace()
