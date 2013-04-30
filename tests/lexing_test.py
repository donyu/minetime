import unittest
import sys
from cStringIO import StringIO
from itertools import izip

sys.path.append('..')
import lexing

class TestLexingSyntax(unittest.TestCase):

    def setUp(self):
        self.lex = lexing.Mtlex()
        self.lex.build()
        self.lexer = self.lex.lexer
    
    def test_tokens(self):
        """
        Checks the correctness of single tokens
        """
        cases = {1 : 'NUMBER',
                 12345 : 'NUMBER',
                 '+' : 'PLUS',
                 '-' : 'MINUS',
                 '/' : 'DIVIDE',
                 '(' : 'LPAREN',
                 ')' : 'RPAREN',
                 'but34' : 'ID',
                 '=' : 'ASSIGN',
                 '{' : 'LCURL',
                 '}' : 'RCURL',
                 '"H3#;.LLO WORLD"' :'STRING',
                 '# #h32.ello' : 'COMMENT',
                 ',' : 'COMMA',
                 '(  1, 2,  3)' : 'POINT',
                 ';' : 'SEMICOLON',
                 ':' : 'COLON'}
        self.assert_tokens_eq(cases)

    def assert_tokens_eq(self, cases):
        """
        Takes in dictionary of value inputs and checks for type and value
        correctness of the LexToken output
        """
        for key, val in cases.iteritems():
            self.lexer.input(str(key))
            token  = self.lexer.token()
            self.assertEqual(key, token.value)
            self.assertEqual(val, token.type)

    def test_helloworld(self):
        """
        Checks the correctness of helloworld.mt
        """
        progfile = open('testfiles/helloworld.mt', 'r')
        expfile = open('testfiles/helloworld.out', 'r')

        self.assert_prog(progfile, expfile)

    def test_sandbox(self):
        """
        Sandbox for mt program lex output
        """
        progfile = open('testfiles/sandbox.mt', 'r')
        print self.lex.tok_str(progfile.read())

    def assert_prog(self, progfile, expfile):
        """
        Takes in a mt programming file and expected output file and checks for
        correctness
        """
        tokens = StringIO(self.lex.tok_str(progfile.read()))

        for t, o in izip(tokens, expfile):
            self.assertEqual(t, o)


if __name__ == "__main__":
    unittest.main(verbosity=2)
