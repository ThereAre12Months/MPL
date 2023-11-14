from datatypes import Codeblock, Vars, Variable, Function, String, Int, Float, Bool

class Tools:
    @staticmethod
    def getGenericVal(valToGet, vars:Vars):
        if type(valToGet) == Variable:
            return vars.getVal(valToGet)
        if type(valToGet) == BinOp:
            return valToGet._eval(vars)
        return valToGet
    
    @staticmethod
    def toString(val, vars:Vars):
        v = Tools.getGenericVal(val, vars)
        if hasattr(v, "_toString"):
            return v._toString()
        return String(v.val)

class AddVar:
    def __init__(self, scope:str, name:str, val:any) -> None:
        self.scope = scope
        self.name = name
        self.val = val

    def _call(self, vars:Vars):
        if self.scope == "global":
            vars.addVar(self.name, self.val, scope=0)
        else:
            vars.addVar(self.name, self.val)

class SetVar:
    def __init__(self, name:str, val:any) -> None:
        self.name = name
        self.val  = val

    def _call(self, vars:Vars):
        vars.setVar(self.name, self.val)

class UnOp:
    def __init__(self, type_, val):
        self.t = type_
        self.v = val

    def _eval(self, vars:Vars):
        val = Tools.getGenericVal(self.v, vars)

        if self.t == "neg":
            if not type(val) in (String, Int, Float, Bool):
                raise Exception(f"Can't negate value of type '{type(val).__name__}'")
            
            if type(val) == String:
                return String(val.val[::-1])
            if type(val) == Int:
                return Int(-val.val)
            if type(val) == Float:
                return Float(-val.val)
            if type(val) == Bool:
                return Bool(not val.val)
            

class BinOp:
    def __init__(self, type_, val1, val2):
        self.t = type_

        self.v1 = val1
        self.v2 = val2

    def _eval(self, vars:Vars):
        val1 = Tools.getGenericVal(self.v1, vars)
        val2 = Tools.getGenericVal(self.v2, vars)

        if self.t == "add":
            sol = NotImplemented
            if hasattr(val1, "_add"):
                sol = val1._add(val2)

                if sol != NotImplemented:
                    return sol
                
                if hasattr(val2, "_add"):
                    sol = val2._add(val1)

                    if sol != NotImplemented:
                        return sol
                    
            raise Exception(f"Can't add '{type(val1).__name__}' and '{type(val2).__name__}'.")
        
        elif self.t == "sub":
            sol = NotImplemented
            if hasattr(val1, "_sub"):
                sol = val1._sub(val2)

                if sol != NotImplemented:
                    return sol
                    
            raise Exception(f"Can't subtract '{type(val2).__name__}' from '{type(val1).__name__}'.")

        elif self.t == "mul":
            sol = NotImplemented
            if hasattr(val1, "_mul"):
                sol = val1._mul(val2)

                if sol != NotImplemented:
                    return sol
                
                if hasattr(val2, "_mul"):
                    sol = val2._mul(val1)

                    if sol == NotImplemented:
                        return sol
                    
            raise Exception(f"Can't multiply '{type(val1).__name__}' and '{type(val2).__name__}'.")
        
        elif self.t == "div":
            sol = NotImplemented
            if hasattr(val1, "_div"):
                sol = val1._div(val2)

                if sol != NotImplemented:
                    return sol
                    
            raise Exception(f"Can't divide '{type(val2).__name__}' from '{type(val1).__name__}'.")
        
        elif self.t == "mod":
            sol = NotImplemented
            if hasattr(val1, "_mod"):
                sol = val1._mod(val2)

                if sol != NotImplemented:
                    return sol
                    
            raise Exception(f"Can't take the mod of '{type(val2).__name__}' and '{type(val1).__name__}'.")
        
        elif self.t == "pow":
            sol = NotImplemented
            if hasattr(val1, "_pow"):
                sol = val1._pow(val2)

                if sol != NotImplemented:
                    return sol
                    
            raise Exception(f"Can't take the power of '{type(val2).__name__}' and '{type(val1).__name__}'.")
        
        elif self.t == "eq":
            if hasattr(val1, "_eq"):
                return val1._eq(val2)
            if hasattr(val2, "_eq"):
                return val2._eq(val1)
            return Bool(False)
        
        elif self.t == "neq":
            if hasattr(val1, "_eq"):
                return Bool(not val1._eq(val2).val)
            if hasattr(val2, "_eq"):
                return Bool(not val2._eq(val1).val)
            return Bool(True)

class Conditional:
    def __init__(self, op:UnOp|BinOp):
        self.op = op

    def _eval(self, vars:Vars):
        return self.op._eval(vars)

    def _test(self, vars:Vars):
        return Bool(self.op._eval(vars).val)

class If:
    def __init__(self, conditional:Conditional, code:Codeblock):
        self.conditional = conditional
        self.code = code
    
    def _call(self, vars:Vars):
        if self.conditional._test(vars).val:
            self.code._call(vars)

class BuiltinFunctionCall:
    def __init__(self, name, args=None, kwargs=None):
        self.name = name
        self.args = args or []
        self.kwargs = kwargs or {}

    def _call(self, vars:Vars):
        match self.name:
            case "out":
                v = []
                for a in self.args:
                    v.append(Tools.toString(a, vars).val)

                print(" ".join(v))

class FunctionCall:
    def __init__(self, name, args=None, kwargs=None):
        self.name   = name
        self.args   = args or []
        self.kwargs = kwargs or {}

    def _call(self, vars:Vars):
        func:Function = vars.getVal(self.name)
        func._call(vars, self.args, self.kwargs)
        