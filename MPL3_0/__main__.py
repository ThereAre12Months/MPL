from .tokenizer import tokenize
from .transpiler import parseAll

tokens = tokenize("""
let a = 5.0;

if (a > 4) {
    print("It is bigger!");
};
""")

code, _ = parseAll(tokens)

for l in code:
    print(l)