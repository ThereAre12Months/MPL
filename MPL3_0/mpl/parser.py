from .tokenizer import tokenize, Constant, Keyword, Identifier, Operator

class GenericType:
    def __init__(self, type:str):
        self.type = type

    def __json__(self):
        return {
            "type": self.type
        }
    
class ArrayType(GenericType):
    def __init__(self, element_type:GenericType, size:int):
        super().__init__("array")
        self.base_type = element_type
        self.size = size

    def __json__(self):
        return {
            "type": self.type,
            "element_type": self.base_type.__json__(),
            "size": self.size
        }

class ConstantType(GenericType):
    def __init__(self, base_type:GenericType):
        super().__init__("const")
        self.base_type = base_type

    def __json__(self):
        return {
            "type": self.type,
            "base_type": self.base_type.__json__()
        }
    
class Variable:
    def __init__(self, name:str, type:GenericType):
        self.name = name
        self.type = type

    def __json__(self):
        return {
            "name": self.name,
            "type": self.type.__json__()
        }

class Expression:
    def __init__(self):
        ...

    def __json__(self):
        return {
            "type": None,
        }

class Literal(Expression):
    def __init__(self, type:GenericType, value:any):
        self.type = type
        self.value = value

    def __json__(self):
        return {
            "type": "literal",
            "literal_type": self.type.__json__(),
            "value": self.value,
        }
    
class VariableReference(Expression):
    def __init__(self, var:Variable):
        self.var = var

    def __json__(self):
        return {
            "type": "var",
            "var_name": self.var.name,
        }

class MathOperation(Expression):
    binary_ops = {"+", "-", "*", "/", "%", "**"}

    def __init__(self, operator:Operator, left:Expression, right:Expression):
        self.operator = operator
        self.left = left
        self.right = right

    def __json__(self):
        return {
            "type": "binary_op" if self.operator.name in MathOperation.binary_ops else "unary_op",
            "op": self.operator.name,
            "left": self.left.__json__(),
            "right": self.right.__json__(),
        }

class FunctionCall(Expression):
    def __init__(self, name:str, args:list[Expression]):
        self.name = name
        self.args = args

    def __json__(self):
        return {
            "type": "call",
            "function": self.name,
            "args": [arg.__json__() for arg in self.args],
        }

class Statement:
    def __init__(self):
        pass

    def __json__(self):
        return {
            "type": None,
        }
    
class VariableDeclaration(Statement):
    def __init__(self, var: Variable, value: Expression):
        self.var = var
        self.value = value

    def __json__(self):
        return {
            "type": "VariableDeclaration",
            "var": self.var.__json__(),
            "value": self.value.__json__(),
        }
    
class VariableAssignment(Statement):
    def __init__(self, var: Variable, value: Expression):
        self.var = var
        self.value = value

    def __json__(self):
        return {
            "type": "VariableAssignment",
            "var": self.var.__json__(),
            "value": self.value.__json__(),
        }

class ReturnStatement(Statement):
    def __init__(self, value: Expression):
        self.value = value

    def __json__(self):
        return {
            "type": "return",
            "value": self.value.__json__(),
        }

class Codeblock:
    def __init__(self, local_vars: list[Identifier], code: list):
        self.local_vars = local_vars
        self.code = code

    def __json__(self):
        return [line.__json__() for line in self.code]
    
class FunctionDefinition:
    def __init__(self, name: str, arg_names: list[str], arg_types: list[GenericType], return_type: GenericType, code: Codeblock):
        self.name = name
        self.arg_names = arg_names
        self.arg_types = arg_types
        self.return_type = return_type
        self.code = code

    def __json__(self):
        return {
            "name": self.name,
            "arg_names": self.arg_names,
            "arg_types": [arg_type.__json__() for arg_type in self.arg_types],
            "return_type": self.return_type.__json__(),
            "body": self.code.__json__(),
        }

class Code:
    def __init__(self, function_defs: list[FunctionDefinition]):
        self.function_defs = function_defs

        self.has_main_fn = False
        for func in function_defs:
            if func.name == "main":
                self.has_main_fn = True
                break

    def __json__(self):
        return {
            "fn_defs": [func.__json__() for func in self.function_defs],
            "has_main_fn": self.has_main_fn,
        }

def parse_shunting_yard(tokens:list):
    output = []
    op_stack = []
    
    for token_idx, token in enumerate(tokens):
        if isinstance(token, Constant):
            if token_idx > 0 and not (isinstance(tokens[token_idx - 1], Operator) and tokens[token_idx - 1].name != ")"):
                while op_stack and op_stack[-1].name != "(":
                    output.append(op_stack.pop())
            output.append(token)
        elif isinstance(token, Identifier):
            if token_idx + 1 < len(tokens) and tokens[token_idx + 1] == Operator("("):
                op_stack.append(Operator(token.name, precedence_override=float("inf")))
            else:
                if token_idx > 0 and not (isinstance(tokens[token_idx - 1], Operator) and tokens[token_idx - 1].name != ")"):
                    while op_stack and op_stack[-1].name != "(":
                        output.append(op_stack.pop())
                output.append(token)
        elif isinstance(token, Operator):
            if token.name == ",":
                while op_stack and op_stack[-1].name != "(":
                    output.append(op_stack.pop())

            elif token.name == "(":
                op_stack.append(token)
            elif token.name == ")":
                while op_stack and op_stack[-1].name != "(":
                    output.append(op_stack.pop())
                if op_stack and op_stack[-1].name == "(":
                    op_stack.pop()
            else:
                while (op_stack and isinstance(op_stack[-1], Operator) and
                       op_stack[-1].precedence >= token.precedence):
                    output.append(op_stack.pop())
                op_stack.append(token)

    for op in reversed(op_stack):
        output.append(op)

    return output

