import ply.yacc as yacc
from lexing import Mtlex

tokens = Mtlex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

def p_expression(p):
	'''
	expression : assignment-expression SEMICOLON
			   | class-method-expression SEMICOLON
			   | function-expression SEMICOLON
	'''
	print 'expression'

def p_assignment_expression(p):
    '''
    assignment-expression : ID ASSIGN initializer
    '''
    print 'assignment-operator'

def p_initializer(p):
	'''
	initializer : ID LPAREN parameter-list RPAREN
				| POINT
	'''
	print 'initializer'

def p_class_method_expression(p):
	'''
	class-method-expression : ID DOTOPERATOR function-expression
	'''
	print 'class-method'

def p_function_expression(p):
	'''
	function-expression : ID LPAREN parameter-list RPAREN
						| ID LPAREN RPAREN
	'''
	print 'function-call'

def p_parameter_list(p):
	'''
	parameter-list : parameter-declaration
				   | parameter-list COMMA parameter-declaration
	'''
	print 'p-list'

def p_parameter_declaration(p):
	'''
	parameter-declaration : primary-expression
						  | initializer
	'''
	print 'parameter'
	p[0] = p[1]

def p_primary_expression(p):
	'''
	primary-expression : ID
					   | STRING
					   | NUMBER
	'''

def p_error(p):
	# we should throw compiler error in this case
    print 'there is no grammar for this'

data_1 = '''
map = Flatmap("testmap.dat",500,500);
'''
data_2 = '''
map.add(block(COBBLE), (0,0,0));
'''
data_3 = '''
map.close();
'''
parser = yacc.yacc()
m = Mtlex()
m.build()
print "line 1"
result = parser.parse(data_1, lexer=m.lexer)
print "\nline 2"
result = parser.parse(data_2, lexer=m.lexer)
print "\nline 3"
result = parser.parse(data_3, lexer=m.lexer)
