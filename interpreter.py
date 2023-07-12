class Funcs:
    def isBuiltin(funcname:str):
        return funcname in ["out", "in"]
    
    def runBuiltin(funcname:str, args:list, consts:list, vars:dict):
        returnable = None
        match funcname:
            case "out":
                returnable = print(*args)

            case "in":
                returnable = input(args[0])

        return vars, returnable
    
    def runCustom(code, args: list, consts:list, vars:dict) -> tuple:
        returnable = None
        new_vars = vars
        local_vars = {}
        new_code = Funcs.getValue(code, consts, vars)
        for line in new_code:
            new_vars, returnable, local_vars = executeLine(line, consts, new_vars, local_vars=local_vars, isLocal=True)

        return new_vars, returnable

    def parseArgs(args:str) -> list:
        new_args = []
        temp = ""
        for char in args[1:-1]:
            if char == ",":
                new_args.append(temp)
                temp = ""
            else:
                temp += char 

        if temp != "":
            new_args.append(Funcs.getValue(temp))

        return new_args
    
    def isValue(v:any) -> bool: # do not use function (not done yet + faulty results)
        if type(v) != str:
            return True
        
        elif "$" in v:
            return False
        
        return False
    
    def getValue(v:str, consts:list, vars:dict) -> any:
        if len(v) < 2:
            if v in vars.keys():
                return vars[v]
            else:
                error(f"Variable {v} does not exist!")
        else:
            if "$" in v[:2]:
                return consts[int(v.replace("$", "").replace(" ", ""))]
            else:
                if v in vars.keys():
                    return vars[v]
                else:
                    error(f"Variable {v} does not exist!")


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
        return value
    
    elif type_ == "INT":
        return int(value)
    
    elif type_ == "FLOAT":
        return float(value)
    
    elif type_ == "BRACKETS":
        return value 
    
    elif type_ == "CODE":
        return splitCodeBlock(value)

    return value


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
                new_locals.update({words[1]: [words[2], words[3]]})
            else:
                new_vars.update({words[1]: [words[2], words[3]]})

        case "CALL":
            if Funcs.isBuiltin(words[1]):
                vars, _ = Funcs.runBuiltin(words[1], Funcs.parseArgs(words[2]), consts, vars)

            else:
                if words[1] in vars.keys():
                    vars, _ = Funcs.runCustom(vars[words[1]][1], Funcs.parseArgs(words[2]), consts, vars)

                else:
                    error(f"Function '{words[1]}' does not exist!")

    return vars, returnable, local_vars


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