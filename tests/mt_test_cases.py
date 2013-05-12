
class MTTests(object):
    """
    Wrapper class for yaccing and traverse test cases. These are mt code
    snippets
    """

    helloworld = """
def main() {
    x = new flatmap("testfilesgitestmap",   500,500,500);
    b = new Point(10,20,30);
    x.add(block(STONE), b);
    x.close();
}"""

    compound = """
def main() {
    { i=0;i=1;i=2; }
}"""

    while_loop = """
def main() {
    while (i=1) {i=1;i=1;i=1;}
    i = 0;
}"""
    for_loop = """
def main() {
    for (i = 1; i = 1; i = 1) {
        i = 1;
    }
}"""
    if_stmt = """
def main() {
    if (i=222220) {} 
}"""

    if_else = """
def main() {
    i = 2;
    if (i = 1)
       i = 2;
    else {
       i = 3;
    }
}"""
    if_elseif_else = """
def main() {
    i = 2;
    if (i == 1)
       i = 2;
    else if (i==2) {
       i = 3;
    } else
       i = 4;
}"""

    zero_bug = """
def main() {
    i = 0;
    i = 1;
}"""
    relations_arithmetic = """
def main() {
    a && b;
    a || b;
    a == b;
    a != b;
    a > b;
    a < b;
    a >= b;
    a <= b;
    a + b;
    2 - 3;
    3 * 3;
}"""
    empty_function = """
def main(1,2) {
}"""
    complicated = """
def main() {
    a * (b - 3) + 3 || 5;
}"""
    external = """
i = 1;

def f(1, 2) {
}

def main() {
    if (a > 3) {
        i;
    }
}"""
    
    return_stmt = """
def main() {
    i = 1;
    return 1;
    return;
}"""

    assignment = """
def main() {
    i = a + 2;
    j = 3 < 2;
}"""
    
    make_blocks = '''
def makeblocks(start, end, x) {
    while (start < end) {
        c = new Point(0,0,start);
        x.add(block(COBBLESTONE), c);
        start = start + 1;
    }
    for (;start<end;start=start+1)
    {
        c = new Point(0,0,start);
        x.add(block(COBBLESTONE), c);
    }
}

def main() {
x = new Flatmap("testfiles/testmap",500,500,500);
makeblocks(0,"hi", x);
x.close();
}
'''
    
    add_block = '''
def main() {
    a = 2;
    if (a > 1) {
        b = 2;
    }
    x = new Flatmap("testfiles/testmap", 500, 500, 500);
    c = new Point(0, 0, 0);
    x.add(block(STONE), c);
    x.close();
}
'''

    def __init__(self):
        pass
