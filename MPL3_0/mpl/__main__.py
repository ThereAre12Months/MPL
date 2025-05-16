import sys, os

def main():
    from . import tokenizer, parser, transpiler

    if len(sys.argv) < 2:
        print("Usage: python -m mpl <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    with open(source_file, "r") as f:
        code = f.read()

    name = os.path.splitext(os.path.split(source_file)[1])[0]

    tokens = tokenizer.tokenize(code)
    ast = parser.parse(tokens)
    obj = transpiler.generate_llvm(ast=ast.__json__())
    with open(f"build/{name}.s", "w") as f:
        f.write(obj)
    

if __name__ == "__main__":
    main()