
########################################################################################
# File       : parser.py
# Author     : Devin Arena
# Description: Parses tokens generated by the lexer.
# Since      : 5/4/2022
########################################################################################

import trees.expr
import trees.statement
import token
import tokens
import oof

class Parser:

    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> list:
        statements = []

        while not self.at_end():
            statements.append(self.statement())
        
        return statements
    
    def statement(self) -> trees.statement.Expr:
        if self.match([tokens.OUTPUT]):
            return self.output_statement()
        
        return self.expression_statement()
    
    def output_statement(self) -> trees.statement.Expr:
        value = self.expression()
        self.consume([tokens.SEMI_COLON], "Expect ';' after value.")
        return trees.statement.Output(value)
    
    def expression_statement(self) -> trees.statement.Expr:
        expr = self.expression()
        self.consume([tokens.SEMI_COLON], "Expect ';' after expression.")
        return trees.statement.Expr(expr)

    def expression(self) -> trees.expr.Expr:
        return self.equality()
    
    def equality(self) -> trees.expr.Expr:
        expr = self.comparison()

        while self.match([tokens.BANG_EQUAL, tokens.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = trees.expr.Binary(expr, operator, right)

        return expr
    
    def comparison(self) -> trees.expr.Expr:
        expr = self.term()

        while self.match([tokens.GREATER, tokens.GREATER_EQUAL, tokens.LESS, tokens.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = trees.expr.Binary(expr, operator, right)

        return expr
    
    def term(self) -> trees.expr.Expr:
        expr = self.factor()

        while self.match([tokens.PLUS, tokens.MINUS]):
            operator = self.previous()
            right = self.factor()
            expr = trees.expr.Binary(expr, operator, right)

        return expr
    
    def factor(self) -> trees.expr.Expr:
        expr = self.unary()

        while self.match([tokens.SLASH, tokens.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = trees.expr.Binary(expr, operator, right)
        
        return expr
    
    def unary(self) -> trees.expr.Expr:
        if self.match([tokens.BANG, tokens.MINUS]):
            operator = self.previous()
            right = self.unary()
            return trees.expr.Unary(operator, right)
        return self.primary()
    
    def primary(self) -> trees.expr.Expr:
        if self.match([tokens.FALSE]):
            return trees.expr.Literal(False)
        if self.match([tokens.TRUE]):
            return trees.expr.Literal(True)
        if self.match([tokens.NULL]):
            return trees.expr.Literal(None)
        if self.match([tokens.NUMBER, tokens.STRING]):
            return trees.expr.Literal(self.previous().literal)
        if self.match([tokens.LEFT_PAREN]):
            expr = self.expression()
            self.consume([tokens.RIGHT_PAREN], "Expect ')' after expression.")
            return trees.expr.Grouping(expr)
        raise self.error(self.peek(), f"Unexpected token {self.peek()}")
    
    def match(self, expected: list) -> bool:
        if self.peek().type in expected:
            self.advance()
            return True
        return False
    
    def check(self, expected: list) -> bool:
        if self.at_end():
            return False
        if self.peek().type in expected:
            return True
        return False
    
    def consume(self, expected: list, message: str) -> None:
        if self.check(expected):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def synchronize(self) -> None:
        self.advance()

        while not self.at_end():
            if self.peek().type == tokens.SEMI_COLON:
                return
            if self.peek().type == tokens.CLASS:
                return
            if self.peek().type == tokens.FUN:
                return
            if self.peek().type == tokens.SET:
                return
            if self.peek().type == tokens.FOR:
                return
            if self.peek().type == tokens.IF:
                return
            if self.peek().type == tokens.WHILE:
                return
            if self.peek().type == tokens.OUTPUT:
                return
            if self.peek().type == tokens.RETURN:
                return
            self.advance()
    
    def advance(self) -> token.Token:
        self.current += 1
        return self.previous()
    
    def peek(self) -> token.Token:
        return self.tokens[self.current]
    
    def previous(self) -> token.Token:
        return self.tokens[self.current - 1]

    def at_end(self) -> bool:
        return self.peek().type == tokens.EOF
    
    def error(self, token: token.Token, message: str) -> None:
        oof.error(token, message)
        return ParseException(token, message)

class ParseException(Exception):
    
    def __init__(self, token: token.Token, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.token = token