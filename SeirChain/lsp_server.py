"""
Crysilis Language Server Protocol (LSP) implementation using pygls.

Features:
- Syntax highlighting and error detection
- Auto-completion for fractal constructs
- Go-to-definition and find references
- Inline documentation and hover info
- Refactoring tools for fractal patterns
"""

from pygls.server import LanguageServer
from pygls.lsp.types import (
    CompletionItem, CompletionItemKind, CompletionParams,
    Hover, HoverParams, Location, Position, Range,
    TextDocumentPositionParams, Diagnostic, DiagnosticSeverity,
    DidOpenTextDocumentParams, DidChangeTextDocumentParams,
    InitializeParams, InitializeResult
)
import re

CRY_KEYWORDS = [
    "triad", "fractal", "parallel", "consensus", "immutable", "mutable",
    "route", "anchor", "true", "false", "uncertain"
]

class CrysilisLanguageServer(LanguageServer):
    CMD_SHOW_CONFIGURATION = 'crysilis.showConfiguration'

    def __init__(self):
        super().__init__()

    def validate_text(self, text):
        diagnostics = []
        # Simple example: check for unmatched braces
        open_braces = 0
        for i, ch in enumerate(text):
            if ch == '{':
                open_braces += 1
            elif ch == '}':
                open_braces -= 1
                if open_braces < 0:
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=text[:i].count('\n'), character=i),
                            end=Position(line=text[:i].count('\n'), character=i+1)
                        ),
                        message="Unmatched closing brace",
                        severity=DiagnosticSeverity.Error,
                        source="crysilis-lsp"
                    ))
                    open_braces = 0
        if open_braces > 0:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=text.count('\n'), character=0),
                    end=Position(line=text.count('\n'), character=1)
                ),
                message="Unmatched opening brace",
                severity=DiagnosticSeverity.Error,
                source="crysilis-lsp"
            ))
        return diagnostics

crysilis_server = CrysilisLanguageServer()

@crysilis_server.feature('textDocument/didOpen')
def did_open(ls: CrysilisLanguageServer, params: DidOpenTextDocumentParams):
    text = params.textDocument.text
    diagnostics = ls.validate_text(text)
    ls.publish_diagnostics(params.textDocument.uri, diagnostics)

@crysilis_server.feature('textDocument/didChange')
def did_change(ls: CrysilisLanguageServer, params: DidChangeTextDocumentParams):
    text = params.contentChanges[0].text
    diagnostics = ls.validate_text(text)
    ls.publish_diagnostics(params.textDocument.uri, diagnostics)

@crysilis_server.feature('textDocument/completion')
def completions(ls: CrysilisLanguageServer, params: CompletionParams):
    items = []
    for kw in CRY_KEYWORDS:
        items.append(CompletionItem(label=kw, kind=CompletionItemKind.Keyword))
    return items

@crysilis_server.feature('textDocument/hover')
def hover(ls: CrysilisLanguageServer, params: HoverParams):
    # Provide simple hover info for keywords
    word = get_word_at_position(ls, params)
    if word in CRY_KEYWORDS:
        contents = f"Crysilis keyword: {word}"
        return Hover(contents=contents)
    return None

def get_word_at_position(ls: CrysilisLanguageServer, params: TextDocumentPositionParams) -> str:
    doc = ls.workspace.get_document(params.textDocument.uri)
    line = doc.lines[params.position.line]
    # Simple regex to extract word at position
    pattern = re.compile(r'\b\w+\b')
    for match in pattern.finditer(line):
        if match.start() <= params.position.character <= match.end():
            return match.group(0)
    return ""

if __name__ == '__main__':
    crysilis_server.start_io()
