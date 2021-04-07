

def loads(string, lexer=None, parser=None):
    """Parses a string into ClouScript"""

    if lexer is None:
        from .lexer import Lexer
        lexer = Lexer()

    if parser is None:
        from .parser import Parser
        parser = Parser()

    elements = list(lexer.lex(string))
    return parser.parse(elements)