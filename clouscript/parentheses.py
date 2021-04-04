import re


class Parentheses:
    def __init__(self, string='ROUND=() SQUARE=[] CURLY={}'):
        """A collection of parentheses and their group names
        
        Each entry is the group name, and the left and right parentheses,
        separated by an equal sign. Each entry is separated by a semicolon
        
        ROUND=() SQUARE=[] CURLY={} ANGLED=<>
        """

        # Partition string into entries of group name and characters
        entries = [entry.partition('=') for entry in string.split(' ')]
        # Store group names and paranthesis characters in two separate lists
        self.groups, _, self.pairs = zip(*entries)
        
        # Divide pairs into left and right parentheses
        self.left, self.right = map(''.join, zip(*self.pairs))
        
        # Join left and right parentheses into one collective string
        self.parentheses = ''.join(self.pairs)
        
        # Create regular expression for all characters
        self.regex = f'[{re.escape(self.parentheses)}]'
        
        
    def find_group(self, parenthesis):
        """Find which group a parenthesis belongs to"""
        
        i = self.parentheses.index(parenthesis)
        group = self.groups[i // 2] if i >= 0 else None
        
        return group