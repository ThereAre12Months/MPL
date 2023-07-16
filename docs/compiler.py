import os, sys

class Exact:
    def __init__(self, val):
        if type(val) == int:
            self.a = val
            self.b = 1

        elif type(val) == float:
            self.a = int(val * (10**len(str(val))))
            self.b = 10**len(str(val))

class TempFunction:
    def __init__(self, name, *args):
        self.n = name
        self.a = args

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
    if debug:
        print(bcolors.OKGREEN + "INFO: " + bcolors.ENDC + str(msg))

def succes(msg):
    if debug:
        print(bcolors.BOLD + bcolors.OKVIOLET + "SUCCES: " + bcolors.ENDC + str(msg))

def details(msg):
    if debug:
        print(bcolors.OKBLUE + "DETAILS: " + bcolors.ENDC + str(msg))

def warning(msg):
    if debug:
        print(bcolors.WARNING + "WARNING: " + bcolors.ENDC + str(msg))

def error(msg):
    if debug:
        print(bcolors.FAIL + "ERROR: " + str(msg) + bcolors.ENDC)

    if not ignore_warnings:
        sys.exit()

def progress(msg, percentage):
    if debug:
        if percentage == 100:
            print(f"\r{bcolors.OKGREEN}{msg}{bcolors.ENDC}: 100% done!     ")
        else:
            print(f"\r{bcolors.OKGREEN}{msg}{bcolors.ENDC}: {round(percentage, 2)}% done!     ", end="")

def read_src(path):
    with open(path, "r") as f:
        return f.read()

def write_compiled(consts, bc, path):
    splittedPath = splitPath(path)
    basePath = os.path.join(*splittedPath[:-1])
    fileName = splittedPath[-1].replace(".mpl", ".mplc")
    file = "\n".join([str(c) for c in consts])
    file += "\n" + "_"*10 + "START_OF_CODE" + "_"*10 + "\n"
    file += "\n".join(bc)

    info(f"Writing to {os.path.join(basePath, 'build', fileName)}")

    if os.path.exists(os.path.join(basePath, "build")):
        if os.path.exists(os.path.join(basePath, "build", fileName)):
            with open(os.path.join(basePath, "build", fileName), "w") as f:
                f.write(file)
        else:
            with open(os.path.join(basePath, "build", fileName), "x") as f:
                f.write(file)

    else:
        os.mkdir(os.path.join(basePath, "build"))
        with open(os.path.join(basePath, "build", fileName), "x") as f:
            f.write(file)

def find_str(src, const_count):
    if not '"' in src:
        return src, []
    
    strs = []
    temp_str = ""
    other = ""
    count = const_count
    in_str = False
    for char in src:
        if char == '"':
            if in_str:
                if temp_str in strs:
                    other += " $" + str(strs.index(temp_str) + const_count) + " "
                    temp_str = ""
                else:
                    other += " $" + str(count) + " "
                    strs.append("STR: " + str(temp_str))
                    temp_str = ""
                    count += 1
                
            in_str = not in_str

        elif in_str:
            temp_str += char

        else:
            other += char

    return other, strs

def find_int(src, const_count):
    can_have_int = False
    for i in range(10):
        if str(i) in src:
            can_have_int = True 
    if not can_have_int:
        return src, []
    
    ints = []
    temp_int = ""
    other = ""
    count = const_count
    in_const = False
    in_text = False
    for idx, char in enumerate(src):
        if char in [str(i) for i in range(10)]:
            if src[idx-1] == "$":
                in_const = True
                other += char
            elif not src[idx-1] in [str(i) for i in range(10)]+[" ", ",", "(", ")"]:
                in_text = True
                other += char
            elif in_const:
                other += char
            elif in_text:
                other += char
            else:
                temp_int += char

        else:
            if not temp_int == "":
                ints.append("INT: " + str(temp_int))
                other += " $" + str(count) + " "
                count += 1
                temp_int = ""

            if not char == ".":
                in_text = False

            in_const = False
            other += char

    if not temp_int == "":
        ints.append("INT: " + str(temp_int))

    return other, ints
 
def find_float(src, const_count):
    if not "f" in src:
        return src, []

    flts = []
    temp_flt = ""
    other = ""
    in_float = False
    count = const_count

    for idx, char in enumerate(src):
        if char == "f":
            if (src[idx-1] in [" ", ",", "(", ")", ":", "{", "}"]) and (src[idx+1] in ([str(i) for i in range(10)] + ["."])):
                in_float = True 
            else:
                other += char 

        elif in_float:
            if char in ([str(i) for i in range(10)] + ["."]):
                temp_flt += char 
            else:
                if not temp_flt == "":
                    flts.append("FLOAT: " + str(temp_flt))
                    temp_flt = ""
                    other += " $" + str(count) + " "
                    count += 1

                other += char
                in_float = False

        else:
            other += char

    if not temp_flt == "":
        flts.append("FLOAT: " + str(temp_flt))

    return other, flts

