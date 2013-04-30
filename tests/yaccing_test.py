import unittest
import sys
import ply.yacc as yacc
from textwrap import dedent

sys.path.append('..')
import yaccing
from lexing import Mtlex

tokens = Mtlex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

class TestYaccing(unittest.TestCase):

    def setUp(self):
        self.parser = yaccing.parser

    def test_helloworld(self):
        prog = """\
               map = Flatmap("testfiles/testmap",500,500,500);
               map.add(block(COBBLE), (0,0,0));
               map.close();
               """
        self.print_result(prog)

    def test_compound(self):
        prog = """\
               { i=0;i=1;i=2; }
               """
        self.print_result(prog)

    def test_while(self):
        prog = """\
               while (i=1) {i=1;i=1;i=1;}
               i = 0;
               """
        self.print_result(prog)

    def test_selection(self):
        prog = """\
               if (i=222220) {} 
               if (i=2) {a;} else {b;}
               """
        self.print_result(prog)

    def print_result(self, prog):
        result = self.parser.parse(dedent(prog))
        print
        print result


if __name__ == "__main__":
    unittest.main(verbosity=2)
