from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class SourcePosition:
    line: int
    column: int
    absolute: int


@dataclass
class AstNode:
    position: SourcePosition


@dataclass
class ProgramNode(AstNode):
    declarations: List["FunctionDeclNode"] = field(default_factory=list)


@dataclass
class FunctionDeclNode(AstNode):
    name: str
    params: List["ParameterNode"]
    body: Optional["ReturnNode"]


@dataclass
class ParameterNode(AstNode):
    name: str


@dataclass
class ReturnNode(AstNode):
    value: Optional["ExpressionNode"]


@dataclass
class BinaryOpNode(AstNode):
    operator: str
    left: "ExpressionNode"
    right: "ExpressionNode"


@dataclass
class IdentifierNode(AstNode):
    name: str


@dataclass
class NumberLiteralNode(AstNode):
    value: Union[int, float]
    raw: str


ExpressionNode = Union[BinaryOpNode, IdentifierNode, NumberLiteralNode]
