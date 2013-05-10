import sys
import StringIO
import types

class Traverse(object):

    def __init__(self, tree, file = sys.stdout):
        self.f = file
        self.flist = {"Flatmap": "Flatmap",
                      "block": "materials.blockWithID", 
                      "add": "fillBlocks",
                      "close": "saveInPlace"}
        self.fargs = {"Flatmap": [str, int, int, int]}
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
        self.values = {}
        self.waitingfor = set()
        self._indent = 0
        self.x = self.dispatch(tree)
        self.f.write("")
        self.f.flush()

    def fill(self, text = ""):
        "Indent a piece of text, according to the current indentation level"
        s = ""
        buf = StringIO.StringIO(text)
        for line in buf:
            s+= "    "*self._indent + line 
        return s

    def getpython(self):
        print self.symbols
        print self.values
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
        elif len(tree.children) == 1: # It is a point
            return self.dispatch(tree.children[0],flag)
        else:
            return "0"

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
        else:
            if len(tree.children)==1:
                s = self.dispatch(tree.children[0],flag)
                s = self.listtoparams(s)
                print s
            else:
                s = ""
            return tree.leaf + "(" + s + ")"

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
        #print x
        if not tree.leaf:
            return x
        else:
            if type(x) is tuple:
                if x[0] == "Flatmap": 
                    self.symbols[tree.leaf] = "MAP" # add to symbol table
                    return self.flatmap_method(tree.leaf, x[1])
                elif x[0] == "Point":
                    self.symbols[tree.leaf] = "POINT"
                    return self.point_method(tree.leaf, x[1])
            else: # assigning a point right now
                if x in self.tempPoints:
                    self.symbols[tree.leaf] = "POINT"
                    self.tempPoints.remove(x)
                elif self.isNum(x): # int or string
                    self.symbols[tree.leaf] = "INT"
                    self.values[tree.leaf] = self.isNum(x)
                else:
                    self.symbols[tree.leaf] = "STRING"
                return tree.leaf + "=" + x

    def listtoparams(self,l,x=None):
        s = ""
        comma = False
        for a in l:
            if comma:
                s += ","
            else:
                comma = True
            s += a
            if x:
                self.waitingfor.add(a)
        return s

    def _logical_or_expression(self,tree,flag=None):
        if tree.leaf:
            s = self.dispatch(tree.children[0],flag) + " or " + self.dispatch(tree.children[1],flag)
            return s
        return self.dispatch(tree.children[0],flag)

    def _logical_and_expression(self,tree,flag=None):
        if tree.leaf:
            s = self.dispatch(tree.children[0],flag) + " and " + self.dispatch(tree.children[1],flag)
            return s
        return self.dispatch(tree.children[0],flag)

    def _equality_expression(self,tree,flag=None):
        if tree.leaf:
            s = self.dispatch(tree.children[0],flag) + tree.leaf + self.dispatch(tree.children[1],flag)
            return s
        return self.dispatch(tree.children[0],flag)

    def _relational_expression(self,tree,flag=None):
        if tree.leaf:
            s = self.dispatch(tree.children[0],flag) + tree.leaf + self.dispatch(tree.children[1],flag)
            return s
        return self.dispatch(tree.children[0],flag)

    def _additive_expression(self,tree,flag=None):
        if tree.leaf:
            s = self.dispatch(tree.children[0],flag) + tree.leaf + self.dispatch(tree.children[1],flag)
            return s
        return self.dispatch(tree.children[0],flag)

    def _multiplicative_expression(self,tree,flag=None):
        if tree.leaf:
            s = self.dispatch(tree.children[0],flag) + tree.leaf + self.dispatch(tree.children[1],flag)
            return s
        return self.dispatch(tree.children[0],flag)

    def flatmap_method(self, name, param):
        if len(param) != 4:
            raise Exception("Wrong number of params passed to Flatmap")
        elif not (self.checkint(param[1]) and self.checkint(param[2]) and self.checkint(param[3])):
            raise Exception("Parameters passed were not integers for map size")
        else:
            if self.getint(param[1]) and self.getint(param[2]) and self.getint(param[3]):
                sizex = self.getint(param[1])
                sizey = self.getint(param[2])
                sizez = self.getint(param[3])
                x = str(int(int(sizex) * 1/2 * -1))
                y = str(0)
                z = str(int(int(sizez) * 1/2 * -1))
                if sizey > 255:
                    sizey = 255
                size = "(" + str(sizex) + "," + str(sizey) + "," + str(sizez) + ")"
                point = "(" + x + "," + y + "," + z + ")"
            else:
                point = "(" + param[1] + "*-0.5," + param[2] + "*-0.5," + param[3] + "*-0.5)"
                size = "(" + param[1] + "," + param[2] + "," + param[3] + ")"
            fline = "mclevel.MCInfdevOldLevel(" + param[0] + ", create=True)"
            line = name + ".createChunksInBox(BoundingBox(" + point + "," + size + "))"
            comp = name + "=" + fline + "\n" + line
            return comp

    def point_method(self, name, param):
        if len(param) != 3:
            raise Exception("Wrong number of params passed to Flatmap")
        elif not (self.checkint(param[0]) and self.checkint(param[1]) and self.checkint(param[2])):
            raise Exception("Parameters passed were not integers")
        else:
            self.symbols[name] = "POINT"
            return name + "=(" + param[0] + "," + param[1] + "," + param[2] + ")"
            #print self.symbols


    def checkint(self,s):
        if not s : return False
        try:
            ret = int(s)
        except ValueError:
            return self.symbols.get(s) == "INT" or s in self.waitingfor 
        return True

    def getint(self,s):
        if self.checkint(s):
            try:
                return int(s)
            except ValueError:
                return self.values.get(s)

    def num_or_str(self, x):
        """The argument is a string; convert to a number if possible, or strip it.
        >>> num_or_str('42')
        42
        >>> num_or_str(' 42x ')
        '42x'
        """
        if hasattr(x, '__int__'): return x
        try:
            return int(x) 
        except ValueError:
            try:
                return float(x) 
            except ValueError:
                    return str(x).strip() 

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
                params = self.dispatch(tree.children[0],flag)
                # initializer argument type checking
                if tree.leaf in self.fargs:
                    typed_params = [self.num_or_str(param) for param in params]
                    init_args = [type(param) for param in typed_params]
                    if init_args != self.fargs[tree.leaf]:
                        print "Initializer Type Check Error"
                return (x, params)
            else:
                return x
        else:
            return self.dispatch(tree.children[0],flag)

    def _parameter_list(self, tree, flag=None): # HAVE TO HANDLE FUNCTION PARAMETERS
        if len(tree.children) == 0:
            return ""
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
        #print "HI",self.dispatch(tree.children[0],flag)
        return self.dispatch(tree.children[0],flag)

    def _statement(self,tree,flag=None):
        return self.dispatch(tree.children[0],flag)

    def _statement_list(self,tree,flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)
        else:
            return self.dispatch(tree.children[0],flag) + "\n" + self.dispatch(tree.children[1],flag)

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
            s = "if " + self.dispatch(tree.children[0],flag) + ":\n"
            r = self.dispatch(tree.children[1],flag)
            # adding the indent yo
            self.enter()
            s += self.fill(r)
            self.leave()
            return s
        else:
            s = "if " + self.dispatch(tree.children[0],flag) + ":\n"
            r = self.dispatch(tree.children[1],flag)
            self.enter()
            s += self.fill(r + "\n")
            self.leave()
            s+= "else:\n"
            t = self.dispatch(tree.children[2],flag)
            self.enter()
            s += self.fill(t)
            self.leave()
            return s

    def _iteration_statement(self,tree,flag=None):
        if len(tree.children) == 2: # while statement
            s = "while " + self.dispatch(tree.children[0],flag) + ":\n"
            r = self.dispatch(tree.children[1],flag)
            # adding the indent yo
            self.enter()
            s += self.fill(r)
            self.leave()
            return s
        else: #for statement
            return "for not implemented"

    def _external_declaration(self,tree,flag=None):
        return self.dispatch(tree.children[0],flag)

    def _translation_unit(self,tree,flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)
        else:
            s = self.dispatch(tree.children[0],flag)
            t = self.dispatch(tree.children[1],flag)
            return s + "\n\n" + t

    def _function_definition(self, tree, flag=None):
        fname = tree.leaf
        s = "def " + tree.leaf + "("
        if len(tree.children) == 2:
            p = self.dispatch(tree.children[0],flag)
            comma = False
            for a in p:
                if comma:
                    s += ","
                else:
                    comma = True
                s += a
                self.waitingfor.add(a)
            s = s + "):\n"
            #print self.waitingfor
            r = self.dispatch(tree.children[1],flag)
            self.enter()
            s += self.fill(r)
            self.leave()
            return s
        else:
            p = self.dispatch(tree.children[0],flag)
            comma = False
            for a in p:
                if comma:
                    s += ","
                else:
                    comma = True
                s += a
                self.waitingfor.add(a)
            s = s + "):"+"\n"
            return s

    def _return_statement(self, tree, flag=None):
        if tree.children:
            s = "return " + self.dispatch(tree.children[0],flag)
            return s
        return "return "

    def isNum(self, s):
        """Convert string to either int or float."""
        try:
            ret = int(s)
        except ValueError:
            return False
        return ret

    # def _parameter_list(self,tree, flag=None):
    #     if tree.children == 0:
    #         return ""
    #     else:
    #         return "SUP DAWG, HANDLE PARAMETERS NOW"


