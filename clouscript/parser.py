from .element import Element
from .exceptions import MismatchedParentheses, InvalidParenthesis


class Parser:
    def __init__(self, capsules=None, parentheses=None, delimiters=None, infixes=None):
        """Capsules are names of parenthesis groups which are allowed
        to connect with labels to form function calls.
        """


        if capsules is None:
            capsules = ['ROUND']

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
        
        OBS! The top level doesn't get parsed properly,
        so the code given should always be surrounded
        by parentheses and have them removed afterward.
        """

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
                if e.value in self.parentheses.right:
                    # If the closing parenthesis does not match
                    # the type that was most recently opened,
                    # there has been a mismatch
                    if e.type != history[-1]:
                        raise MismatchedParentheses(
                                f'{e.type} does not match with {history[-1]}')

                    stack.pop()
                    history.pop()

                    section = stack[-1][-1]

                    # Form infix functions
                    section = self.infixes.structure(section)

                    # Segment section by delimiters
                    section = self.delimiters.segment(section)
                    
                    # Replace section with a section element
                    stack[-1][-1] = Element(e.type, section)

                    
                    # If the type of the section is a capsule,
                    # it is intended for a function call
                    if stack[-1][-1].type in self.capsules:
                        # If the section is preceded by a label, encapsule the two
                        if len(stack[-1]) > 1 and stack[-1][-2] == 'LABEL':
                            # Use the value of the label as the type of function call
                            type_ = stack[-1][-2].value
                            # Use the value of the section as arguments
                            value = stack[-1][-1].value

                            # Remove the original section element
                            stack[-1].pop(-1)
                            # Add the new function call element
                            stack[-1][-1] = Element(type_, value)

                else:
                    raise InvalidParenthesis('Parenthesis element found with invalid parenthesis')

            else:
                # If the element is not a parenthesis,
                # add it to the currently opened section
                stack[-1].append(e)

            i += 1

        return stack[-1]