from .tokenizer import tokenize
from .transpiler import parseAll

tokens = tokenize("""
var a = 5.0;

if (a + 1 > 4) {
    print("It is bigger!");
};
""")

print(tokens)

code, _ = parseAll(tokens)

for l in code:
    print(l)