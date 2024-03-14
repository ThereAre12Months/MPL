from .tokenizer import tokenize
from .transpiler import tempName

tokens = tokenize("""
let a = 5.0;

if (a > 4) {
    print("It is bigger!");
};
""")

print(tokens)

code = tempName(tokens)

for l in code:
    print(l)