def find_function_references(src, const_count):
    other = src
    count = const_count
    refs = []
    while "&" in other:
        start_idx = other.index("&")
        bracket_count = 0
        end_idx = start_idx
        while not (other[end_idx] == ")" and bracket_count == 1):
            if other[end_idx] == "(":
                bracket_count += 1
            elif other[end_idx] == ")":
                bracket_count -= 1

            end_idx += 1

        new_replacing, other_consts = find_brackets(other[start_idx:end_idx+1], count)
        refs += other_consts
        count += len(other_consts)
        refs.append("FNREF: CALL " + str(new_replacing)[1:])
        other = other.replace(other[start_idx:end_idx+1], f" ${count} ")
        count += 1

    return other, refs

def find_array(src, const_count):
    if not ("[" in src and "]" in src):
        return src, []
    
    other = src 
    new = ""
    count = const_count
    arrays = []

    while "]" in other:
        idx = other.index("]")
        
        start_pos = 0
        end_pos = idx
        current_pos = end_pos

        while other[current_pos] != "[":
            current_pos -= 1
        start_pos = current_pos

        array = other[start_pos:end_pos+1]
        arrays.append("ARRAY: " + str(array))
        new = other.replace(array, " $" + str(count) + " ")
        count += 1

        other = new

    return other, arrays

def find_brackets(src, const_count):
    if not ("(" in src and ")" in src):
        return src, []
    
    other = src 
    new = ""
    count = const_count
    brackets = []

    while ")" in other:
        idx = other.index(")")

        start_pos = 0
        end_pos = idx
        current_pos = end_pos 

        while other[current_pos] != "(":
            current_pos -= 1
        start_pos = current_pos

        bracket = other[start_pos:end_pos+1]
        brackets.append("BRACKETS: " + str(bracket))
        new = other.replace(bracket, " $" + str(count) + " ")
        count += 1

        other = new 

    return other, brackets

def brackets_parser(bracket):
    pass

def find_codeblocks(src, const_count):
    if not ("{" in src and "}" in src):
        return src, []
    
    other = src 
    new = ""
    count = const_count 
    blocks = []

    while "}" in other:
        end_pos = other.index("}")
        current_pos = end_pos
        while other[current_pos] != "{": current_pos -= 1
        start_pos = current_pos

        block = other[start_pos:end_pos+1]
        new = other.replace(block, " $" + str(count) + " ")
        block = toBytecode(trim_lines(split_source(block[1:-1])))
        blocks.append("CODE: " + str(block))
        count += 1

        other = new 

    return other, blocks

def split_source(src):
    line = ""
    lines = []
    for char in src:
        if char == ";":
            lines.append(line)
            line = ""
        else:
            line += char
    
    if not line == "":
        lines.append(line)

    return lines

def trim_lines(lines):
    new_lines = []
    for l in lines:
        new_l = l
        while len(new_l) > 0 and new_l[0] in [" ", "\t", "\n"]:
            new_l = new_l[1:]

        while len(new_l) > 0 and new_l[-1] in [" ", "\t", "\n"]:
            new_l = new_l[:-1]

        new_lines.append(new_l)
    return new_lines

def splitPath(path):
    p = []
    t = ""
    for char in path:
        if char in [os.path.sep, "/"]:
            if not t == "": p.append(t); t = ""
        else:
            t += char
    if not t == "": p.append(t)
    return p

def is_reference(txt):
    return "$" in txt[:2]

def getLinePurpose(line):
    words = line.split()
    if len(words) >= 1:
        if words[0] == "let":
            if len(words) >= 4:
                if is_reference(words[3]):
                    return "function output to var"
            return "variable creation"
        
        if words[0] == "fn":
            return "function creation"
        
        if words[0] == "if":
            return "if statement"
        
        if words[0] == "repeat":
            return "repeat loop"
        
        if words[0] == "while":
            return "while loop"
        
        if words[0] == "until":
            return "until loop"
        
        if words[0] == "loop":
            return "loop loop"
        
    if len(words) >= 2:
        match words[1]:
            case "=":
                return "set variable"
            case "+=":
                return "add to variable"
            case "-=":
                return "subtract from variable"
            case "*=":
                return "multiply variable"
            case "/=":
                return "divide variable"
            case "<->":
                return "switch variables"
            case _:
                if is_reference(words[1]):
                    return "call function"
        
    return "empty line"

