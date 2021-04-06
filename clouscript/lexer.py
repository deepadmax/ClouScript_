import re

from .element import Element
from .exceptions import NoMatch


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

    def groups(self):
        return (self.result.group(0), *self.result.groups())


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
                from .parentheses import Parentheses
                parentheses = Parentheses()

            if delimiters is None:
                from .delimiters import Delimiters
                delimiters = Delimiters()

            if infixes is None:
                from .infixes import Infixes
                infixes = Infixes()

        self.parentheses = parentheses
        self.delimiters = delimiters
        self.infixes = infixes


        if solids is None:                
            solids = [
                # Parentheses
                (self.parentheses.regex, lambda g: (
                    parentheses.find_group(g[0]),
                    g[0]
                )),
                
                # Delimiters
                (self.delimiters.regex, lambda g: (
                    'DELIMITER',
                    g[0]
                )),
                
                # Indexing period
                (r'\.', lambda g: ('INFIX', '.')),
                
                # Comments
                (r'(?://.*)?[\s\n]+|\/\*.*\*\/',
                    lambda g: (None, None)),
            ]

        if spacious is None:
            spacious = [
                # Hexadecimal
                (r'0x([0-9a-fA-F]+)', lambda g: (
                    'HEXADECIMAL',
                    int(g[1], 16)
                )),

                # Float
                (r'\-?\d*\.\d+', lambda g: (
                    'FLOAT',
                    float(g[0])
                )),

                # Integer
                (r'\-?\d+', lambda g: (
                    'INTEGER',
                    int(g[0])
                )),

                # String
                (r'\"((?:\\"|.|\n)*?)\"', lambda g: (
                    'STRING',
                    g[0]
                )),

                # Boolean
                (r'true|false', lambda g: (
                    'BOOLEAN',
                    g[0] == 'true'
                )),

                # Null
                (r'null', lambda g: ('NULL', None)),

                # Infix
                (self.infixes.regex, lambda g: (
                    'INFIX',
                    g[0]
                )),

                # Label
                (r'[\w\_][\w\d\_]*', lambda g: ('LABEL', g[0])),
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
            
            # Set up type and value, plus match status
            matched = False
            type_, value = None, None

            # 1. Match with solids
            for regex, process in self.solids:
                if m.match(regex):
                    type_, value = process(m.groups())
                    
                    # Allow spacious after solid match
                    allow_spacious = True
                    # Move cursor along
                    i += len(m.group(0))

                    matched = True
                    break

            # If a match has been found already, yield it
            if type_ is not None:
                yield Element(type_, value)

            # Regardless of whether there is a type or not,
            # continue to the next element if matched successfully
            if matched:
                continue

            # 2. Match with spacious
            if allow_spacious:
                for regex, process in self.spacious:
                    if m.match(regex):
                        type_, value = process(m.groups())
                        yield Element(type_, value)
                        
                        # Disllow another spacious
                        allow_spacious = False
                        # Move cursor along
                        i += len(m.group(0))
                        
                        break
                else:
                    raise NoMatch(f'No element could be matched at {i}')
            
            # 3. Must match with line breaks or spaces
            else:
                if m.match(r'[\s\n]+'):
                    # Allow spacious elements
                    allow_spacious = True
                    # Move cursor along
                    i += len(m.group(0))

                    continue

                raise NoMatch('Spaces are required between spacious elements')