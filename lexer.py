from token_types import Token, TokenType


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None
        self.line = 1
        self.column = 1

    def error(self):
        raise Exception(
            f'Invalid character "{self.current_char}" at line {self.line}, column {self.column}'
        )

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            if self.current_char == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        column = self.column
        decimal_points = 0

        while self.current_char and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            if self.current_char == ".":
                decimal_points += 1
                if decimal_points > 1:
                    self.error()
            result += self.current_char
            self.advance()

        if decimal_points == 0:
            return Token(TokenType.NUMBER, int(result), self.line, column)
        else:
            return Token(TokenType.NUMBER, float(result), self.line, column)

    def string(self):
        result = ""
        column = self.column
        quote_char = self.current_char
        self.advance()

        while self.current_char and self.current_char != quote_char:
            if self.current_char == "\n":
                self.error()
            result += self.current_char
            self.advance()

        if not self.current_char:
            self.error()

        self.advance()
        return Token(TokenType.STRING, result, self.line, column)

    def identifier(self):
        result = ""
        column = self.column

        while self.current_char and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        keywords = {
            "if": TokenType.IF,
            "else": TokenType.ELSE,
        }

        token_type = keywords.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, self.line, column)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if (
                self.current_char == "/"
                and self.pos + 1 < len(self.text)
                and self.text[self.pos + 1] == "/"
            ):
                column = self.column
                comment = "//"
                self.advance()
                self.advance()
                while self.current_char and self.current_char != "\n":
                    comment += self.current_char
                    self.advance()
                if self.current_char == "\n":
                    comment += self.current_char
                    self.advance()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char in ('"', "'"):
                return self.string()

            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier()

            token_map = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                ";": TokenType.SEMICOLON,
                ">": TokenType.GREATER,
                "<": TokenType.LESS,
            }

            if self.current_char in token_map:
                column = self.column
                char = self.current_char
                self.advance()
                return Token(token_map[char], char, self.line, column)

            if self.current_char == "=":
                column = self.column
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(TokenType.EQUALSEQUALS, "==", self.line, column)
                return Token(TokenType.EQUALS, "=", self.line, column)

            self.error()

        return Token(TokenType.EOF, None, self.line, self.column)
