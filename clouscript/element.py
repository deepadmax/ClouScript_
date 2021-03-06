

class Element:
    """The most basic element in the code.
    It represents anything from a function call
    to an integer or a collection.
    All types of elements inherit from this class.
    """
    
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'<{self.type}: {repr(self.value)}>'

    def __eq__(self, other):
        """
        If a string is provided:
            Check if element is a certain type
        If an element is provided:
            Check if the elements are equal in type and value
        """

        if type(other) is str:
            return self.type == other

        if type(other) is Element:
            return self.type == other.type \
              and self.value == other.value

    def asstring(self, indent=1):
        if type(self.value) in (list, tuple):
            subelements = '\n'.join(
                '  ' * indent + f'{element.asstring(indent=indent + 1)}'
                for element in self.value
            )

            return f'<{self.type}>\n{subelements}'
            
        return f'<{self.type}: {self.value}>'