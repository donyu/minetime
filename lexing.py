import ply.lex as lex

class Mtlex:

    reserved = {'if' : 'IF', 
                'then' : 'THEN', 
                'else' : 'ELSE', 
                'while' : 'WHILE', 
                'elif' : 'ELIF',
                'def' : 'DEF',
                'for' : 'FOR',
                'while' : 'WHILE'
                }

    tokens = ['NUMBER',
              'PLUS',
              'MINUS',
              'TIMES',
              'DIVIDE',
              'LPAREN',
              'RPAREN',
              'ID',
              'ASSIGN',
              'LCURL',
              'RCURL',
              'STRING',
              'COMMENT',
              'COMMA',
              'POINT',
              'DOTOPERATOR',
              'SEMICOLON',
              'COLON'] + list(reserved.values())

    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_ASSIGN  = r'='
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_LCURL = r'{'
    t_RCURL = r'}'
    t_STRING = r'".*"'
   # t_COMMMENT = r'/\*.*\*/'
    t_COMMENT = r'\#(.*)(\n)?'
    t_COMMA = r','
    t_DOTOPERATOR = r'\.'
    NUMBER =  r'\d+'
    t_POINT = t_LPAREN + NUMBER + t_COMMA + NUMBER + t_COMMA + NUMBER + t_RPAREN

    # A regular expression rule with some action code
    def t_NUMBER(self,t):
        r'\d+'
        # BUG: FIX, DON. 0 DOES NOT WORKKKK
        # TODO: UNARY MINUS OR FORCE NEGATIVE NUMBER?
        t.value = int(t.value)    
        return t        
    
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        return t

    # Define a rule so we can track line NUMBERs
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def get_lexer(self):
        return self.lexer

    def tok_str(self, data):
        self.lexer.input(data)
        tok_str = ""
        while True:
            tok = self.lexer.token()
            if not tok: 
              break
            tok_str += str(tok) + "\n"
        return tok_str

# m = Mtlex()
# data = '''
# map = Flatmap("testmap.dat",500,500) /* hi */
# map.add(block(COBBLE), (0,0,0))
# map.close()
# '''
# m.build()           # Build the lexer
# m.test(data)     # Test it

if __name__ == "__main__":
    m = Mtlex()
    m.build()
    l = m.get_lexer()
    print "Enter a string to be tokenized"
    while 1:
        line = raw_input()
        print m.tok_str(line)
        print "Enter a string to be tokenized"
