class BuiltInFuncs:
    def isBuiltin(funcname):
        pass

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

def read_src(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    else:
        error(f"File {path} does not exist.")

def splitCodeBlock(cb):
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

def getInfo(const):
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

    return type_, value


def getConstants(src):
    lines = src.splitlines()
    new_lines = []
    idx = 0
    while lines[idx] != "_"*10 + "START_OF_CODE" + "_"*10:
        new_lines.append(lines[idx])
        getInfo(lines[idx])
        idx += 1

    return new_lines

def getCode(src):
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

def executeLine(line, consts, vars):
    words = line.split()

    match words[0]:
        case "FN":
            vars.update({words[1]: [words[2], words[3]]})

        case "CALL":
            pass


def interpret(path):
    src = read_src(path)

    constants = getConstants(src)
    code = getCode(src)

    vars = {}

    for l in code:
        vars = executeLine(l, constants, vars)

if __name__ == "__main__":
    import sys, argparse, os
    global debug, ignore_warnings, empty_lines
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