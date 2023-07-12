class operator:
    pass

class function:
    pass

class codeblock:
    pass

class brackets:
    pass

class Value:
    def __init__(self, type_, value):
        self.t = type_ 
        self.v = value

        if self.t == "BRACKETS":
            # this is trouble
            pass

    def __str__(self):
        return str(self.v)

class Funcs:
    def isBuiltin(funcname:str):
        return funcname in ["out", "in", "type", "toInt", "toStr", "toFloat", "toBool", "toArray"]
    
    def runBuiltin(funcname:str, args:list, consts:list, vars:dict, local_vars:dict={}, isLocal:bool=False):
        returnable = None

        vals = []
        tps = []

        for a in args:
            vals.append(Funcs.getInnerValue(a, consts=consts, vars=vars, local_vars=local_vars, isLocal=isLocal))
            tps.append(a.t)

        match funcname:
            case "out":
                returnable = Value(None, print(*vals))

            case "in":
                returnable = Value(str, input(vals[0]))

            case "type":
                returnable = Value(str, tps[0])

            case "toInt":
                returnable = Value(int, int(vals[0]))

            case "toStr":
                returnable = Value(str, str(vals[0]))

            case "toFloat":
                returnable = Value(float, float(vals[0]))

            case "toBool":
                returnable = Value(bool, bool(vals[0]))

            case "toArray":
                returnable = Value(list, list(vals[0]))

            

        return vars, returnable
    
    def runCustom(code, args: list, consts:list, vars:dict) -> tuple:
        returnable = None
        new_vars = vars
        local_vars = {}
        new_code = Funcs.getInnerValue(code)
        for line in new_code:
            new_vars, returnable, local_vars = executeLine(line, consts, new_vars, local_vars=local_vars, isLocal=True)

        return new_vars, returnable
    
    def checkStatement(statement:str, consts:list, vars:dict, local_vars:dict={}, isLocal:bool=False) -> bool:
        splits = []
        temp = ""

        new_s = Funcs.getValue(statement, consts, vars, local_vars, isLocal).v
        
        for char in new_s[1:-1]:
            if char == " ":
                if temp != "":
                    splits.append(temp)
                    temp = ""
            elif char in ["(", ")", "==", ">", "<", ">=", "<=", "!="]:
                if temp != "":
                    splits.append(temp)
                splits.append(char)
                temp = ""
            else:
                temp += char 

        if not temp == "":
            splits.append(temp)

        if len(splits) == 1:
            return bool(Funcs.getInnerValue(Funcs.getValue(splits[0], consts, vars, local_vars, isLocal), consts, vars, local_vars, isLocal))
        
        if len(splits) == 2:
            error("Conditional cannot exist out of 2 characters")

        if len(splits) == 3:
            val1 = Funcs.getInnerValue(Funcs.getValue(splits[0], consts, vars, local_vars, isLocal), consts, vars, local_vars, isLocal)
            val2 = Funcs.getInnerValue(Funcs.getValue(splits[2], consts, vars, local_vars, isLocal), consts, vars, local_vars, isLocal)

            match splits[1]:
                case "==":
                    return val1 == val2 
                
                case "!=":
                    return val1 != val2
                
                case ">":
                    return val1 > val2 
                
                case "<":
                    return val1 < val2 
                
                case ">=":
                    return val1 >= val2 
                
                case "<=":
                    return val1 <= val2
                
                case _:
                    return False

    def parseArgs(args:Value, consts:list, vars:dict, local_vars:dict = {}, isLocal:bool = False) -> list:
        new_args = []
        a_args = args.v
        temp = ""
        for char in a_args[1:-1]:
            if char == ",":
                new_args.append(Funcs.getValue(temp, consts, vars, local_vars, isLocal))
                temp = ""
            else:
                temp += char 

        if temp != "":
            new_args.append(Funcs.getValue(temp, consts, vars, local_vars, isLocal))

        return new_args
    
    def isValue(v:any) -> bool: # do not use function (not done yet + faulty results)
        if type(v) != str:
            return True
        
        elif "$" in v:
            return False
        
        return False
    
    def getValue(v:any, consts:list, vars:dict, local_vars:dict = {}, isLocal:bool = False) -> any:
        if type(v) == str:
            if "$" in v:
                return consts[int(v.replace("$", "").replace(" ", ""))]
            elif isLocal and v in local_vars.keys():
                return local_vars[v]
            elif v in vars.keys():
                return vars[v]
            elif v in ["(", ")", "+", "-", "*", "/", "==", "!=", "<", "<=", ">", ">="]:
                return Value(operator, v)
            else:
                error(f"Variable {v} does not exist!")
        elif type(v) == Value:
            return v
        else:
            error(f"Can't interpret value of {v}!")
        
    def splitBrackets(bracks):
        splits = []
        temp = ""

        for char in bracks:
            if char == " ":
                if temp != "":
                    splits.append(temp)
                    temp = ""
            elif char in ["(", ")", "+", "-", "*", "/"]:
                splits.append(char)
                temp = ""
            else:
                temp += char 

        if not temp == "":
            splits.append(temp)

        return splits

    def getInnerValue(val:Value, consts:list=[], vars:dict={}, local_vars:dict={}, isLocal:bool=False) -> any:
        if val.t == brackets:        
            splitted = Funcs.splitBrackets(val.v[1:-1])
            new = []
            for split in splitted:
                new_val = Funcs.getValue(split, consts, vars, local_vars, isLocal)
                if new_val.t == brackets:
                    new_new = Funcs.getInnerValue(new_val, consts=consts, vars=vars, local_vars=local_vars, isLocal=isLocal)
                    new.append(Value(type(new_new), new_new))
                else:
                    new.append(new_val)
            
            result = ""
            for v in new:
                if v.t in [int, float, bool, operator]:
                    result += v.v
                elif v.t == str:
                    result += '"' + v.v + '"'
                else:
                    pass

            return eval(result)

        else:
            return val.v


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    OKVIOLET = "\33[35m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def log(msg):
    print(msg)
    return msg

