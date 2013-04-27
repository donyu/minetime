import unittest
import lexing


class TestLexingSyntax(unittest.TestCase):

    def setUp(self):
        self.lex = lexing.Mtlex()
        self.lex.build()
    
    def test_tokens(self):
        lexer = self.lex.lexer

        type_cases = {1 : 'NUMBER',
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
        
        for key, val in type_cases.iteritems():
            lexer.input(str(key))
            token = lexer.token()
            self.assertEqual(key, token.value)
            self.assertEqual(val, token.type)

    def test_true(self):
        """Temporary sanity test"""
        f = open('tests/textfile.txt', 'r')
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main(verbosity=2)
