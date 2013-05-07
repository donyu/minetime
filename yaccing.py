import ply.yacc as yacc
import sys
from lexing import Mtlex
from traverse import *

tokens = Mtlex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

class Node(object):

    def __init__(self,type,children=None,leaf=None,code=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf
         self.code = code

    def __str__(self):
        return self.traverse(1)

    def traverse(self, i):
        s = self.type
        indent = "\n" + i*' |'
        if self.leaf:
            if isinstance(self.leaf, Node):
                s += indent + self.leaf.traverse(i+1)
            else:
                s += indent + str(self.leaf)
        for children in self.children:
            s += indent + children.traverse(i+1)
        return s

def p_function_definition(p):
    '''
    function_definition : DEF ID LPAREN parameter_list RPAREN LCURL declaration_list RCURL
                        | DEF ID LPAREN parameter_list RPAREN LCURL RCURL
    '''
    if len(p) == 9:
        p[0] = Node('function_definition', [p[4], p[7]], p[2])
    else:
        p[0] = Node('function_definition', [p[4]], p[2])

def p_declaration_list(p):
    '''
    declaration_list : declaration
                     | declaration_list declaration
    '''

    if len(p) == 2:
        p[0] = Node('declaration_list', [p[1]])
    else:
        p[0] = Node('declaration_list', [p[1], p[2]])

def p_declaration(p):
    '''
    declaration : statement
                | class_method_expression SEMICOLON
    '''
    p[0] = Node('declaration', [p[1]])

def p_statement(p):
    '''
    statement : compound_statement
              | expression_statement
              | iteration_statement
              | selection_statement
    '''
    p[0] = Node('statement', [p[1]]) 

def p_compound_statement(p):
    '''
    compound_statement : LCURL RCURL
                       | LCURL statement_list RCURL
    '''
    if len(p) == 3:
        p[0] = Node('compound_statement', [], 'emptychange')
    else:
        p[0] = Node('compound_statement', [p[2]])

def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    if len(p) == 2:
        p[0] = Node('statement_list', [p[1]])
    else:
        p[0] = Node('statement_list', [p[1], p[2]])

def p_expression_statement(p):
    '''
    expression_statement : SEMICOLON
                         | expression SEMICOLON
    '''
    if len(p) == 2:
        p[0] = Node('expression_statement', [], 'emptychange')
    else:
        p[0] = Node('expression_statement', [p[1]])


def p_expression(p):
    '''
    expression : assignment_expression 
    '''
    p[0] = Node('expression', [p[1]])


def p_assignment_expression(p):
    '''
    assignment_expression : ID ASSIGN initializer
                          | logical_or_expression
    '''
    if len(p) == 4:
        p[0] = Node('assignment_expression', [p[3]], p[1])
    else:
        p[0] = Node('assignment_expression', [p[1]])

def p_logical_or_expression(p):
    '''
    logical_or_expression : logical_and_expression
                          | logical_or_expression OR logical_and_expression
    '''
    if len(p) == 2:
        p[0] = Node('logical_or_expression', [p[1]])
    else:
        p[0] = Node('logical_or_expression', [p[1], p[3]], p[2])

def p_logical_and_expression(p):
    '''
    logical_and_expression : equality_expression
                           | logical_and_expression AND equality_expression
    '''
    if len(p) == 2:
        p[0] = Node('logical_and_expression', [p[1]])
    else:
        p[0] = Node('logical_and_expression', [p[1], p[3]], p[2])

def p_equality_expression(p):
    '''
    equality_expression : relational_expression
                        | equality_expression EQ relational_expression
                        | equality_expression NEQ relational_expression
    '''
    if len(p) == 2:
        p[0] = Node('equality_expression', [p[1]])
    else:
        p[0] = Node('equality_expression', [p[1], p[3]], p[2])

def p_relational_expression(p):
    '''
    relational_expression : additive_expression
                          | relational_expression G_OP additive_expression
                          | relational_expression L_OP additive_expression
                          | relational_expression GE_OP additive_expression
                          | relational_expression LE_OP additive_expression
    '''
    if len(p) == 2:
        p[0] = Node('relational_expression', [p[1]])
    else:
        p[0] = Node('relational_expression', [p[1], p[3]], p[2])

def p_additive_expression(p):
    '''
    additive_expression : multiplicative_expression
                        | additive_expression PLUS multiplicative_expression
                        | additive_expression MINUS multiplicative_expression
    '''
    if len(p) == 2:
        p[0] = Node('additive_expression', [p[1]])
    else:
        p[0] = Node('additive_expression', [p[1], p[3]], p[2])

def p_multiplicative_expression(p):
    '''
    multiplicative_expression : primary_expression
                              | multiplicative_expression TIMES primary_expression
                              | multiplicative_expression DIVIDE primary_expression
    '''
    if len(p) == 2:
        p[0] = Node('multiplicative_expression', [p[1]])
    else:
        p[0] = Node('multiplicative_expression', [p[1], p[3]], p[2])

def p_initializer(p):
    '''
    initializer : ID LPAREN parameter_list RPAREN
                | primary_expression
    '''
    if len(p) == 2:
        p[0] = Node('initializer', [p[1]])
    else:
        p[0] = Node('initializer', [p[3]], p[1])

def p_class_method_expression(p):
    '''
    class_method_expression : ID DOTOPERATOR function_expression
    '''
    p[0] = Node('class_method_expression',[p[3]], p[1])

def p_function_expression(p):
    '''
    function_expression : ID LPAREN parameter_list RPAREN
    '''
    if len(p) == 5:
        p[0] = Node('function_expression',[p[3]], p[1])
    else:
        p[0] = Node('function_expression', [], p[1])

def p_parameter_list(p):
    '''
    parameter_list : parameter_declaration
                   | parameter_list COMMA parameter_declaration
                   | 
    '''
    if len(p) == 2:
        p[0] = Node('parameter_list', [p[1]])
    elif len(p) == 4:
        p[0] = Node('parameter_list',[p[1], p[3]])
    else:
        p[0] = Node('parameter_list')

def p_parameter_declaration(p):
    '''
    parameter_declaration : initializer
    '''
    p[0] = Node('parameter_declaration', [p[1]])


def p_primary_expression(p):
    '''
    primary_expression : ID 
                       | STRING
                       | NUMBER
                       | point_gen
                       | LPAREN expression RPAREN
    '''
    if not isinstance(p[1], basestring) and not isinstance(p[1],int):
        p[0] = Node('primary_expression', [p[1]])
    elif len(p) == 4:
        p[0] = Node('primary_expression', [p[2]])
    else:
        p[0] = Node('primary_expression', [], p[1])


def p_point_gen(p):
    '''
    point_gen : POINT
    '''
    p[0] = Node('point_gen',[], p[1])

def p_iteration_statement(p):
    '''
    iteration_statement : WHILE LPAREN expression RPAREN statement
                        | FOR LPAREN expression_statement expression_statement expression RPAREN statement
    '''
    if p[1] == "while":
        p[0] = Node('iteration_statement', [p[3], p[5]])
    else:
        p[0] = Node('iteration_statement', [p[3], p[4], p[5], p[7]])

def p_selection_statement(p):
    '''
    selection_statement : IF LPAREN expression RPAREN statement
                        | IF LPAREN expression RPAREN statement ELSE statement
    '''
    if len(p) == 6:
        p[0] = Node('selection_statement', [p[3], p[5]])
    else:
        p[0] = Node('selection_statement', [p[3], p[5], p[7]])

def p_error(p):
    # we should throw compiler error in this case
    print 'there is no grammar for this'


data_1 = '''
def main(){
x = Flatmap("testfiles/testmap",500,500,500);
a = 10;
b = Point(a,a,a);
if (i*5<=30 && x!=5)
{
   i = 2;
   a = 3;
}
else {
   i = 3;
}
while (i*5<=30 && x!=5) 
{
    i=3333;
}
x.add(block(COBBLE), b);
x.close();
}
'''

data_2 = '''
a = (10,20,30);
'''

data_3 = '''
a = 2
if (a> 1 ) { a = 1;}
'''

parser = yacc.yacc()
m = Mtlex()
m.build()

result1 = parser.parse(data_1, lexer=m.lexer)
print result1

firstline = '''
import logging
import os
import sys
from pymclevel import mclevel
from pymclevel.box import BoundingBox'''
t = Traverse(result1).getpython()
code = firstline + "\n" + t + "\n"
#f = open("hello.py",'w')
#f.write(code)
print code
