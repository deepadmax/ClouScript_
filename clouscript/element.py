

class Element:
    """The most basic element in the code.
    It represents anything from a function call
    to an integer or a collection.
    All types of elements inherit from this class.
    """
    
    def __init__(self, name, value):
        self.name = name
        self.value = value