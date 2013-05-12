import re
import sys
from mt_test_cases import MTTests

sys.path.append('..')
import yaccing

parser = yaccing.parser

for attr in MTTests.__dict__.keys():
    if not re.match(r'^__.*__$', attr):
        result = parser.parse(getattr(MTTests, attr))
        f = open('testfiles/' + attr, 'w')
        f.write(result.__str__())
