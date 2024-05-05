from .tokenizer import TOKENTYPES, Token

class Mathtree:
    def __init__(self, op:Token, data:list):
        self.op = op
        self.data = data

    def __str__(self):
        return f"{self.data[0]} {self.op.val} {self.data[1]}"

    def __repr__(self):
        return str(self)

class Line:
    def __init__(self, *data):
        self.oc = data[0]
        self.oa = data[1:]

    def __str__(self):
        return f"{self.oc} {self.oa}"
    
    def __repr__(self):
        return str(self)
    
def addVar(tokens:list[Token], idx:int, scope:str) -> list[Line]:
    # get variable name
    token = tokens[idx]
    name = token.val

    idx += 1
    token = tokens[idx]
    
    if token.val == ";":
        return [
            Line("createVar", scope, name),
        ], idx
    
    elif token.val == "=":
        val, idx = parseVal(tokens, idx+1)

        return [
            Line("createVar", scope, name),
            Line("setVar", name, val),
        ], idx
    
def parseAll(tokens:list[Token], idx:int=0) -> list[Line]:
    lines = []

    while idx < len(tokens):
        token = tokens[idx]

        if token.type == TOKENTYPES.KEYWORD:
            # variable stuff
            if token.val == "var":
                newLines, idx = addVar(tokens, idx+1, "global")
                lines.extend(newLines)

            if token.val == "let":
                newLines, idx = addVar(tokens, idx+1, "local")
                lines.extend(newLines)

            # conditionals
            if token.val == "if":
                idx += 1
                cond, idx = parseVal(tokens, idx)
                code, idx = parseVal(tokens, idx)

                lines.append(
                    Line("if", cond, code)
                )

        elif token.type == TOKENTYPES.VARNAME:
            varname = token.val

            idx += 1
            token = tokens[idx]

            if token.type == TOKENTYPES.SYMBOL:
                if token.val == "(":
                    args, idx = parseVal(tokens, idx)
                    if type(args) != list:
                        args = [args]

                    lines.append(Line("call", varname, args))

                else:
                    pass

        else:
            idx += 1

    return lines, idx+1

def parseVal(tokens:list[Token], idx:int):
    token = tokens[idx]

    if token.type == TOKENTYPES.SYMBOL and token.val == "(":
        start_idx = idx
        depth     = 1
        while depth > 0:
            idx += 1
            token = tokens[idx]

            if token.type == TOKENTYPES.SYMBOL:
                if token.val == "(":
                    depth += 1
                elif token.val == ")":
                    depth -= 1
        end_idx = idx

        idx    = start_idx
        values = [None]
        done   = False
        while not done:
            idx += 1
            token = tokens[idx]

            if token.type == TOKENTYPES.SYMBOL:
                if token.val == ")":
                    done = True

                elif token.val == "(" or token.val == "{":
                    val, idx = parseVal(tokens, idx)
                    values[-1] = val

                elif token.val == ",":
                    values.append(None)

            elif token.type == TOKENTYPES.BINOP:
                operator = token
                firstVal = values[-1]
                fake = [Token(TOKENTYPES.SYMBOL, "(")] + tokens[idx+1:end_idx] + [Token(TOKENTYPES.SYMBOL, ")")]
                secondVal, _ = parseVal(fake, 0)
                values[-1] = Mathtree(token, [firstVal, secondVal])

                done = True

            else:
                values[-1] = token

        if len(values) == 1:
            return values[0], end_idx+1
        
        return values, end_idx+1

    elif token.type == TOKENTYPES.SYMBOL and token.val == "{":
        start_idx = idx + 1

        curly_depth = 1
        while curly_depth > 0:
            idx += 1
            token = tokens[idx]

            if token.type == TOKENTYPES.SYMBOL:
                if token.val == "{":
                    curly_depth += 1
                elif token.val == "}":
                    curly_depth -= 1

        end_idx = idx

        lines, _ = parseAll(tokens[start_idx:end_idx])

        return Token(TOKENTYPES.CODEBLOCK, lines), end_idx + 1
    
    else:
        return token, idx+1
