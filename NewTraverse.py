import sys

class Traverse(object):

    def __init__(self, tree, file = sys.stdout):
        self.f = file
        self.flist = {"Flatmap": "Flatmap",
                      "block": "materials.blockWithID", 
                      "add": "fillBlocks",
                      "close": "saveInPlace"}
        self.flistsymbol = {"close" : "MAP"}
        self.blocks = {"COBBLE": 4, 
                       "AIR": 0, 
                       "STONE": 1, 
                       "GRASS":2, 
                       "DIRT": 3}
        self.future_imports = []
        self.tempPoints = set()
        # Type table for variables 
        self.symbols = {}
        self._indent = 0
        self.x = self.dispatch(tree)
        self.f.write("")
        self.f.flush()

    def fill(self, text = ""):
        "Indent a piece of text, according to the current indentation level"
        return "\n"+"    "*self._indent + text

    def getpython(self):
        return self.x

    def flatten(self, x):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(self.flatten(el))
            else:
                result.append(el)
        return result

    def write(self, text):
        "Append a piece of text to the current line."
        self.f.write(text)

    def enter(self):
        "Print ':', and increase the indentation."
        self._indent += 1
        return ":"

    def leave(self):
        "Decrease the indentation level."
        self._indent -= 1

    # calls the function corresponding to the name of the node of the tree. Call on a single node and not a list
    def dispatch(self, tree, flag=None): 
        "Dispatcher function, dispatching tree type T to method _T."
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t,flag)
            return
        meth = getattr(self, "_"+tree.type)
        x = meth(tree,flag)
        return x

    def _primary_expression(self,tree,flag=None):
        if tree.leaf in self.blocks:
            return str(self.blocks[tree.leaf])
        elif flag == "block":
            raise Exception("Not a valid block type")
        elif tree.leaf:
            return str(tree.leaf)
        else: # It is a point
            return self.dispatch(tree.children[0],flag)

    def _class_method_expression(self,tree,flag=None):
        s = tree.leaf
        a = self.dispatch(tree.children[0],s)
        return a

    def _function_expression(self,tree,flag=None): # not complete
        if tree.leaf == "add":
            return self.add_method(tree,flag)
        elif tree.leaf in self.flist:
            if tree.leaf in self.flistsymbol:
                if not self.symbols.get(flag) == self.flistsymbol[tree.leaf]:
                    raise Exception(tree.leaf + " method called on a non " + self.flistsymbol[tree.leaf] + " type")
            return flag + "." + self.flist[tree.leaf] + "()"

    def add_method(self,tree,flag=None):
        # add must be called on a map type
        if not self.symbols.get(flag) == "MAP":
            raise Exception("Add method called on a non map type")
        a = flag + "." + self.flist[tree.leaf] + "("
        x = self.dispatch(tree.children[0],flag) # x[0] has block with number, x[1] has point
        if len(x) != 2:
            raise Exception("Wrong number of parameters given to add method")
        print "It is:",x[1]
        if not self.symbols.get(x[1]) == "POINT" and not x[1] in self.tempPoints:
            raise Exception("Not a valid point")
        if x[1] in self.tempPoints:
            self.tempPoints.remove(x[1])
        p1 = "BoundingBox(origin=" + x[1] + ",size=(1,1,1)),"
        p2 = flag + "." + x[0]
        a+= p1 + p2 + ")"
        return a

    def _expression(self,tree,flag=None):
        return self.dispatch(tree.children[0],flag)

    def _assignment_expression(self, tree,flag=None):
        x = self.dispatch(tree.children[0],flag) # x has name, y has params
        print x
        if type(x) is tuple:
            if x[0] == "Flatmap": 
                self.symbols[tree.leaf] = "MAP" # add to symbol table
                return self.flatmap_method(tree.leaf, x[1])
        else: # assigning a point right now
            if x in self.tempPoints:
                self.symbols[tree.leaf] = "POINT"
                self.tempPoints.remove(x)
            return tree.leaf + "=" + x

    def flatmap_method(self, name, param):
        if len(param) != 4:
            raise Exception("Wrong number of params passed to Flatmap")
        else:
            sizex = param[1]
            sizey = param[2]
            sizez = param[3]
            x = str(int(int(sizex) * 1/2 * -1))
            y = str(0)
            z = str(int(int(sizez) * 1/2 * -1))
            if sizey > 255:
                sizey = 255
            point = "(" + x + "," + y + "," + z + ")"
            size = "(" + str(sizex) + "," + str(sizey) + "," + str(sizez) + ")"
            fline = "mclevel.MCInfdevOldLevel(" + param[0] + ", create=True)"
            line = name + ".createChunksInBox(BoundingBox(" + point + "," + size + "))"
            comp = name + "=" + fline + "\n" + line
            return comp


    def _initializer(self, tree, flag=None):
        if tree.leaf:
            if tree.leaf == "block":
                x = self.flist[tree.leaf]
                try:
                    y = self.dispatch(tree.children[0],"block")
                    return x + "(" + y + ")"
                except:
                    raise Exception("Invalid Number of arguments/Argument for Block")
            if tree.leaf in self.flist:
                x = self.flist[tree.leaf]
            else:  
                x = tree.leaf
            if tree.children:
                y = self.dispatch(tree.children[0],flag)
                return (x,y)
            else:
                return x
        else:
            return self.dispatch(tree.children[0],flag)

    def _parameter_list(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)
        else:
            x = self.dispatch(tree.children[0],flag)
            y = self.dispatch(tree.children[1],flag)
            z = [x] + [y]
            return self.flatten(z)
                    # if len(tree.children) == 1:
        #     self.dispatch(tree.children)
        # else:
        #     self.dispatch(tree.children[0])
        #     self.write(",")
        #     self.dispatch(tree.children[1])

    # the following are incomplete and won't work with more complicated statements    
    def _parameter_declaration(self, tree, flag=None):
        return self.dispatch(tree.children[0],flag)

    def _declaration_list(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)
        else:
            return self.dispatch(tree.children[0],flag) + "\n" + self.dispatch(tree.children[1],flag)

    def _declaration(self, tree, flag=None):
        return self.dispatch(tree.children[0],flag)

    def _expression_statement(self,tree,flag=None):
        print "HI",self.dispatch(tree.children[0],flag)
        return self.dispatch(tree.children[0],flag)

    def _statement(self,tree,flag=None):
        return self.dispatch(tree.children[0],flag)

    def _statement_list(self,tree,flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)
        else:
            return self.dispatch(tree.children[0],flag) + self.dispatch(tree.children[1],flag)

    def _expression_statement(self,tree,flag=None):
        if len(tree.children) != 0:
            return self.dispatch(tree.children[0],flag)
        else:
            return ""

    def _compound_statement(self,tree,flag=None):
        if len(tree.children) == 0:
            return ""
        else:
            return self.dispatch(tree.children[0],flag)

    def _point_gen(self,tree,flag=None):
        self.tempPoints.add(tree.leaf)
        return tree.leaf

    def _selection_statement(self,tree,flag=None):
        if len(tree.children) == 2: # if statement
            s = "if " + self.dispatch(tree.children[0],flag) + self.enter()
            r = self.dispatch(tree.children[1],flag)
            print r
            s += self.fill(r)
            self.leave()
            return s
        else:
            return "WHAT"


