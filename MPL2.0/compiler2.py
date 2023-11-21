import datatypes as dt
import codeStructure as cs

# CONSTANTS
splittable = list(" ,:;()[]{}+-*/%!=<>\n\t")

class Operator:
    def __init__(self, type_):
        self.t = type_

    def __repr__(self):
        return f"Op: {self.t}"
    
    @staticmethod
    def isOperator(word):
        operators = list("+-*/%<>=") + [
            "==",
            "<=",
            ">=",
            "!=",
            "**",
            "//"
        ]

        return word in operators

class Keyword:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Keyword: {self.name}"

    @staticmethod
    def isKeyword(word):
        keywords   = [
            # if-elif-else
            "if",
            # loops
            "while",
            "until",
            "repeat",
            "loop",
            # variables
            "let",
            "var"
        ]

        return word in keywords

class Reference:
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return f"Reference: {self.num}"

def isLiteralIn(l:any, l_:list):
    for i in range(len(l_)):
        if l_[i].val == l.val:
            return i
    return NotImplemented

def getLiterals(source):
    code = source

    literals = []

    # strings
    new_code = []
    temp_string = ""
    in_string = False
    for i in range(len(code)):
        match code[i]:
            case '"':
                if not in_string:
                    in_string = True
                else:
                    idx = isLiteralIn(dt.String(temp_string), literals)
                    if idx == NotImplemented:
                        literals.append(dt.String(temp_string))
                        idx = len(literals)-1
                    new_code.append(Reference(idx))
                    in_string = False
                    temp_string = ""
            case _:
                if not in_string:
                    new_code.append(code[i])
                else:
                    temp_string += code[i]

    # ints
    code = new_code.copy()
    new_code = []
    temp_int = ""
    canInt  = True
    for i in range(len(code)):
        char = code[i]
        if canInt and char in [str(i) for i in range(10)]:
            temp_int += char
                
        else:
            if i == 0 or char in splittable:
                canInt = True
            else:
                canInt = False

            if temp_int != "":
                if canInt:
                    idx = isLiteralIn(dt.Int(temp_int), literals)
                    if idx == NotImplemented:
                        literals.append(dt.Int(temp_int))
                        idx = len(literals)-1
                    new_code.append(Reference(idx))
                    temp_int = ""
                else:
                    new_code += list(temp_int)
                    temp_int = ""
            new_code.append(char)

    # floats (WIP)
    """code = new_code.copy()
    new_code = []
    floats   = []
    temp_flt = ""
    can_flt  = True
    in_float = False
    
    for i in range(len(code)):
        char = code[i]
        if in_float and char in [str(i) for i in range(10)]+["."]:
            temp_flt += char 

        else:
            if i == 0 or char in " ,:;()[]{}+-*/%!=<>":
                can_flt = True
            else:
                can_flt = False

            if in_float and temp_flt != "":
                if can_flt:
                    if not float(temp_flt) in floats:
                        floats.append(float(temp_flt))
                    new_code.append(Reference(dt.Float, floats.index(float(temp_flt))))
                    temp_flt = ""
                else:
                    new_code.append("f", *list(temp_flt))

            else:
                if char == "f":
                    if can_flt:
                        in_float = True
                    else:
                        in_float = False"""

    return new_code, literals

def split_lines(source):
    list_ = []

    temp = []
    for i in source:
        if i == ";":
            if temp != [" "] and temp != []:
                trimmed = trim_line(temp)
                if len(trimmed) > 0:
                    list_.append(trimmed)
            temp = []
        else:
            temp.append(i)

    return list_

def trim_line(source:list|tuple):
    copy = source.copy()

    while len(copy) > 0 and copy[0] in (" ", "\t", "\n"):
        copy.pop(0)

    while len(copy) > 0 and copy[-1] in (" ", "\t", "\n"):
        copy.pop(-1)

    return copy

def trim_str(source:str):
    return "".join(trim_line(list(source)))

def getVars(source:list|tuple):
    new = []

    temp = ""
    for i in source:
        if i in splittable or type(i) != str:
            trimmed = trim_str(temp)
            if trimmed != "":
                if Keyword.isKeyword(trimmed):
                    new.append(Keyword(trimmed))
                else:
                    new.append(dt.Variable(trimmed))
            temp = ""
            new.append(i)
        else:
            temp += i

    trimmed = trim_str(temp)
    if trimmed != "":
        if Keyword.isKeyword(trimmed):
            new.append(Keyword(trimmed))
        else:
            new.append(dt.Variable(trimmed))

    return new

def getOperators(source:list|tuple):
    new = []

    temp = ""
    for i in source:
        if type(i) != str:
            trimmed = trim_str(temp)
            if trimmed != "":
                if Operator.isOperator(trimmed):
                    new.append(Operator(trimmed))
                else:
                    new += list(trimmed)
            temp = ""
            new.append(i)
        else:
            temp += i

    trimmed = trim_str(temp)
    if trimmed != "":
        if Operator.isOperator(trimmed):
            new.append(Operator(trimmed))
        else:
            new += list(trimmed)

    return new

def getBrackets(literals:list, source:list|tuple):
    lits = literals.copy()
    new  = source.copy()

    length = len(source)

    while ")" in new:
        idx = new.index(")")

        start_pos = 0
        end_pos   = idx
        current_pos = end_pos

        while new[current_pos] != "(":
            current_pos -= 1

        start_pos = current_pos

        bracket = new[start_pos:end_pos+1]

        contents = []
        temp = []

        for char in bracket:
            if char != ",":
                temp.append(char)
            else:
                contents.append(trim_line(temp))
        if trim_line(temp) != []:
            contents.append(trim_line(temp))

        new_contents = []
        for c in contents:
            new_c = []
            count = 0

            while count < len(c):
                if type(c[count]) == Operator:
                    new_c.append(cs.BinOp(c[count].t, c[count-1], c[count+1]))
                    new_c.pop(-2)
                    count += 1
                else:
                    new_c.append(c[count])
                count += 1

            new_contents.append(new_c)

        if type(new[start_pos-1]) == dt.Variable
        new[start_pos:end_pos]

        # l = []
        # 
        # if len(bracket) == 5:
        # 
        # else:
        #     new[start_pos:end_pos+1] = Reference(len(lits))
        #     lits.append(dt.Tuple())

    return new, lits

    # other = src 
    # new = ""
    # count = const_count
    # brackets = []
    # 
    # while ")" in other:
    #     idx = other.index(")")
    # 
    #     start_pos = 0
    #     end_pos = idx
    #     current_pos = end_pos 
    # 
    #     while other[current_pos] != "(":
    #         current_pos -= 1
    #     start_pos = current_pos
    # 
    #     bracket = other[start_pos:end_pos+1]
    #     brackets.append("BRACKETS: " + str(bracket))
    #     new = other.replace(bracket, " $" + str(count) + " ")
    #     count += 1
    # 
    #     other = new 

def compile(code):
    c, lits = getLiterals(code + " ")
    c = getVars(c)
    c = getOperators(c)
    #c, lits = getBrackets(lits, c)
    print(lits)
    c = split_lines(c)
    for i in c:
        print(i)

    