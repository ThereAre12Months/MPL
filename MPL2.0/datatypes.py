class String:
    def __init__(self, val:str):
        self.val = str(val)

    def copy(self):
        return String(self.val)

    def toString(self):
        return self.copy()
    
    def toInt(self):
        return Int(self.val)
    
    def toFloat(self):
        return Float(self.val)
    
    def toBool(self):
        return Bool(self.val)
        
class Int:
    def __init__(self, val:int):
        self.val = int(val)

    def copy(self):
        return Int(self.val)
    
    def toString(self):
        return String(self.val)
    
    def toInt(self):
        return self.copy()
    
    def toFloat(self):
        return Float(self.val)
    
    def toBool(self):
        return Bool(self.val)

class Float:
    def __init__(self, val:float):
        self.val = float(val)

    def copy(self):
        return Float(self.val)
    
    def toString(self):
        return String(self.val)
    
    def toInt(self):
        return Int(self.val)
    
    def toFloat(self):
        return Float(self.val)
    
    def toBool(self):
        return Bool(self.val)

class Bool:
    def __init__(self, val:bool):
        self.val = bool(val)

    def copy(self):
        return Bool(self.val)
    
    def toString(self):
        return String(self.val)
    
    def toInt(self):
        return Int(self.val)
    
    def toFloat(self):
        return Float(self.val)
    
    def toBool(self):
        return Bool(self.val)
