

class Element:
    """The most basic element in the code.
    It represents anything from a function call
    to an integer or a collection.
    All types of elements inherit from this class.
    """
    
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __eq__(self, value):
        """
        If a string is provided:
            Check if element is a certain type
        If an element is provided:
            Check if the elements are equal in type and value
        """
        return self.type == value