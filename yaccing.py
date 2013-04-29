import ply.yacc as yacc
import sys
from lexing import Mtlex
from NewTraverse import *

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
               | primary_expression
    '''
    p[0] = Node('expression', [p[1]])


def p_assignment_expression(p):
    '''
    assignment_expression : ID ASSIGN initializer
    '''
    p[0] = Node('assignment_expression', [p[3]], p[1])

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
                        | ID LPAREN RPAREN
    '''
    if len(p) == 5:
        p[0] = Node('function_expression',[p[3]], p[1])
    else:
        p[0] = Node('function_expression', [], p[1])

def p_parameter_list(p):
    '''
    parameter_list : parameter_declaration
                   | parameter_list COMMA parameter_declaration
    '''
    if len(p) == 2:
        p[0] = Node('parameter_list', [p[1]])
    else:
        p[0] = Node('parameter_list',[p[1], p[3]])


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
                       | POINT
    '''
    p[0] = Node('primary_expression', [], p[1])

def p_iteration_statement(p):
    '''
    iteration_statement : WHILE LPAREN expression RPAREN statement
    '''

    p[0] = Node('iteration_statement', [p[3], p[5]])

def p_selection_statement(p):
    '''
    selection_statement : IF LPAREN expression RPAREN compound_statement
                        | IF LPAREN expression RPAREN compound_statement ELSE statement
    '''
    if len(p) == 6:
        p[0] = Node('selection_statement', [p[3], p[5]])
    else:
        p[0] = Node('selection_statement', [p[3], p[5], p[7]])

def p_error(p):
    # we should throw compiler error in this case
    print 'there is no grammar for this'


data_1 = '''
map = Flatmap("testfiles/testmap",500,500,500);
'''
data_2 = '''
map.add(block(COBBLE), (0,0,0));
'''
data_3 = '''
map.close();
'''
data_4 = '''
{ i=0;i=1;i=2; }
'''

data_5 = '''
while (i=1) {i=1;i=1;i=1;}
i = 0;
'''

data_6 = '''
if (i=222220) {} 
if (i=2) {a;} else {b;}
'''

parser = yacc.yacc()
m = Mtlex()
m.build()
print "line 1"
result1 = parser.parse(data_1, lexer=m.lexer)
print result1
print "\nline 2"
result2 = parser.parse(data_2, lexer=m.lexer)
print result2
print "\nline 3"
result3 = parser.parse(data_3, lexer=m.lexer)
print result3
print "\n"
# print "\nline 4"
# result4 = parser.parse(data_4, lexer=m.lexer)
# print result4
# print "\n"
# print "\nline 5"
# result5 = parser.parse(data_5, lexer=m.lexer)
# print result5
# print "\n"
# print "\nline 6"
# result6 = parser.parse(data_6, lexer=m.lexer)
# print result6
# print "\n"
firstline = '''
import logging
import os
import sys
from pymclevel import mclevel
from pymclevel.box import BoundingBox'''
t = Traverse(result1).getpython()
t1 = Traverse(result2).getpython()
t2 = Traverse(result3).getpython()
code = firstline + "\n" + t + "\n" + t1 + "\n" + t2
f = open("hello.py",'w')
f.write(code)
print code
