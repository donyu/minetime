import sys

class Traverse:

    def __init__(self, tree, file = sys.stdout):
        self.f = file
        self.flist = {"Flatmap": "Flatmap","block": "materials.blockWithID", "add": "fillBlocks", "close": "saveInPlace"}
        self.blocks = {"COBBLE": 4, "AIR": 0, "STONE": 1, "GRASS":2, "DIRT": 3}
        self.future_imports = []
        self._indent = 0
        self.dispatch(tree)
        self.f.write("")
        self.f.flush()

    def fill(self, text = ""):
        "Indent a piece of text, according to the current indentation level"
        self.f.write("\n"+"    "*self._indent + text)

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
        self.write(":")
        self._indent += 1

    def leave(self):
        "Decrease the indentation level."
        self._indent -= 1

    def dispatch(self, tree, flag=None):
        "Dispatcher function, dispatching tree type T to method _T."
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return
        meth = getattr(self, "_"+tree.type)
        x = meth(tree,flag)
        return x

    def _primary_expression(self,tree,flag=None):
        if tree.leaf in self.blocks:
            return str(self.blocks[tree.leaf])
        else:
            return str(tree.leaf)

    def _class_method_expression(self,tree,flag=None):
        s = tree.leaf
        a = self.dispatch(tree.children[0],s)
        return a

    def _function_expression(self,tree,flag=None): # not complete
        if tree.leaf == "add":
            return self.add_method(tree,flag)
        elif tree.leaf in self.flist:
            return flag + "." + self.flist[tree.leaf] + "()"

    def add_method(self,tree,flag=None):
        a = flag + "." + self.flist[tree.leaf] + "("
        x = self.dispatch(tree.children[0])
        p1 = "box.BoundingBox(origin=" + x[2] + ",size=(1,1,1)),"
        p2 = flag + "." + x[0] + "(" + x[1] + ")"
        a+= p1 + p2 + ")"
        return a

    def _expression(self,tree,flag=None):
        print self.dispatch(tree.children[0])

    def _assignment_expression(self, tree,flag=None):
        [x,y] = self.dispatch(tree.children[0])
        if x == "Flatmap":
            return self.flatmap_method(tree.leaf, y)

    def flatmap_method(self, name, param):
        if len(param) > 4:
            raise Exception("Wrong num of params")
        else:
            s = '''
MC_DIR = "~/.minecraft/saves"
saves = os.path.expanduser(MC_DIR)
worldpath = os.path.join(saves,''' 
            worldname = param[0]
            s += worldname + ")"
            sizex = param[1]
            sizey = 100
            sizez = param[2]
            x = str(int(int(sizex) * 1/2 * -1))
            y = str(0)
            z = str(int(int(sizez) * 1/2 * -1))
            if sizey > 255:
                sizey = 255
            point = "(" + x + "," + y + "," + z + ")"
            size = "(" + str(sizex) + "," + str(sizey) + "," + str(sizez) + ")"
            fline = "mclevel.MCInfdevOldLevel(worldpath, create=True)"
            line = "chunk_box = box.BoundingBox(" + point + "," + size + ")"
            comp = name + "=" + fline + "\n" + line + "\n"
            createchunk = name + ".createChunksInBox(chunk_box)"
            s = s + "\n" + comp + createchunk
        return s


    def _initializer(self, tree, flag=None):
        if tree.leaf in self.flist:
            x = self.flist[tree.leaf]
        else:  
            x = tree.leaf
        if tree.children:
            y = self.dispatch(tree.children[0])
            return (x,y)
        return x

    def _parameter_list(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            x = self.dispatch(tree.children[0])
            y = self.dispatch(tree.children[1])
            z = [x] + [y]
            return self.flatten(z)
                    # if len(tree.children) == 1:
        #     self.dispatch(tree.children)
        # else:
        #     self.dispatch(tree.children[0])
        #     self.write(",")
        #     self.dispatch(tree.children[1])

    def _parameter_declaration(self, tree, flag=None):
        return self.dispatch(tree.children[0])




