from .tokenizer import TOKENTYPES

class Line:
    def __init__(self, *data):
        self.oc = data[0]
        self.oa = data[1:]

    def __str__(self):
        return f"{self.oc} {self.oa}"
    
    def __repr__(self):
        return str(self)

def tempName(tokens) -> list:
    tokenLines = []
    temp  = []

    for token in tokens:
        if token.type == TOKENTYPES.SYMBOL and token.val == ";":
            tokenLines.append(temp)
            temp = []

        else:
            temp.append(token)

    if temp != []:
        tokenLines.append(temp)

    codeLines = []

    for line in tokenLines:
        if line[0].type == TOKENTYPES.KEYWORD:
            if line[0].val == "let":
                if len(line) == 2:
                    codeLines.append(Line("createVar", "local", line[1].val))
                else:
                    codeLines.append(Line("setVar", "local", line[1].val, line[3]))

            if line[0].val == "var":
                if len(line) == 2:
                    codeLines.append(Line("createVar", "global", line[1].val))
                else:
                    codeLines.append(Line("setVar", "global", line[1].val, line[3]))

        if line[0].type == TOKENTYPES.VARNAME:
            if line[-1].val == ")":

                startIdx = -1
                for idx, token in enumerate(line):
                    if token.val == "(":
                        startIdx = idx

                codeLines.append(Line("call", line[:startIdx], line[startIdx:]))

    return codeLines