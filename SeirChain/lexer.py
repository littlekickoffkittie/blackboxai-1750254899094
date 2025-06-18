import re
from enum import Enum, auto
from typing import List, Tuple, Optional

class TokenType(Enum):
    # Keywords
    TRIAD = auto()
    FRACTAL = auto()
    PARALLEL = auto()
    CONSENSUS = auto()
    IMMUTABLE = auto()
    MUTABLE = auto()
    ROUTE = auto()
    ANCHOR = auto()
    TRUE = auto()
    FALSE = auto()
    UNCERTAIN = auto()
    # Built-in types
    TRIADHASH = auto()
    FRACTALCOORD = auto()
    CONSENSUSPROOF = auto()
    WAC = auto()
    NETWORKPATH = auto()
    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    # Symbols
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    ARROW = auto()
    ASSIGN = auto()
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    EQUAL = auto()
    NOTEQUAL = auto()
    LESS = auto()
    LESSEQUAL = auto()
    GREATER = auto()
    GREATEREQUAL = auto()
    # End of file
    EOF = auto()

KEYWORDS = {
    "triad": TokenType.TRIAD,
    "fractal": TokenType.FRACTAL,
    "parallel": TokenType.PARALLEL,
    "consensus": TokenType.CONSENSUS,
    "immutable": TokenType.IMMUTABLE,
    "mutable": TokenType.MUTABLE,
    "route": TokenType.ROUTE,
    "anchor": TokenType.ANCHOR,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "uncertain": TokenType.UNCERTAIN,
    "TriadHash": TokenType.TRIADHASH,
    "FractalCoord": TokenType.FRACTALCOORD,
    "ConsensusProof": TokenType.CONSENSUSPROOF,
    "WAC": TokenType.WAC,
    "NetworkPath": TokenType.NETWORKPATH,
}

TOKEN_REGEX = [
    (r"[ \t\n]+", None),  # Skip whitespace
    (r"//.*", None),  # Skip single line comments
    (r"/\*[\s\S]*?\*/", None),  # Skip multi-line comments
    (r"->", TokenType.ARROW),
    (r":", TokenType.COLON),
    (r";", TokenType.SEMICOLON),
    (r",", TokenType.COMMA),
    (r"\.", TokenType.DOT),
    (r"\(", TokenType.LPAREN),
    (r"\)", TokenType.RPAREN),
    (r"\{", TokenType.LBRACE),
    (r"\}", TokenType.RBRACE),
    (r"\[", TokenType.LBRACKET),
    (r"\]", TokenType.RBRACKET),
    (r"==", TokenType.EQUAL),
    (r"!=", TokenType.NOTEQUAL),
    (r"<=", TokenType.LESSEQUAL),
    (r">=", TokenType.GREATEREQUAL),
    (r"<", TokenType.LESS),
    (r">", TokenType.GREATER),
    (r"=", TokenType.ASSIGN),
    (r"\+", TokenType.PLUS),
    (r"-", TokenType.MINUS),
    (r"\*", TokenType.STAR),
    (r"/", TokenType.SLASH),
    (r"%", TokenType.PERCENT),
    (r"&&", TokenType.AND),
    (r"\|\|", TokenType.OR),
    (r"!", TokenType.NOT),
    (r"[0-9]+", TokenType.NUMBER),
    (r'"([^"\\]|\\.)*"', TokenType.STRING),
    (r"[A-Za-z_][A-Za-z0-9_]*", TokenType.IDENTIFIER),
]

class Token:
    def __init__(self, type: TokenType, value: Optional[str], position: int):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value}, pos={self.position})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            match = None
            for pattern, token_type in TOKEN_REGEX:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.position)
                if match:
                    text = match.group(0)
                    if token_type:
                        if token_type == TokenType.IDENTIFIER and text in KEYWORDS:
                            token_type = KEYWORDS[text]
                        token = Token(token_type, text, self.position)
                        self.tokens.append(token)
                    self.position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {self.source[self.position]} at position {self.position}")
        self.tokens.append(Token(TokenType.EOF, None, self.position))
        return self.tokens
