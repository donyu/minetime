import unittest
import lexing


class TestLexingSyntax(unittest.TestCase):

    def setUp(self):
        self.lex = lexing.Mtlex()
        self.lex.build()
    
    def test_if(self):
        """Tests single if token.

        Note: Shouldn't be correct in final version due to lack of brackets
        """

        lexeme = "LexToken(IF,'if',1,0)"
        self.assertEqual(lexeme, self.lex.tok_str("if"))

    def test_true(self):
        """Temporary sanity test"""
        f = open('tests/textfile.txt', 'r')
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main(verbosity=2)
