from .tokenizer import tokenize, Constant, Keyword, Identifier, Operator
from typing import Any

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

class Expression:
    def __init__(self):
        ...

    def __json__(self):
        return {
            "type": None,
        }

class Literal(Expression):
    def __init__(self, type:GenericType, value:Any):
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

    def __init__(self, operator:Operator, left:Expression, right:Expression|None):
        self.operator = operator
        self.left = left
        self.right = right

    def __json__(self):
        if self.right:
            return {
                "type": "binary_op",
                "op": self.operator.name,
                "left": self.left.__json__(),
                "right": self.right.__json__(),
            }
        
        else:
            return {
                "type": "unary_op",
                "op": self.operator.name,
                "right": self.left.__json__(),
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
    
class ArrayAccess(Expression):
    def __init__(self, array:Expression, index:Expression):
        self.array = array
        self.index = index

    def __json__(self):
        return {
            "type": "array_access",
            "array": self.array.__json__(),
            "index": self.index.__json__(),
        }

class Statement:
    def __init__(self):
        self.type = None

    def __json__(self):
        return {
            "type": self.type,
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
        self.type = "variable_assignment"
        self.var = var
        self.value = value

    def __json__(self):
        return {
            "type": self.type,
            "var": self.var.__json__(),
            "value": self.value.__json__(),
        }

class ReturnStatement(Statement):
    def __init__(self, value: Expression):
        self.type = "return"
        self.value = value

    def __json__(self):
        return {
            "type": self.type,
            "value": self.value.__json__(),
        }
    
class IfStatement(Statement):
    def __init__(self, condition: Expression, then_body: Codeblock, else_body:Codeblock|None = None):
        self.type = "if"
        self.condition = condition
        self.then_body  = then_body
        self.else_body  = else_body
    

    def __json__(self):
        if self.else_body:
            return {
                "type": self.type,
                "condition": self.condition.__json__(),
                "then_body": self.then_body.__json__(),
                "else_body": self.else_body.__json__(),
            }
        return {
            "type": "if",
            "condition": self.condition.__json__(),
            "then_body": self.then_body.__json__(),
            "else_body": [],
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

    token_idx = 0
    while token_idx < len(tokens):
        token = tokens[token_idx]

        if isinstance(token, Constant):
            if token_idx > 0 and not (isinstance(tokens[token_idx - 1], Operator) and tokens[token_idx - 1].name != ")"):
                while op_stack and op_stack[-1].name != "(":
                    output.append(op_stack.pop())
            output.append(token)
        elif isinstance(token, Identifier):
            if token_idx + 1 < len(tokens) and tokens[token_idx + 1] == Operator("("):
                op_stack.append(Operator(token.name, precedence_override=1024))
                args, token_idx = parse_function_args(tokens, token_idx+1)
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
                    left = output_expression.pop()
                    output_expression.append(MathOperation(token, left, None))
            else:
                right = output_expression.pop()
                left = output_expression.pop()
                output_expression.append(FunctionCall(token.name, [left, right]))

    return output_expression[0]

def parse_function_args(tokens:list, idx=0) -> tuple[list[Expression], int]:
    args = []
    while idx < len(tokens) and tokens[idx] != Operator(")"):
        arg, idx = parse_func_arg_value(tokens, idx)
        args.append(arg)

    return args, idx

operator_precedence = {
    "==": 1,
    "!=": 1,
    "<": 1,
    "<=": 1,
    ">": 1,
    ">=": 1,

    "+": 2,
    "-": 2,
    "*": 3,
    "/": 3,
    "%": 3,
    "**": 4,
}

operator_associativity = {
    "==": "left",
    "!=": "left",
    "<": "left",
    "<=": "left",
    ">": "left",
    ">=": "left",

    "+": "left",
    "-": "left",
    "*": "left",
    "/": "left",
    "%": "left",
    "**": "right",
}

def parse_postfix(tokens:list, idx, expr) -> tuple[Expression, int]:
    while True:
        token = tokens[idx]

        if token == Operator("("):
            idx += 1
            args = []
            if tokens[idx] != Operator(")"):
                while True:
                    arg, idx = parse_expression_experimental(tokens, idx)
                    args.append(arg)
                    if tokens[idx] == Operator(","):
                        idx += 1
                    else:
                        break
            
            assert tokens[idx] == Operator(")"), "Expected ')' after function arguments"
            expr = FunctionCall(expr.name, args)

        elif token == Operator("["):
            idx += 1
            index, idx = parse_expression_experimental(tokens, idx)
            assert tokens[idx] == Operator("]"), "Expected ']' after array index"
            idx += 1
            expr = ArrayAccess(expr, index)

        else:
            break

    return expr, idx

def parse_primary(tokens:list, idx=0) -> tuple[Expression, int]:
    token = tokens[idx]
    if isinstance(token, Constant):
        expr = Literal(GenericType(token.type), token.value)
    elif isinstance(token, Identifier):
        expr = VariableReference(Variable(token.name, GenericType("var")))
    elif isinstance(token, Operator):
        if token.name == "(":
            expr, idx = parse_expression_experimental(tokens, idx + 1)
            assert tokens[idx] == Operator(")"), "Expected ')' after expression"
            idx += 1
        else:
            raise ValueError(f"Unknown operator: {token.name}")
        
    return parse_postfix(tokens, idx, expr)

def parse_expression_experimental(tokens:list, idx=0) -> tuple[Expression, int]:
    left, idx = parse_primary(tokens, idx)
    min_precedence = 0

    while True:
        token = tokens[idx]
        is_actual_op = isinstance(token, Operator) and token.name in operator_precedence
        if not is_actual_op or token.precedence < min_precedence:
            break

        op = token.name
        precedence = operator_precedence[op]
        idx += 1

        min_precedence = precedence + 1 if operator_associativity[op] == "left" else precedence
        right, idx = parse_expression_experimental(tokens, idx)

        left = MathOperation(token, left, right)


        print(f"left: {left}")

    return left, idx

def parse_value(tokens:list, idx=0) -> tuple[Expression, int]:
    return parse_expression_experimental(tokens, idx)

    temp_tokens = []
    prev_token:Any = None
    while idx < len(tokens):
        if tokens[idx] == Operator("(") and type(prev_token) == Identifier:
            ...
        elif type(tokens[idx]) in (Literal, Constant, Identifier) or tokens[idx] in (Operator("("), Operator("{")):
            if type(prev_token) in (Literal, Constant, Identifier) or prev_token in (Operator(")"), Operator("}")):
                break

        if isinstance(tokens[idx], Keyword):
            break

        if tokens[idx] == Operator(";"):
            break
         
        prev_token = tokens[idx]
        temp_tokens.append(tokens[idx])
        idx += 1

    math = parse_expression(temp_tokens)
    return math, idx

def parse_func_arg_value(tokens:list, idx=0) -> tuple[Expression, int]:
    temp_tokens = []
    prev_token:Any = None
    while idx < len(tokens):
        if tokens[idx] == Operator("(") and type(prev_token) == Identifier:
            ...
        elif type(tokens[idx]) in (Literal, Constant, Identifier) or tokens[idx] in (Operator("("), Operator("{")):
            if type(prev_token) in (Literal, Constant, Identifier) or prev_token in (Operator(")"), Operator("}")):
                break

        if isinstance(tokens[idx], Keyword):
            break

        if tokens[idx] == Operator(","):
            break
         
        prev_token = tokens[idx]
        temp_tokens.append(tokens[idx])
        idx += 1

    math = parse_expression(temp_tokens)
    return math, idx

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

def parse_line(tokens: list, idx=0) -> tuple[Statement|FunctionDefinition, int]:
    if idx >= len(tokens):
        return Statement(), idx
    
    if tokens[idx] == Operator(";"):
        return Statement(), idx + 1

    elif tokens[idx] in (Keyword("bool"), Keyword("int"), Keyword("float"), Keyword("string")):
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
        
        if tokens[idx] == Keyword("if"):
            idx += 1
            cond, idx = parse_value(tokens, idx)
            code, idx  = parse_codeblock(tokens, idx)

            return IfStatement(cond, code), idx

            

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
        elif isinstance(line, Statement):
            if line.type == None:
                continue
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
