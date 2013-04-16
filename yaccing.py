import ply.yacc as yacc

# get token map from lexer
from lexing import Mtlex

parser = yacc.yacc()

result = parser.parse(data, lexer=Mtlex)