def info(msg):
    print(bcolors.OKGREEN + "INFO: " + bcolors.ENDC + str(msg))

def succes(msg):
    print(bcolors.BOLD + bcolors.OKVIOLET + "SUCCES: " + bcolors.ENDC + str(msg))

def details(msg):
    print(bcolors.OKBLUE + "DETAILS: " + bcolors.ENDC + str(msg))

def warning(msg):
    print(bcolors.WARNING + "WARNING: " + bcolors.ENDC + str(msg))

def error(msg):
    print(bcolors.FAIL + "ERROR: " + str(msg) + bcolors.ENDC)
    sys.exit()

def read_src(path:str) -> str:
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    else:
        error(f"File {path} does not exist.")

def splitCodeBlock(cb:str) -> list:
    line = ""
    lines = []
    in_str = False
    for char in cb:
        if char == "'":
            if in_str:
                lines.append(line)
                line = ""
            in_str = not in_str
        elif in_str:
            line += char
    return lines

def getInfo(const:str) -> tuple:
    idx = const.index(": ")
    type_ = const[:idx]
    value = const[idx+2:]

    if type_ == "STR":
        value.replace("\\n", "\n")
        return Value(str, value)
    
    elif type_ == "INT":
        return Value(int, int(value))
    
    elif type_ == "FLOAT":
        return Value(float, float(value))
    
    elif type_ == "BRACKETS":
        return Value(brackets, value) 
    
    elif type_ == "CODE":
        return Value(codeblock, splitCodeBlock(value))

    return Value(None, value)


