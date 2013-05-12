import unittest
import sys
import ply.yacc as yacc
from mt_test_cases import MTTests
from os.path import join

sys.path.append('..')
import yaccing
from textwrap import dedent
from lexing import Mtlex

test_dir = 'testfiles'

class TestYaccing(unittest.TestCase):

    def setUp(self):
        self.parser = yaccing.parser

    def test_helloworld(self):
        self.print_result(MTTests.helloworld)

    def test_compound(self):
        self.print_result(MTTests.compound)

    def test_while(self):
        self.print_result(MTTests.while_loop)

    def test_for(self):
        self.print_result(MTTests.for_loop)

    def test_if(self):
        self.print_result(MTTests.if_stmt)

    def test_if_else(self):
        self.print_result(MTTests.if_else)

    def test_if_elseif_else(self):
        self.print_result(MTTests.if_elseif_else)

    def test_0_bug(self):
        """
        bug: does not display 0 when assigned
        """
        self.print_result(MTTests.zero_bug)

    def test_relations_and_arithmetic(self):
        self.print_result(MTTests.relations_arithmetic)

    def test_empty_function(self):
        self.print_result(MTTests.empty_function)

    def test_complicated(self):
        self.print_result(MTTests.complicated)

    def test_external(self):
        self.print_result(MTTests.external)

    def test_return(self):
        self.print_result(MTTests.return_stmt)

    def test_assignment(self):
        self.print_result(MTTests.assignment)

    def print_result(self, prog):
        result = self.parser.parse(prog)
        print
        print result


if __name__ == "__main__":
    unittest.main(verbosity=2)
