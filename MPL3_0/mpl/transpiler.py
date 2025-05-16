import json
import llvmlite.ir as ir
import llvmlite.binding as llvm

class Types:
    bool = ir.IntType(1)

    i8  = ir.IntType(8)
    i16 = ir.IntType(16)
    i32 = ir.IntType(32)
    i64 = ir.IntType(64)

    f16 = ir.HalfType()
    f32 = ir.FloatType()
    f64 = ir.DoubleType()

    void = ir.VoidType()

    ptr = ir.PointerType()

def mpl_type_to_llvm_type(mpl_type):
    match mpl_type["type"]:
        case "bool":
            return Types.bool
        case "i8":
            return Types.i8
        case "i16":
            return Types.i16
        case "i32":
            return Types.i32
        case "i64":
            return Types.i64
        case "f16":
            return Types.f16
        case "f32":
            return Types.f32
        case "f64":
            return Types.f64
        case "void":
            return Types.void
        case _:
            raise ValueError(f"Unknown type: {mpl_type}")        

class LLVMBuilder:
    def __init__(self, path:str=None, ast:dict=None):
        if path:
            with open(path, 'r') as file:
                ast = json.load(file)
        if not ast:
            raise ValueError("No AST provided. Please provide a valid AST.")
        self.ast = ast
        self.path = path
        self.optimize = True

        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.module = ir.Module(name="Example MPL Module")
        self.builder = None
        self.current_function = None

        self.function_map = {}
        self.global_vars_map = {}
        self.local_vars_stack = []

    def generate_expression(self, builder:ir.IRBuilder, expr:dict):
        match expr["type"]:
            case "literal":
                return ir.Constant(
                    mpl_type_to_llvm_type(expr["literal_type"]),
                    expr["value"]
                )
            case "call":
                func_name = expr["function"]
                args = [self.generate_expression(builder, arg) for arg in expr["args"]]
                func_ir = self.function_map.get(func_name)
                if func_ir:
                    return builder.call(func_ir, args)
                else:
                    raise ValueError(f"Function {func_name} not found.")
                
            case "var":
                var_name = expr["var_name"]
                if var_name in self.local_vars_stack[-1]:
                    return self.local_vars_stack[-1][var_name]
                elif var_name in self.global_vars_map:
                    return self.global_vars_map[var_name]
                else:
                    raise ValueError(f"Variable {var_name} not found.")
                
            case "binary_op":
                left = self.generate_expression(builder, expr["left"])
                right = self.generate_expression(builder, expr["right"])
                op = expr["op"]
                if op == "+":
                    return builder.add(left, right)
                elif op == "-":
                    return builder.sub(left, right)
                elif op == "*":
                    return builder.mul(left, right)
                elif op == "/":
                    return builder.sdiv(left, right)
                elif op == "%":
                    return builder.srem(left, right)
                else:
                    raise ValueError(f"Unknown operator: {op}")

    def generate_codeblock(self, builder:ir.IRBuilder, code:list):
        for line in code:
            if line["type"] == "call":
                func_name = line["function"]
                args = [self.generate_expression(arg) for arg in line["args"]]
                func_ir = self.function_map.get(func_name)
                if func_ir:
                    temp = builder.call(func_ir, args, name=func_name)
                else:
                    raise ValueError(f"Function {func_name} not found.")
            
            elif line["type"] == "return":
                value = self.generate_expression(builder, line["value"])
                if value:
                    builder.ret(value)
                else:
                    builder.ret_void()
            else:
                raise ValueError(f"Unknown line type: {line['type']}")

    def generate_func_def(self, func:dict):
        func_name = func.get("name")
        func_arg_names = func.get("arg_names", [])
        func_arg_types = func.get("arg_types", [])
        func_return_type = func.get("return_type", {"type": "void"})
        func_body = func.get("body", [])

        func_type = ir.FunctionType(
            mpl_type_to_llvm_type(func_return_type),
            [mpl_type_to_llvm_type(arg) for arg in func_arg_types]
        )
        func_ir = ir.Function(
            self.module,
            func_type,
            func_name
        )

        self.local_vars_stack.append({})
        for i, arg_name in enumerate(func_arg_names):
            func_ir.args[i].name = arg_name
            self.local_vars_stack[-1].update({arg_name: func_ir.args[i]})

        self.function_map[func_name] = func_ir

        bb_entry = func_ir.append_basic_block(name="entry")
        builder = ir.IRBuilder(bb_entry)
        self.generate_codeblock(builder, func_body)

    def generate_code(self):
        for func in self.ast.get("fn_defs", []):
            self.generate_func_def(func)

        llvm_module = llvm.parse_assembly(str(self.module))
        llvm_module.verify()

        if self.optimize and False:
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 3
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            pm.run(llvm_module) 

        target_machine = llvm.Target.from_triple("amd64-pc-windows-msvc").create_target_machine(codemodel="small", reloc="default", opt=3)

        return target_machine.emit_assembly(llvm_module)

def generate_llvm(path:str=None, ast:dict=None):
    b = LLVMBuilder(path=path, ast=ast)
    return b.generate_code()