def parse_expression(tokens:list) -> Expression:
    shunting_yard = parse_shunting_yard(tokens)
    output_expression = []

    for token in shunting_yard:
        if isinstance(token, Constant):
            output_expression.append(Literal(GenericType(token.type), token.value))
        elif isinstance(token, Identifier):
            output_expression.append(VariableReference(Variable(token.name, GenericType("var"))))
        elif isinstance(token, Operator):
            if Operator.isoperator(token.name):
                if token.name in Operator.BIN_OPS:
                    right = output_expression.pop()
                    left = output_expression.pop()
                    output_expression.append(MathOperation(token, left, right))
                elif token.name in Operator.UN_OPS:
                    right = output_expression.pop()
                    output_expression.append(MathOperation(token, None, right))
            else:
                right = output_expression.pop()
                left = output_expression.pop()
                output_expression.append(FunctionCall(token.name, [left, right]))

    return output_expression[0]

def parse_value(tokens:list, idx=0) -> tuple[Expression, int]:
    temp_tokens = []
    while idx < len(tokens) and (tokens[idx] != Operator(";") or isinstance(tokens[idx], Keyword)):
        temp_tokens.append(tokens[idx])
        idx += 1

    math = parse_expression(temp_tokens)

    return math, idx + 1

def parse_function(tokens:list, idx=0):
    idx += 1
    return_type = GenericType(tokens[idx].name)
    idx += 1
    name = tokens[idx].name
    idx += 1
    assert tokens[idx] == Operator("("), "Expected '(' after function name"
    idx += 1

    arg_names = []
    arg_types = []

    while tokens[idx] != Operator(")"):
        arg_type = GenericType(tokens[idx].name)
        idx += 1
        arg_name = tokens[idx].name
        idx += 1
        arg_names.append(arg_name)
        arg_types.append(arg_type)

        if tokens[idx] == Operator(","):
            idx += 1

    assert tokens[idx] == Operator(")"), "Expected ')' after function arguments"
    idx += 1

    assert tokens[idx] == Operator("{"), "Expected '{' after function definition"

    codeblock, idx = parse_codeblock(tokens, idx)

    return FunctionDefinition(name, arg_names, arg_types, return_type, codeblock), idx

def parse_line(tokens: list, idx=0):
    if idx >= len(tokens):
        return None

    if tokens[idx] in (Keyword("bool"), Keyword("int"), Keyword("float"), Keyword("string")):
        type:Keyword = tokens[idx]
        idx += 1
        identifier = tokens[idx]
        idx += 1
        assert tokens[idx] == Operator("="), "Expected '=' after identifier"
        idx += 1
        value, idx = parse_value(tokens, idx)
        return VariableDeclaration(Variable(identifier.name, GenericType(type.name)), value), idx
    
    elif tokens[idx] == Keyword("fn"):
        func, idx = parse_function(tokens, idx)

        return func, idx
    
    elif isinstance(tokens[idx], Identifier):
        identifier:Identifier = tokens[idx]
        idx += 1
        assert tokens[idx] == Operator("="), "Expected '=' after identifier"
        idx += 1
        value, idx = parse_value(tokens, idx)
        return VariableAssignment(Variable(identifier.name, GenericType("TEMP")), value), idx
    
    elif isinstance(tokens[idx], Keyword):
        if tokens[idx] == Keyword("return"):
            idx += 1
            value, idx = parse_value(tokens, idx)
            return ReturnStatement(value), idx

    else:
        raise ValueError(f"Unknown statement type: {tokens[idx]}")

def parse_codeblock(tokens:list, idx=0):
    function_defs = []
    local_vars = []
    code = []
    
    assert tokens[idx] == Operator("{"), "Expected '{' at the start of the codeblock"
    idx += 1

    while idx < len(tokens) and tokens[idx] != Operator("}"):
        line, idx = parse_line(tokens, idx)
        if isinstance(line, VariableDeclaration):
            local_vars.append(line.var)
        elif isinstance(line, FunctionDefinition):
            function_defs.append(line)
        else:
            code.append(line)

    return Codeblock(local_vars, code), idx + 1

def parse(tokens:list):
    idx = 0
    function_defs = []
    while idx < len(tokens):
        line, idx = parse_line(tokens, idx)
        if isinstance(line, FunctionDefinition):
            function_defs.append(line)
        elif line is not None:
            raise ValueError(f"Unexpected line: {line}")
        
    return Code(function_defs)
