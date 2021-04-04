import re

from .element import Element
from .exceptions import MissingDelimiter, EmptySection


class Delimiters:
    """Create sublists where items are separated by delimiters

    Ex. [  A B , C D  ;  E F , G H  ]
    --> [[[A B] [C D]] [[E F] [G H]]]
    
    Use the segment function for multiple delimiters
    """    

    def __init__(self, delimiters=';,', flatten_mode='global', allow_empty_sections=False):
        """Arguments:
            delimiters -- str: A string of delimiter characters in descending priority

            flatten_mode -- str: Whether to flatten single-item lists after segmentation
                             'local' --> based on each section's own length
                            'global' --> or the maximum length of all sections

            allow_empty_sections -- bool: Whether to allow empty sections
                            If allowed, empty sections will result in empty lists
        """
        self.delimiters = [Element('DELIMITER', d) for d in delimiters]
        self.regex = f'[{re.escape(delimiters)}]'

        self.flatten_mode = flatten_mode
        self.allow_empty_sections = allow_empty_sections

    def __contains__(self, element):
        """Check if an element is a valid delimiter"""
        return any(element == delimiter for delimiter in self.delimiters)

    def contains(self, array, delimiter=None):
        """Check if an array contains any delimiters,
        or a specific one if specified
        """
        if delimiter:
            return any(element == delimiter for element in array)
        return any(element in self for element in array)

    def segment_single(self, array, delimiter):
        """Segment an array by a specified delimiter"""

        sections = [[]]


        if not self.contains(array, delimiter):
            raise MissingDelimiter(f'No instances of {delimiter} was found')


        # Separate the elements between delimiters
        # by starting a new list whenever a delimiter is encountered
        for element in array:
            if element == 'DELIMITER':
                sections.append([])
            else:
                sections[-1].append(element)


        # Raise error if there are empty sections and it is not allowed
        if not self.allow_empty_sections:
            if not all(sections, key=len):
                raise EmptySection('Empty sections are not allowed')


        # Flatten sections depending on the specified mode

        if self.flatten_mode == 'global' and max(sections, key=len) <= 1:
            # Flatten all sections if there are no sections longer than one element
            for i, section in enumerate(sections):
                if len(section) > 0:
                    sections[i] = section[0]

        if self.flatten_mode == 'local':
            # Flatten sections which contain only one element
            for i, section in enumerate(sections):
                if len(section) == 1:
                    sections[i] = section[0]


        # Convert all lists into sequence elements
        for i, section in enumerate(sections):
            if type(section) is list:
                sections[i] = Sequence(section)

        return sections

    def segment_many(self, array, delimiters):
        """Segment an array by multiple delimiters"""

        if len(delimiters) == 0:
            return array

        # Segment array by priority
        
        for delimiter in delimiters:
            try:
                array = self.segment_single(array, delimiter)
            except MissingDelimiter:
                # If the delimiter cannot be found
                # do not attempt to segment any deeper
                continue
            
            # Do not attempt to segment any deeper
            # if there are no more delimiters left
            # or if the array is not long enough
            if not delimiters[1:] or len(array) <= 1:
                continue

            # For every element in the newly segmented array,
            # if one is a sequence, segment its parts
            for i, element in enumerate(array):
                if type(element) is Sequence:
                    array[i] = Sequence(self.segment_many(element.value, delimiters[1:]))

        return array

    def segment(self, array):
        """Segment an array by delimiters"""
        return self.segment_many(array, self.delimiters)


class Sequence(Element):
    """A sequence generated from delimiter segmentation"""
    
    def __init__(self, array):
        if type(array) is not list:
            raise ValueError('Value must be a list')
        super().__init__('SEQUENCE', array)

    def __len__(self):
        return len(self.value)