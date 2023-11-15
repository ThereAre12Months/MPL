import datatypes as dt
import codeStructure as cs

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
            if i == 0 or char in list(" ,:;()[]{}+-*/%!=<>"):
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
                list_.append(temp)
            temp = []
        else:
            temp.append(i)

    return list_

def trim_lines(source):
    pass

def compile(code):
    c, lits = getLiterals(code + " ")
    c = split_lines(c)
    for i in c:
        print(i)
    