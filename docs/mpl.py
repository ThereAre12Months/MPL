def executeCode(code):
    import compiler, interpreter, contextlib, io

    compiler.setGlobals()
    txt = compiler.compile(code, False, isCode=True)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        interpreter.interpret(txt, True)
    return f.getvalue()
