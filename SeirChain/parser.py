from typing import List, Optional
from lexer import Lexer, Token, TokenType
from ast import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def current_token(self) -> Token:
        return self.tokens[self.position]

    def consume(self, expected_type: TokenType) -> Token:
        token = self.current_token()
        if token.type == expected_type:
            self.position += 1
            return token
        else:
            raise SyntaxError(f"Expected token {expected_type} but got {token.type} at position {token.position}")

    def parse(self) -> Program:
        declarations = []
        while self.current_token().type != TokenType.EOF:
            decl = self.parse_declaration()
            declarations.append(decl)
        return Program(declarations)

    def parse_declaration(self) -> Node:
        token = self.current_token()
        if token.type == TokenType.TRIAD:
            return self.parse_triad_declaration()
        elif token.type == TokenType.FRACTAL:
            return self.parse_function_declaration(fractal=True)
        elif token.type == TokenType.IDENTIFIER and token.value == "function":
            return self.parse_function_declaration(fractal=False)
        else:
            raise SyntaxError(f"Unexpected token {token.type} at position {token.position}")

    def parse_triad_declaration(self) -> TriadDeclaration:
        self.consume(TokenType.TRIAD)
        name_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.LBRACE)
        fields = []
        while self.current_token().type != TokenType.RBRACE:
            field_name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.COLON)
            type_name = self.consume(TokenType.IDENTIFIER).value
            is_array = False
            array_size = None
            if self.current_token().type == TokenType.LBRACKET:
                self.consume(TokenType.LBRACKET)
                size_token = self.consume(TokenType.NUMBER)
                array_size = int(size_token.value)
                self.consume(TokenType.RBRACKET)
                is_array = True
            self.consume(TokenType.SEMICOLON)
            fields.append(Field(field_name, type_name, is_array, array_size))
        self.consume(TokenType.RBRACE)
        return TriadDeclaration(name_token.value, fields)

    def parse_function_declaration(self, fractal: bool) -> FunctionDeclaration:
        if fractal:
            self.consume(TokenType.FRACTAL)
        self.consume(TokenType.IDENTIFIER)  # function keyword
        name_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.LPAREN)
        params = self.parse_parameters()
        self.consume(TokenType.RPAREN)
        return_type = None
        if self.current_token().type == TokenType.ARROW:
            self.consume(TokenType.ARROW)
            return_type = self.consume(TokenType.IDENTIFIER).value
        body = self.parse_block()
        return FunctionDeclaration(name_token.value, params, return_type, body, fractal)

    def parse_parameters(self) -> List[Parameter]:
        params = []
        if self.current_token().type == TokenType.RPAREN:
            return params
        while True:
            param_name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.COLON)
            param_type = self.consume(TokenType.IDENTIFIER).value
            params.append(Parameter(param_name, param_type))
            if self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        return params

    def parse_block(self) -> Block:
        self.consume(TokenType.LBRACE)
        statements = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            statements.append(stmt)
        self.consume(TokenType.RBRACE)
        return Block(statements)

    def parse_statement(self) -> Node:
        # For simplicity, parse variable declarations and expressions here
        token = self.current_token()
        if token.type in (TokenType.IMMUTABLE, TokenType.MUTABLE):
            return self.parse_variable_declaration()
        else:
            expr = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
            return expr

    def parse_variable_declaration(self) -> VariableDeclaration:
        mutable = self.current_token().type == TokenType.MUTABLE
        self.consume(self.current_token().type)
        name = self.consume(TokenType.IDENTIFIER).value
        type_name = None
        if self.current_token().type == TokenType.COLON:
            self.consume(TokenType.COLON)
            type_name = self.consume(TokenType.IDENTIFIER).value
        initializer = None
        if self.current_token().type == TokenType.ASSIGN:
            self.consume(TokenType.ASSIGN)
            initializer = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return VariableDeclaration(name, type_name, mutable, initializer)

    def parse_expression(self) -> Expression:
        # For now, parse identifiers, literals, and call expressions
        token = self.current_token()
        if token.type == TokenType.IDENTIFIER:
            id_name = token.value
            self.consume(TokenType.IDENTIFIER)
            if self.current_token().type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                args = []
                if self.current_token().type != TokenType.RPAREN:
                    while True:
                        arg = self.parse_expression()
                        args.append(arg)
                        if self.current_token().type == TokenType.COMMA:
                            self.consume(TokenType.COMMA)
                        else:
                            break
                self.consume(TokenType.RPAREN)
                return CallExpression(Identifier(id_name), args)
            else:
                return Identifier(id_name)
        elif token.type == TokenType.NUMBER:
            value = int(token.value)
            self.consume(TokenType.NUMBER)
            return Literal(value)
        elif token.type == TokenType.TRUE:
            self.consume(TokenType.TRUE)
            return Literal(True)
        elif token.type == TokenType.FALSE:
            self.consume(TokenType.FALSE)
            return Literal(False)
        elif token.type == TokenType.UNCERTAIN:
            self.consume(TokenType.UNCERTAIN)
            return Literal("uncertain")
        else:
            raise SyntaxError(f"Unexpected token {token.type} at position {token.position}")
