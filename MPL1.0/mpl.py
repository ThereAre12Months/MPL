def executeCode(code):
    import compiler, interpreter, contextlib, io

    compiler.setGlobals()
    txt = compiler.compile(code, False, isCode=True)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        interpreter.interpret(txt, True)
    return f.getvalue()

if __name__ == "__main__":
    import sys, compiler, interpreter, time

    compiler.setGlobals()
    txt = compiler.compile(sys.argv[1], False, False)

    st = time.time()
    interpreter.interpret(txt, True)
    et = time.time()

    print(f"\nFinished executing in {et-st} seconds!")