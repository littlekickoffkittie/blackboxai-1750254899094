from typing import List, Optional, Union

class Node:
    pass

class Program(Node):
    def __init__(self, declarations: List[Node]):
        self.declarations = declarations

class TriadDeclaration(Node):
    def __init__(self, name: str, fields: List['Field']):
        self.name = name
        self.fields = fields

class Field(Node):
    def __init__(self, name: str, type_name: str, is_array: bool = False, array_size: Optional[int] = None):
        self.name = name
        self.type_name = type_name
        self.is_array = is_array
        self.array_size = array_size

class FunctionDeclaration(Node):
    def __init__(self, name: str, params: List['Parameter'], return_type: Optional[str], body: 'Block', is_fractal: bool = False):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.is_fractal = is_fractal

class Parameter(Node):
    def __init__(self, name: str, type_name: str):
        self.name = name
        self.type_name = type_name

class Block(Node):
    def __init__(self, statements: List[Node]):
        self.statements = statements

class VariableDeclaration(Node):
    def __init__(self, name: str, type_name: Optional[str], mutable: bool, initializer: Optional['Expression']):
        self.name = name
        self.type_name = type_name
        self.mutable = mutable
        self.initializer = initializer

class Expression(Node):
    pass

class Literal(Expression):
    def __init__(self, value: Union[str, int, bool, None]):
        self.value = value

class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name

class CallExpression(Expression):
    def __init__(self, callee: Expression, arguments: List[Expression]):
        self.callee = callee
        self.arguments = arguments

class MatchExpression(Expression):
    def __init__(self, expression: Expression, cases: List['MatchCase']):
        self.expression = expression
        self.cases = cases

class MatchCase(Node):
    def __init__(self, pattern: 'Pattern', body: Expression):
        self.pattern = pattern
        self.body = body

class Pattern(Node):
    pass

class LiteralPattern(Pattern):
    def __init__(self, value: Union[str, int, bool, None]):
        self.value = value

class IdentifierPattern(Pattern):
    def __init__(self, name: str):
        self.name = name

# Additional AST nodes can be added as needed for parallel blocks, fractal_spawn, etc.
