from typing import Literal
import struct

def auto(idx=[0]):
    idx[0] += 1
    return idx[0] - 1

class Constant:
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    CONST_POINTER = auto()

    def isbool(value:str) -> bool:
        return value in {"true", "false"}

    def isint(value:str) -> bool:
        if value.count("_") == len(value):
            return False

        if not all(char in "0123456789_" for char in value):
            return False
        
        return True
    
    def isfloat(value:str) -> bool:
        if value.count("_") == len(value):
            return False

        if not all(char in "0123456789_." for char in value):
            return False
        
        if value.count(".") > 1:
            return False
        
        return True

    def __init__(self, constant_type, value):
        self.type  = constant_type
        self.value = value

    def __hash__(self):
        return hash((self.type, self.value))

    def __repr__(self):
        return f"Constant(type={self.type}, value={self.value})"
    
    def simple_repr(self):
        if self.type == Constant.STRING:
            return f"\"{self.value}\""
        return str(self.value)
    
class Keyword:
    keywords = {
        # Variables
        "bool", "i8", "i16", "i32", "i64", "f16", "f32", "f64",

        # Conditionals
        "if", "elif", "else",

        # Loops
        "loop", "repeat", "while", "until", "for", "continue", "break",

        # Functions
        "fn", "return",
    }

    @staticmethod
    def iskeyword(name: str) -> bool:
        return name in Keyword.keywords
    
    @property
    def precedence(self) -> int:
        return -1

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Keyword):
            return self.name == other.name
        return False

    def __repr__(self):
        return f"Keyword(name=\"{self.name}\")"
    
    def simple_repr(self):
        return self.name

class Identifier:
    @staticmethod
    def isidentifier(name: str) -> bool:
        return not(Constant.isfloat(name)) and not(Constant.isbool(name)) and not Keyword.iskeyword(name) and all(not (char in Operator.OPS()) for char in name)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Identifier(name=\"{self.name}\")"
    
    def simple_repr(self):
        return self.name
    
class Operator:
    BIN_OPS = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">="}
    UN_OPS = {"-", "!"}
    SYMBOLS = {"(", ")", "{", "}", "[", "]", ",", ";"}

    OP_PRECEDENCE = {
        # Variable assignment
        "="  : 0,
        "+=" : 0,
        "-=" : 0,
        "*=" : 0,
        "/=" : 0,
        "%=" : 0,
        "**=": 0,

        # Boolean operators
        "==": 1,
        "!=": 1,
        "<" : 1,
        ">" : 1,
        "<=": 1,
        ">=": 1,

        # Arithmetic operators
        "+" : 2,
        "-" : 2,
        "*" : 3,
        "/" : 3,
        "%" : 3,
        "**": 4,

    }

    @staticmethod
    def OPS():
        return Operator.BIN_OPS | Operator.UN_OPS | Operator.SYMBOLS

    @staticmethod
    def isoperator(name: str) -> bool:
        return name in Operator.OPS()

    def __init__(self, name: str, precedence_override: int = None):
        if precedence_override is not None:
            self.precedence = precedence_override
        else:
            self.precedence = Operator.OP_PRECEDENCE.get(name, -1)
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Operator):
            return self.name == other.name
        return False

    def __repr__(self):
        return f"Operator(name=\"{self.name}\")"
    
    def simple_repr(self):
        return self.name
    
def identify_token(token: str):
    if Keyword.iskeyword(token):
        return Keyword(token)
    elif Identifier.isidentifier(token):
        return Identifier(token)
    
    elif Operator.isoperator(token):
        return Operator(token)
    
    elif Constant.isbool(token):
        return Constant("bool", token == "true")
    elif Constant.isint(token):
        return Constant("i32", int(token))
    elif Constant.isfloat(token):
        return Constant("f32", float(token))
    elif token.startswith('"') and token.endswith('"'):
        return Constant("str", token[1:-1])
    else:
        raise ValueError(f"Unknown token type for: {token}")

def split_code(code: str) -> list[str]:
    text_split = " \n\t,;(){}[]\"'"
    splitted = []
    
    temp_token = ""
    for char in code:
        if char in text_split:
            if temp_token:
                splitted.append(temp_token)
                temp_token = ""

            splitted.append(char)            
        else:
            temp_token += char

    if temp_token:
        splitted.append(temp_token)
        temp_token = ""
    
    return splitted

def tokenize(code: str):
    splitted = split_code(code)

    tokens = []
    temp_token = ""
    in_string = False
    for token in splitted:
        if token == "\"":
            in_string = not in_string

            if not in_string:
                tokens.append(Constant(Constant.STRING, temp_token))
                temp_token = ""

            continue

        if in_string:
            temp_token += token
            continue

        if token.isspace():
            continue

        try:
            token_obj = identify_token(token)
            tokens.append(token_obj)
        except ValueError:
            raise ValueError(f"Unknown token type for: {token}")
    
    return tokens