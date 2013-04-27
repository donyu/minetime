import atexit
import os
from os.path import join
import shutil
from pymclevel import mclevel

TEST_DIR = 'testfiles/'

class TempLevel(object):

    def __init__(self, filename, delete=True):
        self.filename = filename
        self.testpath = join(TEST_DIR, filename)

        if os.path.exists(self.testpath) and delete:
            shutil.rmtree(self.testpath)

        self.level = mclevel.MCInfdevOldLevel(self.testpath, create=True)
        atexit.register(self.removeTemp)

    def removeTemp(self):
        if os.path.isdir(self.testpath):
            shutil.rmtree(self.testpath)
        
