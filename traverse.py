import sys

class Traverse(object):

    def __init__(self, tree, file = sys.stdout):
        self.f = file
        self.flist = {"Flatmap": "Flatmap",
                      "block": "level.materials.blockWithID", 
                      "add": "level.fillBlocks",
                      "close": "level.saveInPlace"}
        self.blocks = {"COBBLE": 4, "AIR": 0, "STONE": 1, "GRASS":2, "DIRT": 3}
        self.future_imports = []
        self._indent = 0
        self.dispatch(tree)
        self.f.write("")
        self.f.flush()

    def fill(self, text = ""):
        "Indent a piece of text, according to the current indentation level"
        self.f.write("\n"+"    "*self._indent + text)

    def write(self, text):
        "Append a piece of text to the current line."
        self.f.write(text)

    def enter(self):
        "Print ':', and increase the indentation."
        self.write(":")
        self._indent += 1

    def leave(self):
        "Decrease the indentation level."
        self._indent -= 1

    def dispatch(self, tree, boolean=0):
        "Dispatcher function, dispatching tree type T to method _T."
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return
        meth = getattr(self, "_"+tree.type)
        meth(tree)

    def _primary_expression(self,tree):
        if tree.leaf in self.blocks:
            self.write(str(self.blocks[tree.leaf]))
        else:
            self.write(str(tree.leaf))

    def _class_method_expression(self,tree):
        self.write(tree.leaf)
        self.write(".")
        self.dispatch(tree.children)

    def _function_expression(self,tree): # not complete
        if tree.leaf in self.flist:
            self.write(self.flist[tree.leaf])
        else:  
            self.write(tree.leaf)
        self.write("(")
        self.dispatch(tree.children)
        self.write(")")

    def _expression(self,tree):
        self.dispatch(tree.children)

    def _assignment_expression(self, tree):
        self.write(tree.leaf)
        self.write("=")
        self.dispatch(tree.children)

    def _initializer(self, tree):
        if tree.leaf in self.flist:
            self.write(self.flist[tree.leaf])
        else:  
            self.write(tree.leaf)
        if tree.children:
            self.write("(")
            self.dispatch(tree.children)
            self.write(")")

    def _parameter_list(self, tree):
        if len(tree.children) == 1:
            self.dispatch(tree.children)
        else:
            self.dispatch(tree.children[0])
            self.write(",")
            self.dispatch(tree.children[1])

    def _parameter_declaration(self, tree):
        self.dispatch(tree.children)


