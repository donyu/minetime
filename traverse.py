import sys

class Traverse:

    def __init__(self, tree, file = sys.stdout):
        self.f = file
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

    def dispatch(self, tree):
        "Dispatcher function, dispatching tree type T to method _T."
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return
        meth = getattr(self, "_"+tree.type)
        meth(tree)

    def _primary_expression(self,tree):
        self.fill(tree.leaf)

    def _class_method_expression(self,tree):
        self.fill(tree.leaf)
        self.write(".")
        self.dispatch(tree.children)

    def _function_expression(self,tree): # not complete
        self.write(tree.leaf)
        self.write("(")
        self.dispatch(tree.children)
        self.write(")")

    def _expression(self,tree):
        self.dispatch(tree.children)

    def _assignment_expression