def getLiterals(source):
    code = list(source)

    # strings
    new_code = []
    idx = 0
    STRINGLITTERALS = []
    start_string = None

    while idx < len(code):
        char = code[idx]
        match char:
            case '"':
                if not start_string:
                    start_string = idx
                else:
                    new_code.append()
        idx += 1


def compile(code):
    c = getLiterals()