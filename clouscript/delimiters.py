import re

from .element import Element
from .exceptions import LexingError


DELIMITER = 'DELIMITER'


class Delimiters:
    """Create sublists where items are divided by separators

    Ex. [  A B , C D  ;  E F , G H  ]
    --> [[[A B] [C D]] [[E F] [G H]]]
    
    Use the segment function for multiple separators"""

    def __init__(self, delimiters=',;', flatten_mode='global', allow_empty_sections=False):
        """Arguments:
            delimiters -- str: A string of delimiter characters,
                               in order of least priority

            flatten_mode -- str: Whether to flatten single-item lists after segmentation
                             'local' --> based on each section's own length
                            'global' --> or the maximum length of all sections

            allow_empty_sections -- bool: Whether to allow empty sections
                            If allowed, empty sections will result in empty lists
        """
        self.delimiters = [Element(DELIMITER, d) for d in delimiters]
        self.regex = f'[{re.escape(delimiters)}]'

        self.flatten_mode = flatten_mode
        self.allow_empty_sections = allow_empty_sections

    def __contains__(self, element):
        """Check if an element is a valid delimiter"""
        return any(element == delimiter for delimiter in self.delimiters)

    def contains(self, array):
        """Check if an array contains any delimiters"""
        return any(element in self for element in array)

    def segment_single(self, array, delimiter):
        """Segment an array once by a specified delimiter"""

        sections = [[]]

        # Return the original array as is,
        # if no instance of the specified delimiter can be found
        if not any(element == delimiter for element in array):
            return array

        # Separate the elements between delimiters
        # by starting a new list whenever a delimiter is encountered
        for element in array:
            if element == DELIMITER:
                sections.append([])
            else:
                sections[-1].append(element)


        # Raise error if there are empty sections and it is not allowed
        if not self.allow_empty_sections:
            if any(sections, key=lambda e: len(e) == 0):
                raise LexingError('Empty sections are not allowed')


        # Flatten sections depending on the specified mode

        if self.flatten_mode == 'global' and max(sections, key=len) == 1:
            # Flatten all sections if there are no sections longer than one element
            for i, section in enumerate(sections):                
                sections[i] = section[0]

        if self.flatten_mode == 'local':
            # Flatten sections which contain only one element
            for i, section in enumerate(sections):
                if len(section) == 1:
                    sections[i] = section[0]

        return sections