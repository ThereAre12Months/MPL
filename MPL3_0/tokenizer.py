class TOKENTYPES:
    INT       = 0
    FLOAT     = 1
    STRING    = 2
    LIST      = 3
    CODEBLOCK = 4
    KEYWORD   = 5
    BINOP     = 6
    SYMBOL    = 7
    VARNAME   = 8

class Token:
    def __init__(self, __type:int=TOKENTYPES.INT, __value:any=None):
        self.type = __type
        self.val  = __value

    def __str__(self):
        return f"{['INT', 'FLOAT', 'STRING', 'LIST', 'CODEBLOCK', 'KEYWORD', 'BINOP', 'SYMBOL', 'VARNAME'][self.type]}: {self.val}"

    def __repr__(self):
        return str(self)

def isInt(word:str) -> bool:
    for char in word:
        if not char in "0123456789":
            return False 
        
    return True

def isFloat(word:str) -> bool:
    dotCount = 0

    for char in word:
        if char in "0123456789":
            pass

        elif char == "." and dotCount == 0:
            dotCount += 1

        else:
            return False
        
    return True

def split(string:str, sep:str|list=" ", incl:bool=False) -> list[str]:
    if type(sep) == str:
        return string.split(sep=sep)

    items = []
    temp  = ""
    
    for char in string:
        if char in sep:
            items.append(temp)
            temp = ""

            if incl:
                items.append(char)

        else:
            temp += char

    if temp != "":
        items.append(temp)

    return items

def tokenize(file:str) -> list[list[Token]]:
    tokens:list[list[Token]] = []
    lines:list[str] = split(file, sep=";")

    keywords = (
        # loops
        "while",
        "until",
        "repeat",
        "loop",

        # functions
        "fn",

        # conditionals
        "if",
        "else",

        # variables
        "let",
        "var",
    )

    symbols = (
        # lexical symbols
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        ";",

        # variable stuff
        "=",
        ":=",
    )

    binops = (
        # values
        "+",
        "-",
        "*",
        "/",
        "**",
        "%",

        # boolean
        "==",
        "!=",
        "<",
        ">",
        "<=",
        ">=",
    )

    words = split(file, sep=list(" ,:;()[]{}\n\t\"'"), incl=True)

    inString = False
    tempString = ""

    for word_ in words:
        word = word_.strip()

        if word == "\"" or word == "'":
            if inString:
                tokens.append(Token(TOKENTYPES.STRING, tempString))
                tempString = ""

            inString = not inString


        elif inString:
            tempString += word_

        else:
            if word == "":
                pass

            elif word in keywords:
                tokens.append(Token(TOKENTYPES.KEYWORD, word))

            elif word in symbols:
                tokens.append(Token(TOKENTYPES.SYMBOL, word))

            elif word in binops:
                tokens.append(Token(TOKENTYPES.BINOP, word))

            elif isInt(word):
                tokens.append(Token(TOKENTYPES.INT, word))

            elif isFloat(word):
                tokens.append(Token(TOKENTYPES.FLOAT, word))

            else:
                tokens.append(Token(TOKENTYPES.VARNAME, word))

    return tokens
