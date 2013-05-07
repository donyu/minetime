import unittest
import sys
import ply.yacc as yacc
from textwrap import dedent

sys.path.append('..')
import yaccing
from lexing import Mtlex


class TestYaccing(unittest.TestCase):

    def setUp(self):
        self.parser = yaccing.parser

    def test_helloworld(self):
        prog = """\
def main() {
    x = Flatmap("testfiles/testmap",500,500,500);
    b = (10,20,30);
    x.add(block(COBBLE), b);
    x.close();
}
               """
        self.print_result(prog)

    def test_compound(self):
        prog = """\
def main() {
    { i=0;i=1;i=2; }
}
               """
        self.print_result(prog)

    def test_while(self):
        prog = """\
def main() {
    while (i=1) {i=1;i=1;i=1;}
    i = 0;
}
               """
        self.print_result(prog)

    def test_for(self):
        prog = """
def main() {
    for (i = 1; i = 1; i = 1) {
        i = 1;
    }
}
               """
        self.print_result(prog)

    def test_if(self):
        prog = """\
def main() {
    if (i=222220) {} 
}
               """
        self.print_result(prog)

    def test_if_else(self):
        prog = """\
def main() {
    if (i = 1)
       i = 2;
    else {
       i = 3;
    }
}
               """
        self.print_result(prog)

    def test_if_elseif_else(self):
        prog = """\
def main() {
    if (i = 1)
       i = 2;
    else if (i=2) {
       i = 3;
    } else
       i = 4;
}
               """
        self.print_result(prog)

    def test_0_bug(self):
        """
        BUG: Does not display 0 when assigned
        """
        prog = """\
def main() {
    i = 0;
}
               """
        self.print_result(prog)

    def test_relations_and_arithmetic(self):
        prog = """\
def main() {
    a && b;
    a || b;
    a == b;
    a != b;
    a > b;
    a < b;
    a >= b;
    a <= b;
    a + b;
    2 - 3;
    3 * 3;
    3 / 3;
}
               """
        self.print_result(prog)

    def test_empty_function(self):
        prog = """\
def main(1,2) {
}
               """
        self.print_result(prog)

    def test_complicated(self):
        prog = """\
def main() {
    a * (b - 3) + 3 || 5;
}
               """
        self.print_result(prog)

    def print_result(self, prog):
        result = self.parser.parse(dedent(prog))
        print
        print result


if __name__ == "__main__":
    unittest.main(verbosity=2)
