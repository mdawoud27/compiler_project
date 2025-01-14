import sys
from token_types import TokenType

# Increase recursion limit for deeper expressions
sys.setrecursionlimit(10000)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.errors = []
        self.depth = 0
        self.MAX_DEPTH = 100

    def error(self, message):
        self.errors.append(
            f"Syntax error at line {self.current_token.line}, column {self.current_token.column}: {message}"
        )

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(
                f"Expected {token_type.name}, found {self.current_token.type.name}"
            )

    def check_depth(self):
        self.depth += 1
        if self.depth > self.MAX_DEPTH:
            raise Exception("Maximum recursion depth exceeded")

    def program(self):
        try:
            self.statement_list()
            if self.current_token.type != TokenType.EOF:
                self.error("Expected end of file")
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(str(e))
            return False

    def statement_list(self):
        while self.current_token.type not in [TokenType.EOF, TokenType.RBRACE]:
            self.statement()

    def statement(self):
        self.check_depth()
        if self.current_token.type == TokenType.IF:
            self.if_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            self.assignment_statement()
        else:
            self.error("Expected 'if' or identifier")

    def assignment_statement(self):
        self.check_depth()
        if self.current_token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.EQUALS)
            self.expression()
            if self.current_token.type != TokenType.SEMICOLON:
                self.error("Missing semicolon")
            self.eat(TokenType.SEMICOLON)
        else:
            self.error("Expected identifier")

    def if_statement(self):
        self.check_depth()
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        if self.current_token.type == TokenType.RPAREN:
            self.error("Empty condition in if statement")
        else:
            self.expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        self.statement_list()
        if self.current_token.type != TokenType.RBRACE:
            self.error("Missing closing brace")
        self.eat(TokenType.RBRACE)
        if self.current_token.type != TokenType.ELSE:
            self.error("Missing else block")
        self.eat(TokenType.ELSE)
        self.eat(TokenType.LBRACE)
        self.statement_list()
        if self.current_token.type != TokenType.RBRACE:
            self.error("Missing closing brace")
        self.eat(TokenType.RBRACE)

    def expression(self):
        self.check_depth()
        self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            self.term()

    def term(self):
        self.check_depth()
        self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            else:
                self.eat(TokenType.DIVIDE)
            self.factor()

    def factor(self):
        self.check_depth()
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            self.expression()
            self.eat(TokenType.RPAREN)
        else:
            self.error("Expected number, string, identifier, or '('")
