import yaccing as yacc
import sys
from lexing import Mtlex
from traverse import *
from preprocess import *

def main(argv):
    inputfile = argv[1]
    filename = inputfile.split(".")[0]
    source = open(inputfile).read()
# generate the parser
    parser = yacc.getyacc()
# generate the Lexer to be used with parser
    m = Mtlex()
    m.build()
# preprocessing step
    preprocessor = Processor()
    source = preprocessor.preprocess(source)
    tree = parser.parse(source, lexer=m.lexer)
    
    firstline = '''import logging
import os
import sys
from pymclevel import mclevel
from pymclevel.box import BoundingBox
'''
    lastline = '''
if __name__ == '__main__':
    main()
'''
    result = Traverse(tree).getpython()
    code = firstline + "\n" + result + "\n" + lastline + "\n"
    outputfile = filename + ".py"
    output = open(outputfile, 'w')
    output.write(code)

if __name__ == '__main__':
    main(sys.argv)

