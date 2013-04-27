import unittest
import lexing


class TestLexingSyntax(unittest.TestCase):

    def setUp(self):
        self.lex = lexing.Mtlex()
        self.lex.build()
        self.lexer = self.lex.lexer
    
    def test_tokens(self):
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
        for key, val in cases.iteritems():
            self.lexer.input(str(key))
            token  = self.lexer.token()
            self.assertEqual(key, token.value)
            self.assertEqual(val, token.type)
        

    #def equals(self, cases):
    #    for key, types in type_cases.iteritems():
    #        self.lexer.input(str(key))
    #        for t in types:
    #            self.assertEqual(

    #def equals(self, key, val):
    #    token = self.lexer.token()
    #    self.assertEqual(key, token.value)
    #    self.assertEqual(val, token.type)


if __name__ == "__main__":
    unittest.main(verbosity=2)
