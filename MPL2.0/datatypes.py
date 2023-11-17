#import codeStructure as cs

class Vars:
    def __init__(self):
        self.scopes = [{}]

    def addScope(self, startVars:dict|None = None):
        self.scopes.append(startVars or {})

    def delScope(self):
        if len(self.scopes) > 1:
            self.scopes.pop(-1)

    def addVar(self, name, val, scope=-1):
        self.scopes[scope].update({name.name : val})

    def delVar(self, name, scope=-1):
        self.scopes[scope].pop(name.name)

    def setVar(self, name, val):
        for i in range(len(self.scopes)):
            if name.name in tuple(self.scopes[-i].keys()):
                self.scopes[-i][name.name] = val 
                return
        
        raise Exception(f"Variable '{name.name}' does not exist in this scope.")

    def getVal(self, name):
        for i in range(len(self.scopes)):
            if name.name in tuple(self.scopes[-i].keys()):
                return self.scopes[-i][name.name]
        
        raise Exception(f"Variable '{name.name}' does not exist in this scope.")

class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Var: {self.name}"

class String:
    def __init__(self, val:str):
        self.val = str(val)

    def __repr__(self):
        return f"String: '{self.val}'"

    def _copy(self):
        return String(self.val)

    def _toString(self):
        return self._copy()
    
    def _toInt(self):
        return Int(self.val)
    
    def _toFloat(self):
        return Float(self.val)
    
    def _toBool(self):
        return Bool(self.val)
    
    def _add(self, val):
        if type(val) != String:
            return NotImplemented
        
        return String(self.val + val.val)
    
    def _eq(self, val):
        if type(val) != String:
            return Bool(False)
        return Bool(self.val == val.val)
        
class Int:
    def __init__(self, val:int):
        self.val = int(val)

    def __repr__(self):
        return f"Int: {self.val}"

    def _copy(self):
        return Int(self.val)
    
    def _toString(self):
        return String(self.val)
    
    def _toInt(self):
        return Int(self.val)
    
    def _toFloat(self):
        return Float(self.val)
    
    def _toBool(self):
        return Bool(self.val)
    
    def _add(self, val):
        if not type(val) in (Int, Float, Bool):
            return NotImplemented
        
        if type(val) == Int:
            return Int(self.val + val.val)
        if type(val) == Float:
            return Float(self.val + val.val)
        return Int(self.val + int(val.val))

    def _sub(self, val):
        if not type(val) in (Int, Float, Bool):
            return NotImplemented
        
        if type(val) == Int:
            return Int(self.val - val.val)
        if type(val) == Float:
            return Float(self.val - val.val)
        return Int(self.val - int(val.val))
    
    def _eq(self, val):
        if not type(val) in (Int, Float, Bool):
            return Bool(False)
        return Bool(self.val == val.val)

class Float:
    def __init__(self, val:float):
        self.val = float(val)

    def __repr__(self):
        return f"Float {self.val}"

    def _copy(self):
        return Float(self.val)
    
    def _toString(self):
        return String(self.val)
    
    def _toInt(self):
        return Int(self.val)
    
    def _toFloat(self):
        return Float(self.val)
    
    def _toBool(self):
        return Bool(self.val)
    
    def _eq(self, val):
        if not type(val) in (Int, Float, Bool):
            return Bool(False)
        return Bool(self.val == val.val)

class Bool:
    def __init__(self, val:bool):
        self.val = bool(val)

    def __repr__(self):
        return f"Bool: {'true' if self.val else 'false'}"

    def _copy(self):
        return Bool(self.val)
    
    def _toString(self):
        return String("true" if self.val else "false")
    
    def _toInt(self):
        return Int(self.val)
    
    def _toFloat(self):
        return Float(self.val)
    
    def _toBool(self):
        return Bool(self.val)
    
    def _eq(self, val):
        if not type(val) in (Bool, Int, Float):
            return Bool(False)
        
        return Bool(self.val == val.val)

class NamedArgs:
    def __init__(self, args:list|tuple|None = None, kwargs:dict|None=None):
        self.args:list|tuple = args or []
        self.kwargs:dict     = kwargs or {}

class Codeblock:
    def __init__(self, lines:list|tuple|None=None):
        self.lines = lines or []

    def _call(self, vars):
        for i in self.lines:
            i._call(vars)

class Function:
    def __init__(self, args:NamedArgs, code:Codeblock):
        self.args:NamedArgs = args
        self.code:Codeblock = code

    def _match(self, args:list|tuple, kwargs:dict):
        if not len(self.args.args) == len(args):
            if len(self.args.args) > len(args):
                raise Exception(f"Function needs at least {len(self.args.args)} argument(s), {len(args)} given.")
            raise Exception(f"Function handles at most {len(self.args.args)} positional argument(s), {len(args)} given.")
        
        argsDict = {}
        for i in range(len(args)):
            argsDict.update({self.args.args[i] : args[i]})

        kwargsDict = self.args.kwargs.copy()
        for key in tuple(kwargs.keys()):
            if not key in tuple(kwargsDict.keys()):
                raise Exception(f"Function '{self.name}' does not contain a keyword argument named: '{key}'.")
            kwargsDict.update({key : kwargs[key]})

        return argsDict | kwargsDict

    def _call(self, vars:Vars, args:list|tuple, kwargs:dict):
        startVars = self._match(args, kwargs)

        vars.addScope(startVars=startVars)
        self.code._call(vars)