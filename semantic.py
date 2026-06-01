from dataclasses import dataclass
from typing import Dict, List, Optional

from ast_nodes import (
    BinaryOpNode,
    ExpressionNode,
    FunctionDeclNode,
    IdentifierNode,
    NumberLiteralNode,
    ParameterNode,
    ProgramNode,
    SourcePosition,
)


@dataclass
class SemanticErrorInfo:
    fragment: str
    line: int
    position: int
    absolute_position: int
    description: str

    def location(self) -> str:
        return f"строка {self.line}, позиция {self.position}"


@dataclass
class Symbol:
    name: str
    symbol_type: str
    position: SourcePosition


class SymbolTable:
    def __init__(self) -> None:
        self.scopes: List[Dict[str, Symbol]] = [{}]

    def push_scope(self) -> None:
        self.scopes.append({})

    def pop_scope(self) -> None:
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name: str, symbol_type: str, position: SourcePosition) -> Optional[Symbol]:
        current_scope = self.scopes[-1]
        previous = current_scope.get(name)
        if previous is not None:
            return previous
        current_scope[name] = Symbol(name=name, symbol_type=symbol_type, position=position)
        return None

    def lookup(self, name: str) -> Optional[Symbol]:
        for scope in reversed(self.scopes):
            symbol = scope.get(name)
            if symbol is not None:
                return symbol
        return None


class SemanticAnalyzer:
    MIN_SAFE_INTEGER = -9007199254740991
    MAX_SAFE_INTEGER = 9007199254740991

    def analyze(self, ast: Optional[ProgramNode]) -> List[SemanticErrorInfo]:
        self.errors: List[SemanticErrorInfo] = []
        self.symbols = SymbolTable()

        if ast is None:
            return self.errors

        for declaration in ast.declarations:
            duplicate = self.symbols.declare(declaration.name, "function", declaration.position)
            if duplicate is not None:
                self._add_error(
                    declaration.name,
                    declaration.position,
                    f'Ошибка: идентификатор "{declaration.name}" уже объявлен ранее (строка {duplicate.position.line})',
                )

        for declaration in ast.declarations:
            self._check_function(declaration)

        return self.errors

    def _check_function(self, node: FunctionDeclNode) -> None:
        self.symbols.push_scope()
        for parameter in node.params:
            self._declare_parameter(parameter)

        if node.body is not None and node.body.value is not None:
            self._infer_expression_type(node.body.value)

        self.symbols.pop_scope()

    def _declare_parameter(self, node: ParameterNode) -> None:
        duplicate = self.symbols.declare(node.name, "number", node.position)
        if duplicate is not None:
            self._add_error(
                node.name,
                node.position,
                f'Ошибка: идентификатор "{node.name}" уже объявлен ранее (строка {duplicate.position.line})',
            )

    def _infer_expression_type(self, node: ExpressionNode) -> str:
        if isinstance(node, NumberLiteralNode):
            self._check_number_range(node)
            return "number"

        if isinstance(node, IdentifierNode):
            symbol = self.symbols.lookup(node.name)
            if symbol is None or symbol.symbol_type == "function":
                self._add_error(
                    node.name,
                    node.position,
                    f'Ошибка: идентификатор "{node.name}" не был объявлен ранее',
                )
                return "unknown"
            return symbol.symbol_type

        if isinstance(node, BinaryOpNode):
            left_type = self._infer_expression_type(node.left)
            right_type = self._infer_expression_type(node.right)
            if "unknown" in {left_type, right_type}:
                return "unknown"
            if left_type != "number" or right_type != "number":
                self._add_error(
                    node.operator,
                    node.position,
                    f"Ошибка: оператор '{node.operator}' применим только к числовым выражениям",
                )
                return "unknown"
            return "number"

        return "unknown"

    def _check_number_range(self, node: NumberLiteralNode) -> None:
        if self.MIN_SAFE_INTEGER <= node.value <= self.MAX_SAFE_INTEGER:
            return

        self._add_error(
            node.raw,
            node.position,
            (
                f"Ошибка: значение {node.raw} выходит за допустимые пределы "
                f"[{self.MIN_SAFE_INTEGER}; {self.MAX_SAFE_INTEGER}]"
            ),
        )

    def _add_error(self, fragment: str, position: SourcePosition, description: str) -> None:
        self.errors.append(
            SemanticErrorInfo(
                fragment=fragment,
                line=position.line,
                position=position.column,
                absolute_position=position.absolute,
                description=description,
            )
        )
