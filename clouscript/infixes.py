import re

from .element import Element
from .exceptions import UnmatchedInfix


class Infixes:
    """An object for organising and structuring infixes
    
    infixes -- dict: Each key represents the priority of the items
                     in the list held in the corresponding value.
                     Use an odd value for left-handed infixes
                     and an even value for right-handed infixes.

    types -- dict: Names used for the new elements
                   in place of the original infix name

    Ex. {
        3: ['not', 'or', 'and'],
        11: ['==', '!='],
        15: ['+', '-']
    }
    """

    def __init__(self, infixes=None, types=None):
        if not infixes:
            infixes = {
                 1: '='.split(),

                # Logic
                 3: 'not or and'.split(),
                 5: ['not in', 'in'],
                 7: ['has not', 'has'],
                 9: ['is not', 'is'],

                # Comparison
                11: '== !='.split(),
                13: '<= < >= >'.split(),
                
                # Operation
                15: '+-',
                17: '* / // %'.split(),
                19: '^',

                # Special
                21: '.'
            }

        # Store the priority for each infix
        self.infixes = {
            infix: priority
            for priority, infixes in infixes.items()
            for infix in infixes
        }

        # Generate regular expression for all infixes
        self.regex = '|'.join([
            re.escape(word)
            for priority, words in reversed(sorted(infixes.items()))
            for word in words
        ])

        if not types:
            types = {
                '=': 'SET',

                # Comparison
                '==': 'EQ', '!=': 'NE',
                '<=': 'LE',  '<': 'LT', '>=': 'GE',  '>': 'GT',

                # Operation
                '+': 'ADD', '-': 'SUB',
                '*': 'MUL', '/': 'DIV', '//': 'FDIV', '%': 'MOD',
                '^': 'POW',

                # Special
                '.': 'INDEX'
            }

        self.types = types

    def structure(self, array):
        """Fit arguments of infix functions into new elements"""
        
        # An infix function requires both
        # a right-hand and a left-hand side
        if len(array) < 3:
            return array

        # Generate priority map
        # This is a 1D array of integers
        # representing the infix priority of each element 
        priorities = [
            self.infixes[element.value]
            if element == 'INFIX' else 0
            for element in array
        ]
        
        # If an infix is found at any edge of the array,
        # it can obviously not have non-infix elements on both sides
        if priorities[0]:
            raise UnmatchedInfix(f'{array[0]} is missing a left-hand element')
        if priorities[-1]:
            raise UnmatchedInfix(f'{array[-1]} is missing a right-hand element')

        # If any infixes are found beside each other,
        # they can obviously not have non-infix elements on both sides
        if any(a and b for a, b in zip(priorities[:-1], priorities[1:])):
            raise UnmatchedInfix(f'Infixes found beside each other')

        # Start with the highest priority in the list and work your way down
        # Get the upper limit of all the priorities in the list for every iteration
        while highest_priority := max(priorities):
            # Locate at which indices the top priority infixes are
            priority_indices = [i for i, p in enumerate(priorities)
                                    if p == highest_priority]

            # Swap order depending on handedness
            if highest_priority % 2 == 0:
                priority_indices = priority_indices[::-1]

            while priority_indices:
                # left-hand (i), infix (j), and right-hand (k) indices
                j = priority_indices[0]
                i, k = j-1, j+1

                # left-hand, infix, and right-hand elements
                left, infix, right = array[i:k+1]

                # Find type name for infix if provided
                type_ = self.types.get(infix.value, infix.value)
                function = Element(type_, (left, right))

                # Remove the original elements
                # and insert the new function element
                del array[i:k]
                array[i] = function

                # Clear their entries in the priority list
                # and nullify the priority of the new element
                del priorities[i:k]
                priorities[i] = 0
                
                # Move on to the next priority index
                priority_indices.pop(0)

                # If the current highest priority is left-handed,
                # after an element has been removed, move the rest 2 steps to the left
                if highest_priority % 2 == 1:
                    priority_indices = [i - 2 for i in priority_indices]

        return array