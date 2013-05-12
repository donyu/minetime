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
        # function argument types for type-checking
        self.fargs = {"Flatmap": [str, int, int, int],
                      "Point": [int, int, int]}
        self.class_meths = {"Flatmap": {
                                'add': ['block', 'Point'], 
                                'close': []
                                }
                            }
        # will be used for scope checking 
        self.var_scopes = [[]]
        self.scope_depth = 0
        self.flistsymbol = {"close" : "MAP"}
        self.blocks = {"STONE":1,
                       "GRASS":2,
                       "DIRT":3,
                       "COBBLESTONE":4,
                       "WOODENPLANK":5,
                       "SAPLING":6,
                       "BEDROCK":7,
                       "WATER":8,
                       "WATER":9,
                       "LAVA":10,
                       "LAVA":11,
                       "SAND":12,
                       "GRAVEL":13,
                       "GOLDORE":14,
                       "IRONORE":15,
                       "COALORE":16,
                       "WOOD":17,
                       "LEAVES":18,
                       "SPONGE":19,
                       "GLASS":20,
                       "LAPISLAZULIORE":21,
                       "LAPISLAZULIBLOCK":22,
                       "DISPENSER":23,
                       "SANDSTONE":24,
                       "NOTEBLOCK":25,
                       "BED":26,
                       "POWEREDRAIL":27,
                       "DETECTORRAIL":28,
                       "STICKYPISTON":29,
                       "COBWEB":30,
                       "TALLGRASS":31,
                       "DEADSHRUB":32,
                       "PISTON":33,
                       "PISTON":34,
                       "WOOL":35,
                       "PISTON":36,
                       "DANDELION":37,
                       "ROSE":38,
                       "BROWNMUSHROOM":39,
                       "REDMUSHROOM":40,
                       "BLOCKOFGOLD":41,
                       "BLOCKOFIRON":42,
                       "STONESLAB":43,
                       "STONESLAB":44,
                       "BRICK":45,
                       "TNT":46,
                       "BOOKCASE":47,
                       "MOSSSTONE":48,
                       "OBSIDIAN":49,
                       "TORCH":50,
                       "FIRE":51,
                       "MOBSPAWNER":52,
                       "WOODENSTAIRS":53,
                       "CHEST":54,
                       "REDSTONEWIRE":55,
                       "DIAMONDORE":56,
                       "BLOCKOFDIAMOND":57,
                       "WORKBENCH":58,
                       "WHEAT":59,
                       "FARMLAND":60,
                       "FURNACE":61,
                       "FURNACE":62,
                       "SIGN":63,
                       "WOODDOOR":64,
                       "LADDER":65,
                       "RAIL":66,
                       "COBBLESTONESTAIRS":67,
                       "SIGN":68,
                       "LEVER":69,
                       "STONEPRESSUREPLATE":70,
                       "IRONDOOR":71,
                       "WOODENPRESSUREPLATE":72,
                       "REDSTONEORE":73,
                       "REDSTONEORE":74,
                       "REDSTONETORCH":75,
                       "REDSTONETORCH":76,
                       "BUTTON":77,
                       "SNOW":78,
                       "ICE":79,
                       "SNOWBLOCK":80,
                       "CACTUS":81,
                       "CLAYBLOCK":82,
                       "SUGARCANE":83,
                       "JUKEBOX":84,
                       "FENCE":85,
                       "PUMPKIN":86,
                       "NETHERRACK":87,
                       "SOULSAND":88,
                       "GLOWSTONE":89,
                       "PORTAL":90,
                       "JACKOLANTERN":91,
                       "CAKE":92,
                       "REDSTONEREPEATER":93,
                       "REDSTONEREPEATER":94,
                       "LOCKEDCHEST":95,
                       "TRAPDOOR":96,
                       "SILVERFISHSTONE":97,
                       "STONEBRICKS":98,
                       "BROWNMUSHROOM":99,
                       "REDMUSHROOM":100,
                       "IRONBARS":101,
                       "GLASSPANE":102,
                       "MELON":103,
                       "PUMPKINVINE":104,
                       "MELONVINE":105,
                       "VINES":106,
                       "FENCEGATE":107,
                       "BRICKSTAIRS":108,
                       "STONEBRICKSTAIRS":109,
                       "MYCELIUM":110,
                       "LILYPAD":111,
                       "NETHERBRICK":112,
                       "NETHERBRICKFENCE":113,
                       "NETHERBRICKSTAIRS":114,
                       "NETHERWART":115,
                       "ENCHANTMENTTABLE":116,
                       "BREWINGSTAND":117,
                       "CAULDRON":118,
                       "ENDPORTAL":119,
                       "ENDPORTALFRAME":120,
                       "ENDSTONE":121,
                       "DRAGONEGG":122,
                       "REDSTONELAMP":123,
                       "REDSTONELAMP":124,
                       "OAKWOODSLAB":125,
                       "COCAPLANT":127,
                       "SANDSTONESTAIRS":128,
                       "EMERALDORE":129,
                       "ENDERCHEST":130,
                       "TRIPWIREHOOK":131,
                       "TRIPWIRE":132,
                       "BLOCKOFEMERALD":133,
                       "WOODENSTAIRS":134,
                       "WOODENSTAIRS":135,
                       "WOODENSTAIRS":136,
                       "COMMANDBLOCK":137,
                       "BEACON":138,
                       "COBBLESTONEWALL":139,
                       "FLOWERPOT":140,
                       "CARROT":141,
                       "POTATOES":142,
                       "BUTTON":143,
                       "HEADBLOCK":144,
                       "ANVIL":145,
                       "TRAPPEDCHEST":146,
                       "WEIGHTEDPRESSUREPLATE":147,
                       "WEIGHTEDPRESSUREPLATE":148,
                       "REDSTONECOMPARATOR":149,
                       "REDSTONECOMPARATOR":150,
                       "DAYLIGHTSENSOR":151,
                       "BLOCKOFREDSTONE":152,
                       "NETHERQUARTZORE":153,
                       "HOPPER":154,
                       "QUARTZBLOCK":155,
                       "QUARTZSTAIRS":156,
                       "ACTIVATORRAIL":157,
                       "DROPPER":158,
                       "HAYBALE":170,
                       "CARPET":171,
                       "HARDENEDCLAY":172
                       }
        self.relops = {'<', '>', '<=', '>=', '==', '!=',
                       '+', '-', '*', '/', '%'}
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
        "Print ':', and increase the indentation and create a new scope"
        # initialize depth
        self.scope_depth += 1
        self.var_scopes.append([])
        self._indent += 1
        return ":"

    def leave(self):
        "Decrease the indentation level and remove out-of-scope symbols"
        # remove symbols from this scope and then return s
        for var in self.var_scopes[self.scope_depth]:
            del self.symbols[var]
            if var in self.values:
                del self.values[var]
        del self.var_scopes[self.scope_depth]
        self.scope_depth -= 1
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
        elif tree.leaf == "true":
            return "True"
        elif tree.leaf == "false":
            return "False"
        elif tree.leaf:
            print str(tree.leaf)
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
                params = self.dispatch(tree.children[0],flag)
                print params, " hi"
                s = self.listtoparams(params)
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
            # add x to the scoping dict to be removed when out of scope
            self.var_scopes[self.scope_depth].append(tree.leaf)
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
                    self.symbols[tree.leaf] = int
                    self.values[tree.leaf] = self.isNum(x)
                else:
                    self.symbols[tree.leaf] = str
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
                print params
                # initializer argument type checking
                if tree.leaf in self.fargs:
                    typed_params = [self.num_or_str(param) for param in params]
                    init_args = [type(param) for param in typed_params]
                    if init_args != self.fargs[tree.leaf]:
                        print "Initializer Type Check Error for", tree.leaf
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
            s = self.dispatch(tree.children[0],flag) + "\n" + "while " + self.dispatch(tree.children[1],flag)  + ":\n"
            r = self.dispatch(tree.children[3],flag) + "\n" + self.dispatch(tree.children[2],flag)
            # adding the indent yo
            self.enter()
            s += self.fill(r)
            self.leave()
            return s

    def _external_declaration(self,tree,flag=None):
        return self.dispatch(tree.children[0],flag)

    def _translation_unit(self,tree,flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)
        else:
            s = self.dispatch(tree.children[0],flag)
            t = self.dispatch(tree.children[1],flag)
            return s + "\n\n" + t

    def get_param_types(self, params, tree):
        ''' will return a list of type objects'''
        typed_params = []
        for param in params:
            typed_params.append(self.get_param_type(param, tree))
        return typed_params

    def get_param_type(self, param, tree):
        '''traverse tree until we find spot where param has to be certain type'''
        if tree.leaf == param:
            return True
        for child in tree.children:
            ret_val = self.get_param_type(param, child)
            if ret_val:
                if tree.leaf in self.relops:
                    params = self.dispatch(tree.children[0])
                    return int
                if tree.leaf in self.fargs:
                    params = self.dispatch(tree.children[0])
                    print param
                    print "hi " + params
                return ret_val

    def _function_definition(self, tree, flag=None):
        # initialize depth
        self.scope_depth += 1
        self.var_scopes.append([])

        # dispatch tree now
        fname = tree.leaf
        s = "def " + tree.leaf + "("
        if len(tree.children) == 2:
            params = self.dispatch(tree.children[0],flag)
            print params
            # find out the necessary types for this new function
            self.fargs[fname] = self.get_param_types(params, tree.children[1])
            comma = False
            for a in params:
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


