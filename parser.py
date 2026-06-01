from dataclasses import dataclass
from typing import Iterable, List, Optional

from ast_nodes import (
    BinaryOpNode,
    ExpressionNode,
    FunctionDeclNode,
    IdentifierNode,
    NumberLiteralNode,
    ParameterNode,
    ProgramNode,
    ReturnNode,
    SourcePosition,
)
from scanner import Lexeme


@dataclass
class SyntaxErrorInfo:
    fragment: str
    line: int
    position: int
    absolute_position: int
    description: str

    def location(self) -> str:
        return f"строка {self.line}, позиция {self.position}"


@dataclass
class ParseResult:
    success: bool
    errors: List[SyntaxErrorInfo]
    suppressed_lexical_errors: List[int]
    ast: Optional[ProgramNode] = None


class SyntaxParser:
    WHITESPACE_VALUES = {"(пробел)", "\\t", "\\n"}
    ADDITIVE_OPERATORS = {"+", "-"}
    MULTIPLICATIVE_OPERATORS = {"*", "/"}
    ALL_OPERATORS = ADDITIVE_OPERATORS | MULTIPLICATIVE_OPERATORS
    EXPRESSION_START_VALUES = {"("}
    PARAMS_END_SYNC = {")", "{", "return"}
    RETURN_SYNC = {"}", ";"}
    FUNCTION_SYNC = {"function"}

    def parse(self, tokens: List[Lexeme]) -> ParseResult:
        self.lexical_errors = [token for token in tokens if token.is_error]
        self.tokens = [
            token for token in tokens
            if token.value not in self.WHITESPACE_VALUES
        ]
        self.index = 0
        self.errors: List[SyntaxErrorInfo] = []
        self.suppressed_lexical_errors = set()
        self.source_tokens = tokens

        program = ProgramNode(position=self._program_position(), declarations=[])
        if not self.tokens:
            if not self.lexical_errors:
                self._add_error_at_current("конец ввода", "Ожидалось объявление функции")
            return ParseResult(False, self.errors, sorted(self.suppressed_lexical_errors), program)

        while not self._is_at_end():
            start_index = self.index
            declaration = self._parse_function()
            if declaration is not None:
                program.declarations.append(declaration)

            if self.index == start_index:
                self._advance()

            if not self._is_at_end() and not self._check_keyword("function"):
                self._add_error_at_current(
                    self._current_value() or "фрагмент",
                    f"Лишний фрагмент после завершения функции: '{self._current_value()}'",
                )
                self._recover_until(self.FUNCTION_SYNC)

        return ParseResult(len(self.errors) == 0, self.errors, sorted(self.suppressed_lexical_errors), program)

    def _parse_function(self) -> Optional[FunctionDeclNode]:
        start_token = self._current()
        if self._check_keyword("function"):
            self._advance()
        else:
            self._add_error_at_current("function", "Ожидалось ключевое слово 'function'")
            self._recover_until({"function", "("})
            if self._check_keyword("function"):
                start_token = self._advance()
            elif self._is_at_end():
                return None

        name_token = self._expect_identifier_token("Ожидалось имя функции")
        if name_token is None:
            self._recover_until({"(", "function"})
            if self._check_keyword("function") or self._is_at_end():
                return None

        if not self._expect_value("(", "Ожидалась открывающая круглая скобка '('", {")", "{", "return"}):
            if self._check_keyword("function") or self._is_at_end():
                return None

        params = self._parse_params()
        self._expect_value(")", "Ожидалась закрывающая круглая скобка ')'", {"{", "return"})
        self._expect_value("{", "Ожидалась открывающая фигурная скобка '{'", {"return", "}"})

        body: Optional[ReturnNode] = None
        if self._check_value("}"):
            self._add_error_at_current("return", "Ожидалось ключевое слово 'return' внутри тела функции")
        elif self._is_at_end():
            self._add_error_at_current("return", "Ожидалось ключевое слово 'return' внутри тела функции")
        else:
            body = self._parse_return_statement()
            if self._check_value(";") and self._has_value_after_current("}"):
                self._add_error_at_current(";", "Лишняя точка с запятой после выражения return")
                self._recover_until({"}"})

        self._expect_value("}", "Ожидалась закрывающая фигурная скобка '}'", {";"})
        self._expect_value(";", "Ожидалась точка с запятой после тела функции", {"function"})

        if name_token is None:
            return None

        return FunctionDeclNode(
            position=self._position(start_token or name_token),
            name=name_token.value,
            params=params,
            body=body,
        )

    def _parse_params(self) -> List[ParameterNode]:
        params: List[ParameterNode] = []
        if self._is_at_end() or self._is_params_end():
            return params

        token = self._expect_identifier_token("Ожидался идентификатор параметра или ')'")
        if token is not None:
            params.append(ParameterNode(position=self._position(token), name=token.value))
        else:
            self._recover_params_until(self.PARAMS_END_SYNC | {","})

        while not self._is_at_end() and not self._is_params_end():
            if self._check_value(","):
                self._advance()
                token = self._expect_identifier_token("Ожидался идентификатор параметра после ','")
                if token is not None:
                    params.append(ParameterNode(position=self._position(token), name=token.value))
                    continue
                self._recover_params_until(self.PARAMS_END_SYNC | {","})
                continue

            if self._check_identifier():
                self._add_error_at_current("параметры", "Ожидалась ',' между параметрами или ')'")
                token = self._advance()
                params.append(ParameterNode(position=self._position(token), name=token.value))
                continue

            self._add_error_at_current("параметры", "Ожидалась ',' между параметрами или ')'")
            self._recover_params_until(self.PARAMS_END_SYNC | {","})

        return params

    def _parse_return_statement(self) -> Optional[ReturnNode]:
        keyword_token = self._current()
        if self._check_keyword("return"):
            self._advance()
        else:
            self._add_error_at_current("return", "Ожидалось ключевое слово 'return'")
            if not self._is_expression_start():
                self._recover_until(self.RETURN_SYNC)
                return None

        value: Optional[ExpressionNode] = None
        if self._is_expression_start():
            value = self._parse_expression(self.RETURN_SYNC)
        else:
            self._add_error_at_current("выражение", "Ожидалось выражение после ключевого слова 'return'")

        if self._check_value(";"):
            self._advance()
        elif self._check_value("}") or self._is_at_end():
            self._add_error_at_current(";", "Ожидалась точка с запятой после выражения return")
        else:
            self._recover_until(self.RETURN_SYNC)
            if self._check_value(";"):
                self._advance()

        return ReturnNode(position=self._position(keyword_token), value=value)

    def _parse_expression(self, stop_values: Iterable[str]) -> Optional[ExpressionNode]:
        stop = set(stop_values)
        node = self._parse_term(stop)
        while self._current_value() in self.ADDITIVE_OPERATORS:
            operator = self._advance()
            if not self._is_expression_start():
                self._add_error_at_current("операнд", f"Ожидался операнд после оператора '{operator.value}'")
                self._recover_until(stop | {")"})
                return node
            right = self._parse_term(stop)
            if node is None or right is None:
                return node
            node = BinaryOpNode(
                position=self._position(operator),
                operator=operator.value,
                left=node,
                right=right,
            )

        self._check_expression_tail(stop)
        return node

    def _parse_term(self, stop_values: Iterable[str]) -> Optional[ExpressionNode]:
        stop = set(stop_values)
        node = self._parse_factor(stop)
        while self._current_value() in self.MULTIPLICATIVE_OPERATORS:
            operator = self._advance()
            if not self._is_expression_start():
                self._add_error_at_current("операнд", f"Ожидался операнд после оператора '{operator.value}'")
                self._recover_until(stop | {")"})
                return node
            right = self._parse_factor(stop)
            if node is None or right is None:
                return node
            node = BinaryOpNode(
                position=self._position(operator),
                operator=operator.value,
                left=node,
                right=right,
            )
        return node

    def _parse_factor(self, stop_values: Iterable[str]) -> Optional[ExpressionNode]:
        stop = set(stop_values)
        if self._check_identifier():
            token = self._advance()
            return IdentifierNode(position=self._position(token), name=token.value)

        if self._check_number():
            token = self._advance()
            value = float(token.value) if "." in token.value else int(token.value)
            return NumberLiteralNode(position=self._position(token), value=value, raw=token.value)

        if self._check_value("("):
            self._advance()
            node = self._parse_expression(stop | {")"})
            self._expect_value(")", "Ожидалась закрывающая круглая скобка в выражении", stop)
            return node

        self._add_error_at_current("операнд", "Ожидался идентификатор, число или выражение в скобках")
        self._recover_until(stop | self.ALL_OPERATORS | {")"})
        return None

    def _check_expression_tail(self, stop_values: Iterable[str]) -> None:
        stop = set(stop_values)
        if self._current_value() == ")" and ")" not in stop:
            self._add_repeated_value_error(")", "Лишняя закрывающая круглая скобка ')'")
            self._recover_until(stop)
            return
        if self._check_error() and self._next_non_error_value() in stop:
            return
        if not self._is_at_end() and self._current_value() not in stop:
            if self._is_expression_start() or self._check_value(")"):
                self._add_error_at_current("оператор", "Ожидался оператор между операндами")
            else:
                self._add_error_at_current("выражение", "Недопустимый фрагмент в выражении")
            self._recover_until(stop)

    def _expect_identifier_token(self, message: str) -> Optional[Lexeme]:
        if self._check_identifier():
            return self._advance()

        self._add_error_at_current("идентификатор", message)
        if not self._is_at_end() and self._current_value() not in {"(", ")", "{", "}", ",", ";", "function"}:
            self._advance()
        return None

    def _expect_value(self, value: str, message: str, sync_values: Iterable[str]) -> bool:
        if self._check_value(value):
            self._advance()
            return True

        self._add_error_at_current(value, message)
        sync = set(sync_values)
        if not self._is_at_end() and self._current_value() not in sync:
            self._recover_until(sync | {value})
            if self._check_value(value):
                self._advance()
        return False

    def _recover_until(self, values: Iterable[str]) -> None:
        sync_values = set(values)
        while not self._is_at_end() and self._current_value() not in sync_values:
            self._advance()

    def _recover_params_until(self, values: Iterable[str]) -> None:
        sync_values = set(values)
        while not self._is_at_end() and self._current_value() not in sync_values:
            self._advance()

    def _is_params_end(self) -> bool:
        return self._current_value() in self.PARAMS_END_SYNC

    def _is_expression_start(self) -> bool:
        return self._check_identifier() or self._check_number() or self._current_value() in self.EXPRESSION_START_VALUES

    def _check_keyword(self, value: str) -> bool:
        token = self._current()
        return token is not None and token.token_type == "ключевое слово" and token.value == value

    def _check_identifier(self) -> bool:
        token = self._current()
        return token is not None and token.token_type == "идентификатор"

    def _check_number(self) -> bool:
        token = self._current()
        return token is not None and token.token_type in {"целое без знака", "вещественное число"}

    def _check_error(self) -> bool:
        token = self._current()
        return token is not None and token.is_error

    def _check_value(self, value: str) -> bool:
        return self._current_value() == value

    def _current_value(self) -> Optional[str]:
        token = self._current()
        return token.value if token is not None else None

    def _current(self) -> Optional[Lexeme]:
        if self._is_at_end():
            return None
        return self.tokens[self.index]

    def _next_non_error_value(self) -> Optional[str]:
        next_index = self.index + 1
        while next_index < len(self.tokens):
            token = self.tokens[next_index]
            if not token.is_error:
                return token.value
            next_index += 1
        return None

    def _advance(self) -> Optional[Lexeme]:
        if self._is_at_end():
            return None
        token = self.tokens[self.index]
        self.index += 1
        return token

    def _is_at_end(self) -> bool:
        return self.index >= len(self.tokens)

    def _has_value_after_current(self, value: str) -> bool:
        for token_index in range(self.index + 1, len(self.tokens)):
            if self.tokens[token_index].value == value:
                return True
        return False

    def _program_position(self) -> SourcePosition:
        if self.tokens:
            return self._position(self.tokens[0])
        return SourcePosition(1, 1, 0)

    def _position(self, token: Optional[Lexeme]) -> SourcePosition:
        if token is None:
            error = self._make_eof_error("конец ввода", "")
            return SourcePosition(error.line, error.position, error.absolute_position)
        return SourcePosition(token.line, token.start, token.absolute_start)

    def _add_error_at_current(self, fragment: str, description: str) -> None:
        token = self._current()
        if token is None:
            error = self._make_eof_error(fragment, description)
            if not self._has_error_at(error.absolute_position, description):
                self.errors.append(error)
            return
        self._add_error(token, description)

    def _add_repeated_value_error(self, value: str, description: str) -> None:
        token = self._current()
        if token is None:
            self._add_error_at_current(value, description)
            return

        end_index = self.index
        while end_index + 1 < len(self.tokens) and self.tokens[end_index + 1].value == value:
            end_index += 1
        fragment = "".join(self.tokens[i].value for i in range(self.index, end_index + 1))
        if self._has_error_at(token.absolute_start, description):
            return
        self.errors.append(
            SyntaxErrorInfo(
                fragment=fragment,
                line=token.line,
                position=token.start,
                absolute_position=token.absolute_start,
                description=description,
            )
        )

    def _add_error(self, token: Lexeme, description: str) -> None:
        if token.is_error:
            self._suppress_lexical_error(token)
        if self._has_error_at(token.absolute_start, description):
            return
        self.errors.append(
            SyntaxErrorInfo(
                fragment=token.value,
                line=token.line,
                position=token.start,
                absolute_position=token.absolute_start,
                description=description,
            )
        )

    def _has_error_at(self, absolute_position: int, description: str) -> bool:
        return any(
            error.absolute_position == absolute_position and error.description == description
            for error in self.errors
        )

    def _suppress_lexical_error(self, token: Lexeme) -> None:
        if token.is_error:
            self.suppressed_lexical_errors.add(token.absolute_start)

    def _make_eof_error(self, fragment: str, description: str) -> SyntaxErrorInfo:
        if self.source_tokens:
            last_token = self.source_tokens[-1]
            return SyntaxErrorInfo(
                fragment=fragment,
                line=last_token.line,
                position=last_token.end + 1,
                absolute_position=last_token.absolute_end + 1,
                description=description,
            )

        return SyntaxErrorInfo(
            fragment=fragment,
            line=1,
            position=1,
            absolute_position=0,
            description=description,
        )
