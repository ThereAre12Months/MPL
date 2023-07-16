def executeCode(code):
    import contextlib, io

    setGlobals()
    txt = compile(code, False, isCode=True)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        interpret(txt, True)
    return f.getvalue()