def toBytecode(lines):
    bc = []
    for idx, line in enumerate(lines):
        purpose = getLinePurpose(line)
        words = line.split()

        if purpose == "variable creation":
            if len(words) < 3:
                error("Variable needs name AND starting value!")
            else:
                bc.append(f"CREATE {words[1]} {words[2]}")

        elif purpose == "set variable":
            if len(words) < 3:
                error("Cannot set a variable to no value!")
            else:
                bc.append(f"SET {words[0]} {words[2]}")

        elif purpose == "add to variable":
            if len(words) < 3:
                error("Cannot add None to variable!")
            else:
                bc.append(f"ADDTO {words[0]} {words[2]}")

        elif purpose == "subtract from variable":
            if len(words) < 3:
                error("Cannot subtract None from variable!")
            else:
                bc.append(f"SUBFROM {words[0]} {words[2]}")

        elif purpose == "multiply variable":
            if len(words) < 3:
                error("Cannot multiply variable by None!")
            else:
                bc.append(f"MULBY {words[0]} {words[2]}")

        elif purpose == "divide variable":
            if len(words) < 3:
                error("Cannot divide variable by None!")
            else:
                bc.append(f"DIVBY {words[0]} {words[2]}")

        elif purpose == "switch variables":
            if len(words) < 3:
                error("Cannot switch variable with None!")
            else:
                bc.append(f"SWITCH {words[0]} {words[2]}")

        elif purpose == "call function":
            if len(words) < 2:
                error("HOOOOOOOOOOOWWWWWWW IS THIS POOOOOSSSSSSSSSIIIIIIIBLE?!?!?!?!?!?")
            else:
                bc.append(f"CALL {words[0]} {words[1]}")

        elif purpose == "function output to var":
            if len(words) < 4:
                error("Man, I don't get these errors")
            else:
                bc.append(f"FNTOVAR {words[2]} {words[3]} {words[1]}")

        elif purpose == "function creation":
            if len(words) < 4:
                error("Incomplete function!")
            else:
                bc.append(f"FN {words[1]} {words[2]} {words[3]}")

        elif purpose == "if statement":
            if len(words) < 3:
                error("Incomplete if statement!")
            else:
                bc.append(f"IF {words[1]} {words[2]}")

        elif purpose == "repeat loop":
            if len(words) < 3:
                error("Incomplete repeat loop!")
            else:
                bc.append(f"RPT {words[1]} {words[2]}")

        elif purpose == "while loop":
            if len(words) < 3:
                error("Incomplete while loop")
            else:
                bc.append(f"WHILE {words[1]} {words[2]}")

        elif purpose == "until loop":
            if len(words) < 3:
                error("Incomplete until loop")
            else:
                bc.append(f"UNTIL {words[1]} {words[2]}")

        elif purpose == "loop loop":
            if len(words) < 2:
                error("Incomplete loop loop")
            else:
                bc.append(f"LOOP {words[1]}")

        elif purpose == "empty line":
            if empty_lines: bc.append("NOP")

        else:
            error(f"Cannot interpret line {line}")

        progress("Compiling to bytecode", idx*100/len(lines))

    progress("Compiling to bytecode", 100)

    return bc

def compile(path, ignore, doWrite=True, doDebug=False, isCode=False):
    if isCode:
        src = path
    else:
        src = read_src(path)

    src = " " + src + " "

    info("Finding literals...")

    src, constants = find_str(src, 0)
    succes(f"Found {len(constants)} string litteral{'' if len(constants) == 1 else 's'}.")
    succes("Replaced all string litterals with references.")
    src, temp_constants = find_int(src, len(constants))
    constants += temp_constants
    succes(f"Found {len(temp_constants)} integer litteral{'' if len(temp_constants) == 1 else 's'}.")
    succes("Replaced all integer litterals with references.")
    src, temp_constants = find_float(src, len(constants))
    constants += temp_constants
    succes(f"Found {len(temp_constants)} float litteral{'' if len(temp_constants) == 1 else 's'}.")
    succes("Replaced all float litterals with references.")
    src, temp_constants = find_function_references(src, len(constants))
    constants += temp_constants
    succes(f"Found {len(temp_constants)} function reference{'' if len(temp_constants) == 1 else 's'}.")
    succes("Replaced all function references with references.")
    src, temp_constants = find_array(src, len(constants))
    constants += temp_constants
    succes(f"Found {len(temp_constants)} array litteral{'' if len(temp_constants) == 1 else 's'}.")
    succes("Replaced all array litterals with references.")
    src, temp_constants = find_brackets(src, len(constants))
    constants += temp_constants
    succes(f"Found {len(temp_constants)} bracket pair{'' if len(temp_constants) == 1 else 's'}.")
    succes("Replaced all bracket pairs with references.") 
    src, temp_constants = find_codeblocks(src, len(constants))
    constants += temp_constants
    succes(f"Found {len(temp_constants)} codeblock{'' if len(temp_constants) == 1 else 's'}.")
    succes("Replaced all codeblocks with references.") 

    # split into lines (based on semi-colon)
    info("Splitting lines...")
    lines = split_source(src)
    succes(f"Split {len(lines)} lines succesfully!")

    info("Trimming lines...")
    lines = trim_lines(lines)
    succes("Trimmed all lines succesfully!")
    
    info("Converting lines into bytecode...")
    bc = toBytecode(lines)
    succes("Converted all lines into bytecode!")

    if doWrite:
        info("Creating .mplc file from bytecode...")
        write_compiled(constants, bc, path)
        succes("Succesfully created .mplc file from bytecode!")
    else:
        file = "\n".join([str(c) for c in constants])
        file += "\n" + "_"*10 + "START_OF_CODE" + "_"*10 + "\n"
        file += "\n".join(bc)
        return file

def setGlobals():
    global debug, ignore_warnings, empty_lines
    debug = ignore_warnings = empty_lines = False