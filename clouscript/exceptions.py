

class ClouScriptError(Exception): pass

class LexingError(ClouScriptError):
    """String is not compliant with lexing rules"""

class ParsingError(ClouScriptError):
    """Elements are not compliant with parsing rules"""