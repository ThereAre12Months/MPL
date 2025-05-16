from src import tokenizer
from src import parser
from src import transpiler

code = """
fn i32 mul(i32 a, i32 b) {
    return a * b;
}

fn i32 add(i32 a, i32 b) {
    return a + b;
}

fn i32 main() {
    return mul(5, 2);
}
"""

tokens = tokenizer.tokenize(code)

ast = parser.parse(tokens)

obj = transpiler.generate_llvm(ast=ast.__json__())

with open("out.o", "wb") as f:
    f.write(obj)