def getConstants(src:str) -> list:
    lines = src.splitlines()
    new_lines = []
    idx = 0
    while lines[idx] != "_"*10 + "START_OF_CODE" + "_"*10:
        new_lines.append(getInfo(lines[idx]))
        
        idx += 1

    return new_lines

def getCode(src:str) -> list:
    lines = src.splitlines()
    new_lines = []
    has_entered = False 

    for line in lines:
        if line == "_"*10 + "START_OF_CODE" + "_"*10:
            has_entered = True
            continue

        if has_entered:
            new_lines.append(line)

    return new_lines

def executeLine(line:str, consts:list, vars:dict, local_vars:dict = {}, isLocal:bool = False) -> tuple:
    words = line.split()
    new_vars = vars
    new_locals = local_vars
    returnable = None

    match words[0]:
        case "FN":
            if isLocal:
                new_locals.update({words[1]: Value(function, [Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal), Funcs.getValue(words[3], consts, new_vars, new_locals, isLocal)])})
            else:
                new_vars.update({words[1]: Value(function, [Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal), Funcs.getValue(words[3], consts, new_vars, new_locals, isLocal)])})

        case "IF":
            if Funcs.checkStatement(words[1], consts, new_vars, new_locals, isLocal):
                new_vars, _ = Funcs.runCustom(Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal), [], consts, new_vars)

        case "CALL":
            if Funcs.isBuiltin(words[1]):
                new_vars, _ = Funcs.runBuiltin(words[1], Funcs.parseArgs(Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal), consts, new_vars, new_locals, isLocal), consts, new_vars, new_locals, isLocal)

            else:
                if words[1] in new_vars.keys():
                    new_vars, _ = Funcs.runCustom(new_vars[words[1]].v[1], Funcs.parseArgs(Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal), consts, new_vars, new_locals, isLocal), consts, new_vars)

                else:
                    error(f"Function '{words[1]}' does not exist!")

        case "FNTOVAR":
            if Funcs.isBuiltin(words[1]):
                new_vars, temp = Funcs.runBuiltin(words[1], Funcs.parseArgs(Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal), consts, new_vars, new_locals, isLocal), consts, new_vars)
                if isLocal:
                    new_locals[words[3]] = temp
                else:
                    new_vars[words[3]] = temp

            else:
                if words[1] in new_vars.keys():
                    new_vars, _ = Funcs.runCustom(new_vars[words[1]][1], Funcs.parseArgs(words[2], consts, new_vars, new_locals, isLocal), consts, new_vars)

                else:
                    error(f"Function '{words[1]}' does not exist!")

        case "CREATE":
            val = Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal)
            if val.t == brackets:
                val = Funcs.getInnerValue(val, consts=consts, vars=new_vars, local_vars=new_locals, isLocal=isLocal)
                val = Value(type(val), val)
            if isLocal:
                new_locals.update({words[1] : val})
            else:
                new_vars.update({words[1] : val})

        case "ADDTO":
            if isLocal and words[1] in new_locals.keys():
                old_val = new_locals[words[1]]
                other_val = Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal)

                new_locals.update({words[1] : Value(type(old_val), old_val.v + other_val.v)})
            elif words[1] in new_vars.keys():
                new_vars.update({words[1] : new_vars[words[1]] + Funcs.getInnerValue(Funcs.getValue(words[2], consts, new_vars, new_locals, isLocal))})

    return new_vars, returnable, new_locals


def interpret(path:str):
    src = read_src(path)

    constants = getConstants(src)
    code = getCode(src)

    vars = {}

    for l in code:
        vars, _, _ = executeLine(l, constants, vars)

if __name__ == "__main__":
    import sys, argparse, os
    os.system("")

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
                        prog="MPLC Interpreter",
                        description="This program executes .mplc files")
        
        parser.add_argument("name", metavar="name", help="the path to the file to execute")

        args = parser.parse_args()

        file_path = args.name

    else:
        file_path = input("Enter the path to the file that you want to execute.\n>")

    interpret(file_path)