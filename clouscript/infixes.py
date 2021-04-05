import re

from .element import Element


class Infixes:
    """An object for organising and structuring infixes
    
    infixes -- dict: each key represents the priority of the items
                     in the list held in the corresponding value
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