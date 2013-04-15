import os
from pymclevel import mclevel, box
import logging

MC_DIR = "~/.minecraft/saves"
world = "testworld4"
saves = os.path.expanduser(MC_DIR)
worldpath = os.path.join(saves, world)

logging.basicConfig(level=logging.INFO)

if not os.path.exists(worldpath):
    level = mclevel.MCInfdevOldLevel(worldpath, create=True)

level = mclevel.loadWorld(worldpath)

box = box.BoundingBox((-4, 68, 8), (5,5,5))
dore =  level.materials.blockWithID(56)
level.fillBlocks(box, dore)
level.saveInPlace()
