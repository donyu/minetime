import unittest
import sys
import ply.yacc as yacc
from mt_test_cases import MTTests

sys.path.append('..')
import yaccing
from traverse import Traverse

class TestTraverse(unittest.TestCase):
    """
    Tests the traverse for correctness
    """

    firstline = '''
import logging
import os
import sys 
from pymclevel import mclevel
from pymclevel.box import BoundingBox''' 

    def setUp(self):
        self.parser = yaccing.parser
    
    def test_helloworld(self):
        self.traverse(MTTests.helloworld)

    def test_compound(self):
        self.traverse(MTTests.compound)

    def test_while_loop(self):
        self.traverse(MTTests.while_loop)

    def test_if(self):
        self.traverse(MTTests.if_stmt)

    def test_if_elseif_else(self):
        self.traverse(MTTests.if_elseif_else)

    def test_make_blocks(self):
        """
        Check for type mismatch
        """
        with self.assertRaises(Exception):
            self.traverse(MTTests.make_blocks)

    def test_add_block(self):
        self.traverse(MTTests.add_block)

    def test_empty_function(self):
        self.traverse(MTTests.empty_function)
    
    def traverse(self, prog):
        result = self.parser.parse(prog)
        translated = Traverse(result).getpython()
        code = "\n{0}\n{1}\n\n".format(self.firstline, translated)
        print code


if __name__ == "__main__":
    unittest.main(verbosity=2)
