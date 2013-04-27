import ply.yacc as yacc
from lexing import Mtlex

tokens = Mtlex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

def p_expression(p):
	'''
	expression : assignment-expression
			   | initializer
	'''
	print 'expression'

def p_assignment_expression(p):
    '''
    assignment-expression : ID ASSIGN initializer
    '''
    print 'assignment-operator'
    print p[3]
    # p[0] = p[1] + p[3]

def p_initializer(p):
	'''
	initializer : ID LPAREN parameter-list RPAREN
	'''
	print 'initializer'

def p_parameter_list(p):
	'''
	parameter-list : parameter-declaration
				   | parameter-list COMMA parameter-declaration
	'''
	print 'p-list' + ' ' + str(p[1])

def p_parameter_declaration(p):
	'''
	parameter-declaration : STRING 
						  | NUMBER
	'''
	print 'parameter' + ' ' + str(p[1])
	p[0] = p[1]

data = '''
map = Flatmap("testmap.dat",500,500);
'''
parser = yacc.yacc()
m = Mtlex()
m.build()
l = m.get_lexer()
result = parser.parse(data, lexer=l)
