from datatypes import *

class Vars:
    def __init__(self):
        self.reset()

    def reset(self):
        self.scopes = [{}]

    def addVar(self, varName, defaultVal=None, scope:int=-1):
        self.scopes[scope].update({varName:defaultVal})

    def addScope(self):
        self.scopes.append({})

    def rmScope(self):
        self.scopes.pop(-1)

    def getVal(self, varName):
        for scope in reversed(self.scopes):
            if varName in list(scope.keys()):
                return scope[varName]
            
        raise NameError(f"Variable '{varName}' doesn't exist!")

class Tree:
    def __init__(self, nodes:list|None=None):
        self.nodes = nodes or list()

    def addNode(self, node):
        self.nodes.append(node)

    def run(self):
        for node in self.nodes:
            node()

class Tools:
    @staticmethod
    def getGenericVal(val, vars:Vars):
        if type(val) == str:
            vars.getVal(val)
        else:
            return val

class FunctionCall:
    def __init__(self, funcName:str, args:list=None, kwargs:dict=None):
        self.name   = funcName
        self.args   = args or []
        self.kwargs = kwargs or []

    def __call__(self, vars:Vars):
        func = vars.getVal(self.name)

        actualArgs   = [Tools.getGenericVal(arg, vars) for arg in self.args]
        actualKwargs = {(key, Tools.getGenericVal(val, vars)) for (key, val) in self.kwargs}

        func(*actualArgs, **actualKwargs)