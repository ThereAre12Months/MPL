def executeCode(code):
    import compiler, interpreter, contextlib, io

    compiler.setGlobals()
    txt = compiler.compile(code, False, isCode=True)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        interpreter.interpret(txt, True)
    return f.getvalue()

if __name__ == "__main__":
    import sys, compiler, interpreter

    compiler.setGlobals()
    txt = compiler.compile(sys.argv[1], False, False)
    interpreter.interpret(txt, True)