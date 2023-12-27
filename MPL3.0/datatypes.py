class Codeblock:
    def __init__(self, code:list=None):
        self.code = code or []

    def __call__(self, vars):
        for line in self.code:
            line(vars)

class Function:
    def __init__(self, code:Codeblock, args:list=None, kwargs:dict=None):
        self.code   = code
        self.args   = args or []
        self.kwargs = kwargs or {}