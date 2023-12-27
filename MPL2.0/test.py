import codeStructure as cs
import datatypes as dt
import time

code = cs.Codeblock([
    cs.AddVar("local", dt.Variable("add"), dt.Function(
        dt.NamedArgs([cs.Variable("v1"), cs.Variable("v2")]),
        dt.Codeblock([
            cs.BuiltinFunctionCall("out", [cs.BinOp("add", cs.Variable("v1"), cs.Variable("v2"))])
        ]))),
    cs.FunctionCall(dt.Variable("add"), [dt.Int(5), dt.Int(10)])
])

perf = cs.Codeblock([
    cs.AddVar("local", dt.Variable("a"), dt.Int(0)),
    cs.Repeat(dt.Int(1000), cs.Codeblock([
        cs.Repeat(dt.Int(1000), cs.Codeblock([
            cs.SetVar(dt.Variable("a"), cs.BinOp("+", dt.Variable("a"), dt.Int(5))),
            cs.SetVar(dt.Variable("a"), cs.BinOp("-", dt.Variable("a"), dt.Int(3))),
            cs.SetVar(dt.Variable("a"), cs.BinOp("*", dt.Variable("a"), dt.Int(10))),
            cs.SetVar(dt.Variable("a"), cs.BinOp("/", dt.Variable("a"), dt.Int(2))),
        ]))
    ]))
])

variables = dt.Vars()

st = time.time()
perf._call(variables)
et = time.time()

print(f"\nFinished executing in {et-st} seconds!")

# fn hello() {
#   out("Hello, world!");
# };
#
# hello();