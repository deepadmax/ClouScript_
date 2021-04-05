

class ClouScriptException(Exception): pass


class LexingError(ClouScriptException):
    """String is not compliant with lexing rules"""

class MissingDelimiter(LexingError):
    """No instances of a specified delimiter"""

class EmptySection(LexingError):
    """Found empty section while segmenting"""

class NoMatch(LexingError):
    """No lexing rule could be matched"""


class ParsingError(ClouScriptException):
    """Elements are not compliant with parsing rules"""