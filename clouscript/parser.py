from rich import print

from .element import Element
from .exceptions import MismatchedParentheses, InvalidParenthesis


class Parser:
    def __init__(self, capsules=None, parentheses=None, delimiters=None, infixes=None):
        # Capsules are parenthesis groups which are allowed
        # to connect with other elements to form function calls or the likes
        
        if capsules is None:
            capsules = {
                'ROUND': 'CALL'
            }

        self.capsules = capsules
        
        
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
        
    def parse(self, elements):
        """Parse an array of elements
        and generate an abstract syntax tree
        """

        # The top level does not get properly parsed,
        # so the elements given should always be surrounded
        # by parentheses and have them removed afterward

        left_parenthesis = Element(
            self.parentheses.groups[0],
            self.parentheses.left[0]
        )
        
        right_parenthesis = Element(
            self.parentheses.groups[0],
            self.parentheses.right[0]
        )
        
        elements = [left_parenthesis] + elements + [right_parenthesis]

        # Initialize stack to deal with navigating
        # up and down parenthesized sections
        stack = [[]]
        
        # History of opened parenthese
        history = [None]
        

        i = 0
        while i < len(elements):
            e = elements[i]

            if e.type in self.parentheses.groups:
                # Open up a new section
                # when a left-hand parenthesis is found
                if e.value in self.parentheses.left:
                    stack[-1].append([])
                    stack.append(stack[-1][-1])
                    history.append(e.type)

                # Close down the last opened section
                # when a right-hand parenthesis is found
                elif e.value in self.parentheses.right:
                    # If the closing parenthesis does not match
                    # the type that was most recently opened,
                    # there has been a mismatch
                    if e.type != history[-1]:
                        raise MismatchedParentheses(
                                f'{e.type} does not match with {history[-1]}')

                    stack.pop()
                    history.pop()

                    section = stack[-1][-1]

                    # Form capsule functions
                    section = self.encapsulate(section)

                    # Form infix functions
                    section = self.infixes.structure(section)

                    # Segment section by delimiters
                    section = self.delimiters.segment(section)
                    
                    # Replace section with a section element
                    stack[-1][-1] = Element(e.type, section)

                else:
                    raise InvalidParenthesis('Parenthesis element found with invalid parenthesis')

            else:
                # If the element is not a parenthesis,
                # add it to the currently opened section
                stack[-1].append(e)

            i += 1

        # Remove the section made from the dummy parentheses added at the start
        stack[-1] = stack[-1][0].value

        # But put everything into an overarching code element
        return Element('', stack[-1])

    def encapsulate(self, elements):
        """Group capsules with preceding elements to form function calls"""

        # A capsule can not be preceded by an element
        # if there is only one element
        if len(elements) <= 1:
            return elements

        i = 1
        while i < len(elements):
            # If the type of the element is a capsule,
            # it is intended for a function call.
            # If the section is preceded by a label, encapsule the two
            if elements[i].type in self.capsules:
                # Use the value of the precedent as the function
                function = elements[i - 1]
                # Use the value of the section as arguments
                value = elements[i]
                
                # Get the name for this type of encapsulation
                name = self.capsules.get(value.type)

                # If there is only one argument and it is a sequence,
                # use the array of it instead                            
                if type(value) in (list, tuple) and len(value) == 1 and value[0] == 'SEQUENCE':
                    value = value[0].value

                # If the value element is just a parenthesis group,
                # extract and use the array instead
                if value.type in self.parentheses.groups:
                    value = value.value

                if type(value) not in (list, tuple):
                    value = [value]

                # Add the new function call element
                elements[i - 1] = Element(name, (function, *value))
                # Remove the capsule element
                elements.pop(i)

            else:
                i += 1

        return elements