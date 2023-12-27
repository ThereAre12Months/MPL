import struct

class codeblock:
    def __init__(self, val):
        self.v = val

class fnref:
    def __init__(self, val):
        self.v = val

def getInfo(const:str) -> any:
    idx = const.index(": ")
    type_ = const[:idx]
    value = const[idx+2:]

    if type_ == "STR":
        value.replace("\\n", "\n")
        return str(value)
    
    elif type_ == "INT":
        return int(value)
    
    elif type_ == "FLOAT":
        return float(value)
    
    elif type_ == "BRACKETS":
        return list(value)
    
    elif type_ == "CODE":
        return codeblock(value)
    
    elif type_ == "FNREF":
        return fnref(value)

    return value

def getNumSlots(num:int):
    slots = []
    temp = ""

    for char in hex(num).replace("0x", ""):
        if len(temp) == 1:
            temp += char 
        else:
            slots.append(int(temp, 16))
            temp = char

    while len(slots) < 4:
        slots.append(0x00)

    while len(slots) > 4:
        slots.pop(-1)

    slots.reverse()
    return bytearray(slots)

def getConstants(src:str) -> list:
    lines = src.splitlines()
    new_lines = []
    idx = 0
    while lines[idx] != "_"*10 + "START_OF_CODE" + "_"*10:
        new_lines.append(getInfo(lines[idx]))
        idx += 1

    arr = bytearray(list())
    
    for line in new_lines:
        if type(line) == int:
            arr.append(0x00)
            arr += getNumSlots(line)

        elif type(line) == str:
            encoded = bytearray(line.encode(encoding="utf-8", errors="replace"))

            arr.append(0x01)
            arr.append(len(encoded))
            arr += encoded

        elif type(line) == float:
            pass

    return new_lines

def toBytecode(mplc:str): # takes an mplc file as input
    # create variables

    CONSTCOUNT = 0
    VARTABLE   = {}

