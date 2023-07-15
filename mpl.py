if __name__ == "__main__":
    import sys, compiler, interpreter

    compiler.setGlobals()
    txt = compiler.compile(sys.argv[1], False, False)
    interpreter.interpret(txt, True)