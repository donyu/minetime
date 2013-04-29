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
        return self.traverse(0)

    def traverse(self, i):
        s = self.type
        indent = "\n" + i*2*' '
        if self.leaf:
            if isinstance(self.leaf, Node):
                s += indent + self.leaf.traverse(i+1)
            else:
                s += indent + str(self.leaf)
        for children in self.children:
            s += indent + children.traverse(i+1)
        return s
    

def p_expression(p):
    '''
    expression : assignment-expression SEMICOLON
               | class-method-expression SEMICOLON
               | function-expression SEMICOLON
    '''
    p[0] = Node('expression', [p[1]])


def p_assignment_expression(p):
    '''
    assignment-expression : ID ASSIGN initializer
    '''
    p[0] = Node('assignment_expression', [p[3]], p[1])

def p_initializer(p):
    '''
    initializer : ID LPAREN parameter-list RPAREN
                | POINT
    '''
    if len(p) == 2:
        p[0] = Node('initializer', [], p[1])
    else:
        p[0] = Node('initializer', [p[3]], p[1])


def p_class_method_expression(p):
    '''
    class-method-expression : ID DOTOPERATOR function-expression
    '''
    p[0] = Node('class_method_expression',[p[3]], p[1])

def p_function_expression(p):
    '''
    function-expression : ID LPAREN parameter-list RPAREN
                        | ID LPAREN RPAREN
    '''
    if len(p) == 5:
        p[0] = Node('function_expression',[p[3]], p[1])
    else:
        p[0] = Node('function_expression', [], p[1])

def p_parameter_list(p):
    '''
    parameter-list : parameter-declaration
                   | parameter-list COMMA parameter-declaration
    '''
    if len(p) == 2:
        p[0] = Node('parameter_list', [p[1]])
    else:
        p[0] = Node('parameter_list',[p[1], p[3]])


def p_parameter_declaration(p):
    '''
    parameter-declaration : primary-expression
                          | initializer
    '''
    p[0] = Node('parameter_declaration', [p[1]])


def p_primary_expression(p):
    '''
    primary-expression : ID
                       | STRING
                       | NUMBER
    '''
    p[0] = Node('primary_expression', [], p[1])

def p_error(p):
    # we should throw compiler error in this case
    print 'there is no grammar for this'


data_1 = '''
map = Flatmap("testmap.dat",500,500,500);
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
result1 = parser.parse(data_1, lexer=m.lexer)
print result1
print "\nline 2"
result2 = parser.parse(data_2, lexer=m.lexer)
print result2
print "\nline 3"
result3 = parser.parse(data_3, lexer=m.lexer)
print result3
print "\n"
firstline = '''
import logging
import os
import sys
from pymclevel import mclevel, box'''
t = Traverse(result1).getpython()
t1 = Traverse(result2).getpython()
t2 = Traverse(result3).getpython()
code = firstline + "\n" + t + "\n" + t1 + "\n" + t2
f = open("hello.py",'w')
f.write(code)
print code