from typing import List, Optional

from ast_nodes import (
    BinaryOpNode,
    ExpressionNode,
    FunctionDeclNode,
    IdentifierNode,
    NumberLiteralNode,
    ParameterNode,
    ProgramNode,
    ReturnNode,
)


def format_ast(ast: Optional[ProgramNode]) -> str:
    if ast is None:
        return "AST не построено."
    if not ast.declarations:
        return "ProgramNode\n└── declarations: []"

    lines = ["ProgramNode"]
    for index, declaration in enumerate(ast.declarations):
        _append_function(lines, declaration, "", index == len(ast.declarations) - 1)
    return "\n".join(lines)


def _append_function(lines: List[str], node: FunctionDeclNode, prefix: str, is_last: bool) -> None:
    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}FunctionDeclNode")
    child_prefix = prefix + ("    " if is_last else "│   ")

    children_count = 3
    _append_leaf(lines, f'name: "{node.name}"', child_prefix, False)
    _append_parameters(lines, node.params, child_prefix, children_count == 2)
    _append_return(lines, node.body, child_prefix, True)


def _append_parameters(lines: List[str], params: List[ParameterNode], prefix: str, is_last: bool) -> None:
    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}params")
    child_prefix = prefix + ("    " if is_last else "│   ")

    if not params:
        _append_leaf(lines, "[]", child_prefix, True)
        return

    for index, parameter in enumerate(params):
        _append_leaf(lines, f'ParameterNode name: "{parameter.name}"', child_prefix, index == len(params) - 1)


def _append_return(lines: List[str], node: Optional[ReturnNode], prefix: str, is_last: bool) -> None:
    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}ReturnNode")
    child_prefix = prefix + ("    " if is_last else "│   ")

    if node is None or node.value is None:
        _append_leaf(lines, "value: <empty>", child_prefix, True)
        return

    _append_expression(lines, node.value, child_prefix, True)


def _append_expression(lines: List[str], node: ExpressionNode, prefix: str, is_last: bool) -> None:
    connector = "└── " if is_last else "├── "
    if isinstance(node, BinaryOpNode):
        lines.append(f'{prefix}{connector}BinaryOpNode operator: "{node.operator}"')
        child_prefix = prefix + ("    " if is_last else "│   ")
        _append_expression(lines, node.left, child_prefix, False)
        _append_expression(lines, node.right, child_prefix, True)
        return

    if isinstance(node, IdentifierNode):
        lines.append(f'{prefix}{connector}IdentifierNode name: "{node.name}"')
        return

    if isinstance(node, NumberLiteralNode):
        lines.append(f"{prefix}{connector}NumberLiteralNode value: {node.raw}")


def _append_leaf(lines: List[str], value: str, prefix: str, is_last: bool) -> None:
    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}{value}")
