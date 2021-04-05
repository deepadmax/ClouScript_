from clouscript.lexer import Lexer
from clouscript.element import Element


text = """doif (
    /* Three if-statements followed by an else-statement */
    
    CHANNEL.name == "General" (
        3 + (1 * 2)
    )

    USER has not 1235 (
        statement2
    )

    USER is 4569 (
        statement3
    )
    
    ( 
        statement4// This is the else-statement
    )
)"""

lexer = Lexer()
print(list(lexer.lex(text)))