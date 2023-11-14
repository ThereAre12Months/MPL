import codeStructure as cs
import datatypes as dt

code = cs.Codeblock([
    cs.AddVar("local", dt.Variable("add"), dt.Function(
        dt.NamedArgs([cs.Variable("v1"), cs.Variable("v2")]),
        dt.Codeblock([
            cs.BuiltinFunctionCall("out", [cs.BinOp("add", cs.Variable("v1"), cs.Variable("v2"))])
        ]))),
    cs.FunctionCall(dt.Variable("add"), [dt.Int(5), dt.Int(10)])
])

variables = dt.Vars()

code._call(variables)

# fn hello() {
#   out("Hello, world!");
# };
#
# hello();