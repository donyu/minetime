import sys
import unittest
import filecmp
from filecmp import dircmp

sys.path.append('..')
from pymclevel.box import BoundingBox
import templevel

STANDARD = 'testfiles/Standard'

class TestLevelCreation(unittest.TestCase):

    def setUp(self):
        self.testlevel = templevel.TempLevel("Temp")

    def test_chunk_creation(self):
        level = self.testlevel.level

        level.createChunk(0, 0)
        level.saveInPlace()
        self.assertTrue(level.containsChunk(0, 0))

    def test_fill(self):
        level = self.testlevel.level

        level.createChunk(0, 0)
        cx, cz = level.allChunks.next()
        box = BoundingBox((cx * 16, 0, cz * 16), (32, level.Height, 32))
        level.fillBlocks(box, level.materials.WoodPlanks)
        level.fillBlocks(box, level.materials.WoodPlanks, [level.materials.Stone])
        level.saveInPlace()
        c = level.getChunk(cx, cz)

        assert (c.Blocks == 5).all()

if __name__ == "__main__":
    unittest.main(verbosity=2)
