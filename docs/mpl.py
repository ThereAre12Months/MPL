def executeCode(code):

    setGlobals()
    txt = compile(code, False, doWrite=False, isCode=True)
    interpret(txt, True)
