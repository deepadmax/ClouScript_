import re

from .parentheses import Parentheses
from .delimiters import Delimiters
# from .infixes import Infixes


class REMatcher:
    """Test multiple regular expressions on a string
    and store the match in object for easy access"""
    
    def __init__(self, string):
        self.string = string

    def match(self, regex):
        self.result = re.match(f"^{regex}", self.string)
        return bool(self.result)
    
    def group(self, *i):
        return self.result.group(*i)


def lex(string):
    """Segment string into elements"""

    space = True
    i = 0

    while i < len(string):
        # Set up the rest of the string for matching
        m = REMatcher(string[i:])

        if m.match:
            pass


class Lexer:
    """A lexer that """

    def __init__(self, parentheses=None, delimiters=None, infixes=None, \
                                        solids=None, spacious=None):
        """Arguments:
            solids -- list: Elements which may be close to other elements
            spacious -- list: Elements which may only be beside
                another spacious element if there is a space separating them
        """

        # If default solids or spacious are to be used,
        # parentheses, delimiters, and infixes must be defined
        
        if solids is None or spacious is None:
            if parentheses is None:
                parentheses = Parentheses()

            if delimiters is None:
                delimiters = Delimiters()

            # if infixes is None:
            #     infixes = Infixes()

        self.parentheses = parentheses
        self.delimiters = delimiters
        self.infixes = infixes


        if solids is None:                
            solids = [
                # Parentheses
                (self.parentheses.regex, lambda m: (
                    parentheses.find_group(m.group(0)),
                    m.group(0)
                )),
                
                # Delimiters
                (self.delimiters.regex, lambda m: (
                    'DELIMITER',
                    m.group(0)
                )),
                
                # Indexing period
                (r'\.', lambda m: ('INFIX', '.')),
                
                # Comments and Line breaks
                (r'(?://.*)?[\s\n]+|\/\*.*\*\/',
                    lambda m: (None, None)),
            ]

        if spacious is None:
            spacious = [
                # Hexadecimal
                (r'0x([0-9a-fA-F]+)', lambda m: (
                    'HEXADECIMAL',
                    int(m.group(1), 16)
                )),

                # Float
                (r'\-?\d*\.\d+', lambda m: (
                    'FLOAT',
                    float(m.group(0))
                )),

                # Integer
                (r'\-?\d+', lambda m: (
                    'INTEGER',
                    int(m.group(0))
                )),

                # String
                (r'\"((?:\\"|.|\n)*?)\"', lambda m: (
                    'STRING',
                    m.group(0)
                )),

                # Boolean
                (r'true|false', lambda m: (
                    'BOOLEAN',
                    m.group(0) == 'true'
                )),

                # Null
                (r'null', lambda m: ('NULL', None)),

                # Infix
                (self.infixes.regex, lambda m: (
                    'INFIX',
                    m.group(0)
                )),

                # Label
                (r'[\w\_][\w\d\_]*', lambda m: ('LABEL', m.group(0))),
            ]


        self.solids = solids
        self.spacious = spacious

    def lex(self, string):
        """Segment string into elements
        Spaces are required between spacious elements"""

        # Track whether the latest match
        # allows for a spacious element
        allow_spacious = True

        i = 0
        while i < len(string):
            # Set up the rest of the string for matching
            m = REMatcher(string[i:])