from ast import *
from stdlib.triad_matrix import Triad
from stdlib.triad_store import TriadStore
from stdlib.pof_consensus import ProofOfFractalConsensus

class CodeGenerator:
    def __init__(self):
        self.output = []
        self.triad_store = TriadStore(db_path="triad_db")
        self.pof_consensus = ProofOfFractalConsensus()

    def generate(self, node: Node):
        method_name = f"generate_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_generate)
        return method(node)

    def generic_generate(self, node: Node):
        raise NotImplementedError(f"No generate_{type(node).__name__} method")

    def generate_Program(self, node: Program):
        for decl in node.declarations:
            self.generate(decl)
        return "\\n".join(self.output)

    def generate_TriadDeclaration(self, node: TriadDeclaration):
        self.output.append(f"struct {node.name} {{")
        for field in node.fields:
            type_str = field.type_name
            if field.is_array:
                type_str += f"[{field.array_size}]"
            self.output.append(f"  {type_str} {field.name};")
        self.output.append("};")
        # Example: create and store a Triad instance
        triad_id = b"codegen_triad_id_" + node.name.encode()
        triad = Triad(id=triad_id)
        # Store triad asynchronously (placeholder)
        # await self.triad_store.put_triad(triad)

    def generate_FunctionDeclaration(self, node: FunctionDeclaration):
        ret_type = node.return_type or "void"
        params_str = ", ".join(f"{param.type_name} {param.name}" for param in node.params)
        self.output.append(f"{ret_type} {node.name}({params_str}) {{")
        self.generate(node.body)
        self.output.append("}")

    def generate_Block(self, node: Block):
        for stmt in node.statements:
            self.generate(stmt)

    def generate_VariableDeclaration(self, node: VariableDeclaration):
        type_str = node.type_name or "auto"
        mut_str = "mutable " if node.mutable else ""
        init_str = ""
        if node.initializer:
            init_str = " = " + self.generate_expression(node.initializer)
        self.output.append(f"{mut_str}{type_str} {node.name}{init_str};")

    def generate_expression(self, node: Node) -> str:
        method_name = f"generate_expr_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_generate_expr)
        return method(node)

    def generic_generate_expr(self, node: Node) -> str:
        raise NotImplementedError(f"No generate_expr_{type(node).__name__} method")

    def generate_expr_CallExpression(self, node: CallExpression) -> str:
        args_str = ", ".join(self.generate_expression(arg) for arg in node.args)
        return f"{node.callee.name}({args_str})"

    def generate_expr_Identifier(self, node: Identifier) -> str:
        return node.name

    def generate_expr_Literal(self, node: Literal) -> str:
        if isinstance(node.value, str):
            return f'"{node.value}"'
        elif isinstance(node.value, bool):
            return "true" if node.value else "false"
        else:
            return str(node.value)
