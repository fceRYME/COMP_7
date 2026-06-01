from dataclasses import dataclass, field
from typing import List, Optional

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QDialog, QGraphicsScene, QGraphicsView, QVBoxLayout

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


@dataclass
class GraphNode:
    label: str
    children: List["GraphNode"] = field(default_factory=list)
    x: float = 0
    y: float = 0


class AstGraphDialog(QDialog):
    NODE_WIDTH = 260
    NODE_HEIGHT = 82
    HORIZONTAL_GAP = 70
    VERTICAL_GAP = 130

    def __init__(self, ast: ProgramNode, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("AST")
        self.resize(1200, 800)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        root = _build_graph(ast)
        self._layout_tree(root)
        self._draw_tree(root)
        self.scene.setSceneRect(self.scene.itemsBoundingRect().adjusted(-60, -60, 60, 60))
        self.view.centerOn(root.x + self.NODE_WIDTH / 2, root.y + self.NODE_HEIGHT / 2)

    def _layout_tree(self, root: GraphNode) -> None:
        next_leaf_x = [0.0]

        def visit(node: GraphNode, depth: int) -> None:
            node.y = depth * self.VERTICAL_GAP
            if not node.children:
                node.x = next_leaf_x[0]
                next_leaf_x[0] += self.NODE_WIDTH + self.HORIZONTAL_GAP
                return

            for child in node.children:
                visit(child, depth + 1)
            node.x = (node.children[0].x + node.children[-1].x) / 2

        visit(root, 0)

    def _draw_tree(self, root: GraphNode) -> None:
        self._draw_edges(root)
        self._draw_nodes(root)

    def _draw_edges(self, node: GraphNode) -> None:
        for child in node.children:
            self.scene.addLine(
                node.x + self.NODE_WIDTH / 2,
                node.y + self.NODE_HEIGHT,
                child.x + self.NODE_WIDTH / 2,
                child.y,
                QPen(QColor("#94a3b8"), 2),
            )
            self._draw_edges(child)

    def _draw_nodes(self, node: GraphNode) -> None:
        rect = QRectF(node.x, node.y, self.NODE_WIDTH, self.NODE_HEIGHT)
        item = self.scene.addRect(
            rect,
            QPen(QColor("#2563eb"), 2),
            QBrush(QColor("#eff6ff")),
        )
        item.setZValue(1)

        text = self.scene.addText(node.label, QFont("Consolas", 12))
        text.setDefaultTextColor(QColor("#111827"))
        text.setTextWidth(self.NODE_WIDTH - 16)
        text.setPos(node.x + 8, node.y + 8)
        text.setZValue(2)

        for child in node.children:
            self._draw_nodes(child)


def _build_graph(ast: ProgramNode) -> GraphNode:
    return GraphNode(
        "ProgramNode",
        [_function_node(declaration) for declaration in ast.declarations],
    )


def _function_node(node: FunctionDeclNode) -> GraphNode:
    params_node = GraphNode(
        "params",
        [_parameter_node(parameter) for parameter in node.params],
    )
    body_node = _return_node(node.body)
    return GraphNode(
        f'FunctionDeclNode\nname: "{node.name}"',
        [params_node, body_node],
    )


def _parameter_node(node: ParameterNode) -> GraphNode:
    return GraphNode(f'ParameterNode\nname: "{node.name}"')


def _return_node(node: Optional[ReturnNode]) -> GraphNode:
    if node is None or node.value is None:
        return GraphNode("ReturnNode\nvalue: <empty>")
    return GraphNode("ReturnNode", [_expression_node(node.value)])


def _expression_node(node: ExpressionNode) -> GraphNode:
    if isinstance(node, BinaryOpNode):
        return GraphNode(
            f'BinaryOpNode\noperator: "{node.operator}"',
            [_expression_node(node.left), _expression_node(node.right)],
        )
    if isinstance(node, IdentifierNode):
        return GraphNode(f'IdentifierNode\nname: "{node.name}"')
    if isinstance(node, NumberLiteralNode):
        return GraphNode(f"NumberLiteralNode\nvalue: {node.raw}")
    return GraphNode(type(node).__name__)
