from dataclasses import dataclass
from typing import List


@dataclass
class Lexeme:
    code: int
    token_type: str
    value: str
    line: int
    start: int
    end: int
    absolute_start: int
    absolute_end: int
    is_error: bool = False
    error_message: str = ""

    def location(self) -> str:
        return f"строка {self.line}, {self.start}-{self.end}"


@dataclass
class ScanResult:
    tokens: List[Lexeme]
    errors: List[Lexeme]


class LexicalAnalyzer:
    KEYWORDS = {"function", "return"}
    OPERATORS = {
        "==",
        "!=",
        ">=",
        "<=",
        "+=",
        "-=",
        "*=",
        "/=",
        "+",
        "-",
        "*",
        "/",
        "=",
        ">",
        "<",
    }
    SEPARATORS = {"(", ")", "{", "}", ","}
    END_OPERATOR = ";"

    CODES = {
        "INTEGER": 1,
        "REAL": 3,
        "IDENTIFIER": 2,
        "OPERATOR": 10,
        "SEPARATOR": 11,
        "KEYWORD": 14,
        "END_OPERATOR": 16,
        "ERROR": 99,
    }

    TYPES = {
        "INTEGER": "целое без знака",
        "REAL": "вещественное число",
        "IDENTIFIER": "идентификатор",
        "OPERATOR": "оператор",
        "SEPARATOR": "разделитель",
        "KEYWORD": "ключевое слово",
        "END_OPERATOR": "конец оператора",
        "ERROR": "ошибка",
    }

    def analyze(self, text: str) -> ScanResult:
        self.text = text
        self.index = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Lexeme] = []
        self.errors: List[Lexeme] = []

        while self.index < len(self.text):
            char = self.text[self.index]

            if char in (" ", "\t"):
                self._handle_whitespace(char)
            elif char == "\n":
                self._handle_newline()
            elif char.isdigit():
                self._handle_number()
            elif self._is_identifier_start(char):
                self._handle_identifier_or_keyword()
            elif self._is_operator_start(char):
                self._handle_operator()
            elif char in self.SEPARATORS:
                self._add_token("SEPARATOR", char, self.line, self.column, self.column, self.index, self.index)
                self._advance()
            elif char == self.END_OPERATOR:
                self._add_token("END_OPERATOR", char, self.line, self.column, self.column, self.index, self.index)
                self._advance()
            else:
                self._handle_invalid_sequence()

        return ScanResult(tokens=self.tokens, errors=self.errors)

    def _handle_whitespace(self, char: str) -> None:
        value = "(пробел)" if char == " " else "\\t"
        self._add_token("SEPARATOR", value, self.line, self.column, self.column, self.index, self.index)
        self._advance()

    def _handle_newline(self) -> None:
        self._add_token("SEPARATOR", "\\n", self.line, self.column, self.column, self.index, self.index)
        self.index += 1
        self.line += 1
        self.column = 1

    def _handle_number(self) -> None:
        start_index = self.index
        start_column = self.column
        value = ""

        while self.index < len(self.text) and self.text[self.index].isdigit():
            value += self.text[self.index]
            self._advance()

        token_type = "INTEGER"
        if (
            self.index + 1 < len(self.text)
            and self.text[self.index] == "."
            and self.text[self.index + 1].isdigit()
        ):
            token_type = "REAL"
            value += self.text[self.index]
            self._advance()

            while self.index < len(self.text) and self.text[self.index].isdigit():
                value += self.text[self.index]
                self._advance()

        if self.index < len(self.text) and self._is_identifier_start(self.text[self.index]):
            while self.index < len(self.text) and self._is_identifier_part(self.text[self.index]):
                value += self.text[self.index]
                self._advance()
            message = f"Недопустимый идентификатор, начинающийся с цифры: '{value}'"
            self._add_error(value, message, self.line, start_column, self.column - 1, start_index, self.index - 1)
            return

        self._add_token(token_type, value, self.line, start_column, self.column - 1, start_index, self.index - 1)

    def _handle_identifier_or_keyword(self) -> None:
        start_index = self.index
        start_column = self.column
        value = ""

        while self.index < len(self.text) and self._is_identifier_part(self.text[self.index]):
            value += self.text[self.index]
            self._advance()

        token_type = "KEYWORD" if value in self.KEYWORDS else "IDENTIFIER"
        self._add_token(token_type, value, self.line, start_column, self.column - 1, start_index, self.index - 1)

    def _handle_operator(self) -> None:
        start_index = self.index
        start_column = self.column
        two_char_value = self.text[self.index:self.index + 2]

        if two_char_value in self.OPERATORS:
            self._add_token(
                "OPERATOR",
                two_char_value,
                self.line,
                start_column,
                start_column + 1,
                start_index,
                start_index + 1,
            )
            self._advance()
            self._advance()
            return

        value = self.text[self.index]
        if value in self.OPERATORS:
            self._add_token("OPERATOR", value, self.line, start_column, start_column, start_index, start_index)
            self._advance()
            return

        message = f"Недопустимый оператор: '{value}'"
        self._add_error(value, message, self.line, start_column, start_column, start_index, start_index)
        self._advance()

    def _handle_invalid_sequence(self) -> None:
        start_index = self.index
        start_column = self.column
        value = ""

        while self.index < len(self.text):
            char = self.text[self.index]
            if (
                char in (" ", "\t", "\n")
                or char.isdigit()
                or self._is_identifier_start(char)
                or self._is_operator_start(char)
                or char in self.SEPARATORS
                or char == self.END_OPERATOR
            ):
                break
            value += char
            self._advance()

        if value == ".":
            message = "Ожидалась цифра перед десятичной точкой"
        elif len(value) == 1:
            message = f"Недопустимый символ: '{value}'"
        else:
            message = f"Недопустимая последовательность символов: '{value}'"
        self._add_error(value, message, self.line, start_column, self.column - 1, start_index, self.index - 1)

    def _add_token(
        self,
        token_type: str,
        value: str,
        line: int,
        start: int,
        end: int,
        absolute_start: int,
        absolute_end: int,
    ) -> None:
        self.tokens.append(
            Lexeme(
                code=self.CODES[token_type],
                token_type=self.TYPES[token_type],
                value=value,
                line=line,
                start=start,
                end=end,
                absolute_start=absolute_start,
                absolute_end=absolute_end,
            )
        )

    def _add_error(
        self,
        value: str,
        message: str,
        line: int,
        start: int,
        end: int,
        absolute_start: int,
        absolute_end: int,
    ) -> None:
        lexeme = Lexeme(
            code=self.CODES["ERROR"],
            token_type=self.TYPES["ERROR"],
            value=value,
            line=line,
            start=start,
            end=end,
            absolute_start=absolute_start,
            absolute_end=absolute_end,
            is_error=True,
            error_message=message,
        )
        self.tokens.append(lexeme)
        self.errors.append(lexeme)

    def _advance(self) -> None:
        self.index += 1
        self.column += 1

    @staticmethod
    def _is_identifier_start(char: str) -> bool:
        return ("A" <= char <= "Z") or ("a" <= char <= "z") or char in ("_", "$")

    @classmethod
    def _is_identifier_part(cls, char: str) -> bool:
        return cls._is_identifier_start(char) or char.isdigit()

    @classmethod
    def _is_operator_start(cls, char: str) -> bool:
        return any(operator.startswith(char) for operator in cls.OPERATORS)
