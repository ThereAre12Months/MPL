class Exact:
    def __init__(self, val):
        if type(val) == int:
            self.a = val
            self.b = 1

        elif type(val) == float:
            self.a = int(val * (10**len(str(val))))
            self.b = 10**len(str(val))

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

def write_compiled(bc, path):
    splittedPath = splitPath(path)
    basePath = os.path.join(*splittedPath[:-1])
    fileName = splittedPath[-1].replace(".mpl", ".mplc")
    file = "\n".join(bc)

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
                    other += " §" + str(strs.index(temp_str) + const_count) + " "
                    temp_str = ""
                else:
                    other += " §" + str(count) + " "
                    strs.append(temp_str)
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
    in_float = False
    for idx, char in enumerate(src):
        if char in [str(i) for i in range(10)]:
            if src[idx-1] == "§":
                in_const = True
                other += char
            elif src[idx-1] == "f":
                in_float = True
                other += char
            elif in_const:
                other += char
            elif in_float:
                other += char
            else:
                temp_int += char

        else:
            if not temp_int == "":
                ints.append(int(temp_int))
                other += " §" + str(count) + " "
                count += 1
                temp_int = ""

            if not char == ".":
                in_float = False

            in_const = False
            other += char

    if not temp_int == "":
        ints.append(int(temp_int))

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
                    flts.append(float(temp_flt))
                    temp_flt = ""
                    other += " §" + str(count) + " "
                    count += 1

                other += char
                in_float = False

        else:
            other += char

    if not temp_flt == "":
        flts.append(float(temp_flt))

    return other, flts

def find_array(src, const_count):
    if not "[" in src and "]" in src:
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
        arrays.append(array)
        new = other.replace(array, " §" + str(count) + " ")
        count += 1

        other = new

    return other, arrays

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

def getLinePurpose(line):
    words = line.split()
    if len(words) >= 1:
        if words[0] == "let":
            return "variable creation"
        
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
                return "empty line"
        
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
                bc.append(f"SET {words[1]} {words[2]}")

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
                error("Cannot switch variable by None!")
            else:
                bc.append(f"SWITCH {words[0]} {words[2]}")

        elif purpose == "empty line":
            if empty_lines: bc.append("NOP")

        else:
            error(f"Cannot interpret line {line}")

        progress("Compiling to bytecode", idx*100/len(lines))

    progress("Compiling to bytecode", 100)

    return bc

def compile(path, ignore):
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
    src, temp_constants = find_array(src, len(constants))
    constants += temp_constants
    succes(f"Found {len(temp_constants)} array litteral{'' if len(temp_constants) == 1 else 's'}.")
    succes("Replaced all array litterals with references.") 

    details("All litterals: " + str(constants))

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

    info("Creating .mplc file from bytecode...")
    write_compiled(bc, path)
    succes("Succesfully created .mplc file from bytecode!")

if __name__ == "__main__":
    import sys, argparse, os
    global debug, ignore_warnings, empty_lines
    os.system("")

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
                        prog="MPL Compiler",
                        description="This program compiles .mpl files to .mplc files")
        
        parser.add_argument("name", metavar="name", help="the path to the file to compile")
        parser.add_argument("-i", "--include", help="include extra files in the compiled build", type=str, nargs="+")
        parser.add_argument("-d", "--debug", help="gives debug information while compiling if active", action="store_true")
        parser.add_argument("-e", "--emptylines", help="includes empty lines in final build", action="store_true")
        parser.add_argument("-w", "--warnings", help="ignores warnings when set", action="store_true")

        args = parser.parse_args()

        file_path = args.name
        include = args.include
        if include == None:
            include = []
        debug = args.debug
        ignore_warnings = args.warnings
        empty_lines = args.emptylines

        print(ignore_warnings)
        print(empty_lines)

    else:
        file_path = input("Enter the path to the file that you want to compile.\n>")
        include = []
        if input("Do you want to include other files in the compiled build? [y/n]\n>").lower() == "y":
            more = True
            while more:
                include.append(input("Enter the path to the file that you want to include.\n>"))
                more = input("Do you want to include more files? [y/n]\n>").lower() == "y"
        debug = input("Do you want debug information to display during compilation? [y/n]\n>").lower() == "y"
        ignore_warnings = False
        empty_lines = False

    compile(file_path, include)
